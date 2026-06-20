from django.shortcuts import render,redirect
from django.utils import timezone
from attendance.models import Attendance
from accounts.models import User
import datetime

def manager_attendance(request):

    managers = User.objects.filter(role="manager")

    today = timezone.now().date()

    for manager in managers:

        attendance = Attendance.objects.filter(
            user_id=manager.id,
            attendance_date=today
        ).first()

        manager.today_attendance = attendance

    return render(
        request,
        "admin/manager_attendance.html",
        {"att": managers}
    )

def manager_present(req,id):
    Attendance.objects.create(
        attendance_date = datetime.date.today(),
        status = 'Present',
        marked_by_id = req.user.id,
        user_id = id
    )
    if req.user.role == 'admin':
        return redirect("/manager_attendance")
    else:
        return redirect("/employee_attendance")
        
def manager_absent(req,id):
    Attendance.objects.create(
        attendance_date = datetime.date.today(),
        status = 'Absent',
        marked_by_id = req.user.id,
        user_id = id
    )
    if req.user.role == 'admin':
        return redirect("/manager_attendance")
    else:
        return redirect("/employee_attendance")

def manager_halfday(req,id):
    Attendance.objects.create(
        attendance_date = datetime.date.today(),
        status = 'Half Day',
        marked_by_id = req.user.id,
        user_id = id
    )
    if req.user.role == 'admin':
        return redirect("/manager_attendance")
    else:
        return redirect("/employee_attendance")

def employee_attendance(req):
    if req.user.role == "admin":
    
        employees = User.objects.filter(
            role='employee'
        )

    elif req.user.role == "manager":

        employees = User.objects.filter(
            role='employee',
            under_by_id=req.user.id
        )

    else:

        employees = User.objects.none()
    today = timezone.now().date()
    
    for emp in employees:
        attendance = Attendance.objects.filter(user_id=emp.id,attendance_date=today).first()
        emp.today_attendance = attendance
    
    return render(req,"employee/employee_attendance.html",{"emp":employees})