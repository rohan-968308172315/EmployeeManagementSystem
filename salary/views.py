from io import BytesIO

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from .models import Salarytbl
from .services import (
    build_whatsapp_url,
    generate_salary_for_month,
    get_accessible_salary_queryset,
    get_company_name,
    month_label,
    previous_month_period,
)


@login_required
def salary_list(request):
    today = timezone.localdate()
    default_year, default_month = previous_month_period(today)

    year = int(request.GET.get("year") or default_year)
    month = int(request.GET.get("month") or default_month)

    if not Salarytbl.objects.filter(year=year, month=month).exists():
        generate_salary_for_month(year, month)

    slips = get_accessible_salary_queryset(request.user).filter(
        year=year,
        month=month,
    )

    slip_rows = []
    for slip in slips:
        slip_rows.append(
            {
                "slip": slip,
                "whatsapp_link": build_whatsapp_url(slip),
            }
        )

    return render(
        request,
        "admin/salary_list.html",
        {
            "salary_rows": slip_rows,
            "selected_year": year,
            "selected_month": month,
            "selected_month_label": month_label(year, month),
        },
    )


def _build_salary_pdf_response(salary: Salarytbl) -> HttpResponse:
    buffer = BytesIO()
    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "SalaryTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=18,
        leading=22,
        spaceAfter=10,
    )
    center_style = ParagraphStyle(
        "SalaryCenter",
        parent=styles["BodyText"],
        alignment=TA_CENTER,
        fontSize=10,
        leading=13,
    )

    story = []
    story.append(Paragraph(get_company_name(), title_style))
    story.append(Paragraph("Salary Slip", title_style))
    story.append(Paragraph(month_label(salary.year, salary.month), center_style))
    story.append(Spacer(1, 8))

    employee_info = [
        ["Employee", salary.user.get_full_name() or salary.user.username],
        ["Role", salary.user.role.title()],
        ["Employee Code", salary.user.employee_code or "-"],
        ["Mobile", salary.user.mobile or "-"],
        ["Department", salary.user.department.department_name if salary.user.department else "-"],
    ]

    salary_summary = [
        ["Total Working Days", salary.total_working_days],
        ["Present Days", salary.present_days],
        ["Half Days", salary.half_days],
        ["Paid Leaves", salary.paid_leaves],
        ["Absent Days", salary.absent_days],
        ["Basic Salary", f"{salary.basic_salary}"],
        ["Gross Salary", f"{salary.gross_salary}"],
        ["PF Amount", f"{salary.pf_amount}"],
        ["Net Salary", f"{salary.net_salary}"],
    ]

    employee_table = Table(employee_info, colWidths=[40 * mm, 120 * mm])
    employee_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8EEF9")),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.whitesmoke, colors.white]),
            ]
        )
    )

    salary_table = Table(salary_summary, colWidths=[60 * mm, 100 * mm])
    salary_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2E3A59")),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.HexColor("#F7F9FC"), colors.white]),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
            ]
        )
    )

    story.append(employee_table)
    story.append(Spacer(1, 12))
    story.append(salary_table)
    story.append(Spacer(1, 10))
    story.append(Paragraph("This salary slip is generated from attendance and approved leave data.", center_style))

    document.build(story)
    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="salary-slip-{salary.user.username}-{salary.year}-{salary.month:02d}.pdf"'
    )
    response.write(pdf)
    return response


@login_required
def download_salary_slip(request, salary_id):
    salary = get_object_or_404(get_accessible_salary_queryset(request.user), id=salary_id)
    return _build_salary_pdf_response(salary)


@login_required
def send_salary_on_whatsapp(request, salary_id):
    salary = get_object_or_404(get_accessible_salary_queryset(request.user), id=salary_id)
    whatsapp_url = build_whatsapp_url(salary)

    if not whatsapp_url:
        return HttpResponseForbidden("Mobile number is required for WhatsApp sharing.")

    return render(
        request,
        "salary/whatsapp_redirect.html",
        {
            "whatsapp_url": whatsapp_url,
            "salary": salary,
        },
    )
