from .models import CompanyDetails


def company_details(request):
    try:
        company = CompanyDetails.objects.first()
    except Exception:
        company = None

    return {
        'company_details': company
    }
