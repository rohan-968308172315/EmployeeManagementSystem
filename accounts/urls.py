from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="login", permanent=False)),
    path("login/",views.login_view,name="login"),
    path("admin_dashboard/",views.admin_dashboard,name="admin_dashboard"),
    path('logout_view/',views.logout_view,name='logout_view'),
    
    path('manager_dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('employee_dashboard/', views.employee_dashboard, name='employee_dashboard'),
    
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<int:user_id>/', views.reset_password, name='reset_password'),
    
    path('add_manager/', views.add_manager, name='add_manager'),
    path('save_manager/', views.save_manager, name='save_manager'),
    path('manager_list/', views.manager_list, name='manager_list'),
    path('edit_manager/<int:id>', views.edit_manager, name='edit_manager'),
    path('update_manager/<int:id>', views.update_manager, name='update_manager'),
    path('delete_manager/<int:id>', views.delete_manager, name='delete_manager'),
    
    path('add_employee/', views.add_employee, name='add_employee'),
    path('save_employee/', views.save_employee, name='save_employee'),
    path('department_users/', views.department_users, name='department_users'),
    path('employee_list/', views.employee_list, name='employee_list'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('company_details/', views.company_details, name='company_details'),
    path('update_profile/<int:id>', views.update_profile, name='update_profile'),
    path('update_company_details/<int:id>', views.update_company_details, name='update_company_details'),
    
    
    path('employee_pending_leaves/', views.employee_pending_leaves, name='employee_pending_leaves'),
    path('approve_employee_leave/<int:id>', views.approve_employee_leave, name='approve_employee_leave'),
    path('reject_employee_leave/<int:id>', views.reject_employee_leave, name='reject_employee_leave'),
    path('employee_approve_leaves/', views.employee_approve_leaves, name='employee_approve_leaves'),
    path('employee_rejected_leaves/', views.employee_rejected_leaves, name='employee_rejected_leaves'),
    
]   