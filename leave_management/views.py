from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from leave_management.models import Leave

# Create your views here.
# apply_leave

def apply_leave(req):
    return render(req,"employee/apply_leave.html")

def save_leave(req):
    if req.method == "POST":
        leave = Leave(
            leave_type = req.POST.get('leave_type'),
            start_date = req.POST.get('start_date'),
            end_date = req.POST.get('end_date'),
            reason = req.POST.get('reason'),
            user_id = req.user.id
        )
        if req.FILES.get('attachment'):
            leave.attachment = req.FILES.get('attachment')
        leave.save()
        return redirect("/apply_leave")
    return redirect("/apply_leave")

def leave_list(req):
    myleave = Leave.objects.filter(user_id=req.user.id)
    return render(req,"employee/leave_list.html",{"myleave":myleave})

def edit_leave(req,id):
    leave = Leave.objects.get(id=id)
    return render(req,"employee/edit_leave.html",{"leave":leave})

def update_leave(req, id):
    leave = Leave.objects.get(id=id)

    if req.method == "POST":
        leave.start_date = req.POST.get("start_date")
        leave.end_date = req.POST.get("end_date")
        leave.leave_type = req.POST.get("leave_type")
        leave.reason = req.POST.get("reason")

        if req.FILES.get("attachment"):
            leave.attachment = req.FILES.get("attachment")

        leave.save()

    return redirect("leave_list")

def delete_leave(req,id):
    leave = Leave.objects.get(id=id)
    leave.delete()
    return redirect("/leave_list")