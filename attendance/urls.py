from django.urls import path
from . import views

urlpatterns = [
    path("manager_attendance/",views.manager_attendance,name="manager_attendance"),
    path("manager_present/<int:id>",views.manager_present,name="manager_present"),
    path("manager_absent/<int:id>",views.manager_absent,name="manager_absent"),
    path("manager_halfday/<int:id>",views.manager_halfday,name="manager_halfday"),
    path("employee_attendance/",views.employee_attendance,name="employee_attendance"),
]