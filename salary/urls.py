from django.urls import path

from . import views

urlpatterns = [
    path("salary_list/", views.salary_list, name="salary_list"),
    path("download_salary_slip/<int:salary_id>/", views.download_salary_slip, name="download_salary_slip"),
    path("send_salary_on_whatsapp/<int:salary_id>/", views.send_salary_on_whatsapp, name="send_salary_on_whatsapp"),
]