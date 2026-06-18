from django.urls import path
from . import views

urlpatterns = [
    path('add_department/',views.add_department),
    path('department_list/',views.department_list),
    path('update_department/<int:id>/',views.update_department,name="update_department"),
    path('edit_department/<int:id>/',views.edit_department),
    path('delete_department/<int:id>/',views.delete_department),
    path('save_department/',views.save_department,name="save_department"),   
]