from django.urls import path
from . import views

urlpatterns = [
    path("login/",views.login_view,name="login"),
    path("admin_dashboard/",views.admin_dashboard,name="admin_dashboard"),
    path('logout/',views.logout_view,name='logout'),
    
    path('manager_dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('employee_dashboard/', views.employee_dashboard, name='employee_dashboard'),
    
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<int:user_id>/', views.reset_password, name='reset_password'),
]   