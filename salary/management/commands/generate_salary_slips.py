from django.core.management.base import BaseCommand
from django.utils import timezone

from salary.services import generate_salary_for_month, previous_month_period


class Command(BaseCommand):
    help = "Generate monthly salary slips for managers and employees."

    def add_arguments(self, parser):
        parser.add_argument("--year", type=int, help="Salary year to generate")
        parser.add_argument("--month", type=int, help="Salary month to generate")

    def handle(self, *args, **options):
        year = options.get("year")
        month = options.get("month")

        if not year or not month:
            year, month = previous_month_period(timezone.localdate())

        slips = generate_salary_for_month(year, month)
        self.stdout.write(
            self.style.SUCCESS(
                f"Generated {len(slips)} salary slips for {month:02d}/{year}."
            )
        )