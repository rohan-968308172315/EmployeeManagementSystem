from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from departments import models

# Create your views here.

def add_department(req):
    return render(req,"admin/add_department.html")

def save_department(req):
    # return HttpResponse("Hello")
    if req.method == "POST":
        models.Department.objects.create(
            department_name = req.POST.get('department_name'),
            department_code = req.POST.get('department_code'),
            description = req.POST.get('description'),
            status = req.POST.get("status")
        )
        return redirect('/add_department')
    return redirect('/add_department')

def department_list(req):
    dep = models.Department.objects.all()
    obj = {"dep":dep}
    return render(req,"admin/department_list.html",obj)

def edit_department(req,id):
    dep = models.Department.objects.get(id=id)
    return render(req,"admin/edit_department.html",{"editdep":dep})

def update_department(req,id):
    if req.method == "POST":
        department = get_object_or_404(models.Department,id=id)
        department.department_name = req.POST.get('department_name')
        department.department_code = req.POST.get('department_code')
        department.description = req.POST.get('description')
        department.status = req.POST.get('status')
        department.save()
        return redirect("/department_list")
    return redirect("/department_list")

def delete_department(req,id):
    depart = get_object_or_404(models.Department,id=id)
    depart.delete()
    return redirect("/department_list")