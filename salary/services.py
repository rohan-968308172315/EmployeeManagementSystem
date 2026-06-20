from calendar import month_name, monthrange
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, Iterable, Optional, Tuple
from urllib.parse import quote

from django.db.models import Q
from django.utils import timezone

from accounts.models import CompanyDetails, User
from attendance.models import Attendance
from leave_management.models import Leave

from .models import Salarytbl


SALARY_ROLES = ("manager", "employee")


def to_money(value: Decimal | int | float) -> Decimal:
    return Decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def month_period(year: int, month: int) -> Tuple[date, date]:
    last_day = monthrange(year, month)[1]
    return date(year, month, 1), date(year, month, last_day)


def previous_month_period(reference_date: Optional[date] = None) -> Tuple[int, int]:
    reference_date = reference_date or timezone.localdate()

    if reference_date.month == 1:
        return reference_date.year - 1, 12

    return reference_date.year, reference_date.month - 1


def month_label(year: int, month: int) -> str:
    return f"{month_name[month]} {year}"


def salary_users() -> Iterable[User]:
    return User.objects.filter(role__in=SALARY_ROLES, salary__gt=0)


def count_paid_leave_days(user: User, start_date: date, end_date: date) -> int:
    approved_leaves = Leave.objects.filter(
        user=user,
        status="Approved",
        start_date__lte=end_date,
        end_date__gte=start_date,
    )

    paid_leave_days = 0
    for leave in approved_leaves:
        overlap_start = max(leave.start_date, start_date)
        overlap_end = min(leave.end_date, end_date)
        paid_leave_days += (overlap_end - overlap_start).days + 1

    return paid_leave_days


def calculate_salary_breakdown(user: User, year: int, month: int) -> Dict[str, Decimal | int]:
    start_date, end_date = month_period(year, month)
    total_working_days = monthrange(year, month)[1]

    attendance_qs = Attendance.objects.filter(
        user=user,
        attendance_date__range=(start_date, end_date),
    )

    present_days = attendance_qs.filter(status="Present").count()
    half_days = attendance_qs.filter(status="Half Day").count()
    paid_leaves = count_paid_leave_days(user, start_date, end_date)

    absent_days = max(total_working_days - present_days - half_days - paid_leaves, 0)

    basic_salary = to_money(user.salary or 0)
    daily_salary = to_money(basic_salary / Decimal(total_working_days)) if total_working_days else Decimal("0.00")
    half_day_deduction = to_money(daily_salary / Decimal(2))
    absent_deduction = to_money(daily_salary * Decimal(absent_days))
    half_day_total_deduction = to_money(half_day_deduction * Decimal(half_days))

    gross_salary = max(basic_salary - absent_deduction - half_day_total_deduction, Decimal("0.00"))
    pf_amount = to_money(basic_salary * Decimal(user.pf_percentage or 0) / Decimal(100))
    net_salary = max(gross_salary - pf_amount, Decimal("0.00"))

    return {
        "total_working_days": total_working_days,
        "present_days": present_days,
        "half_days": half_days,
        "paid_leaves": paid_leaves,
        "absent_days": absent_days,
        "basic_salary": basic_salary,
        "gross_salary": to_money(gross_salary),
        "pf_amount": pf_amount,
        "net_salary": to_money(net_salary),
    }


def generate_salary_for_user(user: User, year: int, month: int) -> Salarytbl:
    breakdown = calculate_salary_breakdown(user, year, month)
    defaults = {
        "total_working_days": breakdown["total_working_days"],
        "present_days": breakdown["present_days"],
        "half_days": breakdown["half_days"],
        "paid_leaves": breakdown["paid_leaves"],
        "absent_days": breakdown["absent_days"],
        "basic_salary": breakdown["basic_salary"],
        "gross_salary": breakdown["gross_salary"],
        "pf_amount": breakdown["pf_amount"],
        "net_salary": breakdown["net_salary"],
    }

    salary, _created = Salarytbl.objects.update_or_create(
        user=user,
        month=month,
        year=year,
        defaults=defaults,
    )
    return salary


def generate_salary_for_month(year: int, month: int) -> list[Salarytbl]:
    slips = []
    for user in salary_users():
        slips.append(generate_salary_for_user(user, year, month))
    return slips


def get_accessible_salary_queryset(user: User):
    queryset = Salarytbl.objects.select_related("user").order_by("-year", "-month", "user__first_name", "user__last_name", "user__username")

    if user.role == "admin":
        return queryset

    if user.role == "manager":
        return queryset.filter(Q(user=user) | Q(user__under_by=user))

    return queryset.filter(user=user)


def get_company_name() -> str:
    company = CompanyDetails.objects.first()
    return company.company_name if company else "Company"


def build_whatsapp_url(salary: Salarytbl) -> str:
    mobile = salary.user.mobile or ""
    digits = "".join(character for character in mobile if character.isdigit())

    if len(digits) == 10:
        digits = f"91{digits}"

    if not digits:
        return ""

    message = (
        f"Salary slip for {salary.user.get_full_name() or salary.user.username} "
        f"for {month_label(salary.year, salary.month)}. "
        f"Net salary: {salary.net_salary}."
    )
    return f"https://wa.me/{digits}?text={quote(message)}"