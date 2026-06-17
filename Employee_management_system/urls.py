"""
URL configuration for Employee_management_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from departments import views as dpview

urlpatterns = [
    path('',dpview.dashboard),
    path('add_department/',dpview.add_department),
    path('department_list/',dpview.department_list),
    path('update_department/<int:id>/',dpview.update_department,name="update_department"),
    path('edit_department/<int:id>/',dpview.edit_department),
    path('delete_department/<int:id>/',dpview.delete_department),
    path('save_department/',dpview.save_department,name="save_department"),
    path('admin/', admin.site.urls),
]
