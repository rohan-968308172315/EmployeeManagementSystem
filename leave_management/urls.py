from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path("apply_leave/",views.apply_leave,name="apply_leave"),
    path("save_leave/",views.save_leave,name="save_leave"),
    path("leave_list/",views.leave_list,name="leave_list"),
    path("edit_leave/<int:id>",views.edit_leave,name="edit_leave"),
    path("update_leave/<int:id>",views.update_leave,name="update_leave"),
    path("delete_leave/<int:id>",views.delete_leave,name="delete_leave"),
]