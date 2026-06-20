from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from leave_management.models import Leave
from datetime import date,datetime
from django.contrib import messages

# Create your views here.
# apply_leave

def apply_leave(req):
    return render(req,"employee/apply_leave.html")



def save_leave(req):

    if req.method == "POST":

        leave_type = req.POST.get('leave_type')
        start_date = req.POST.get('start_date')
        end_date = req.POST.get('end_date')
        leave_duration = req.POST.get('leave_duration')
        reason = req.POST.get('reason')
        attachment = req.FILES.get('attachment')

        # -------------------------
        # Date Validation
        # -------------------------

        start_date_obj = datetime.strptime(
            start_date,
            "%Y-%m-%d"
        ).date()

        end_date_obj = datetime.strptime(
            end_date,
            "%Y-%m-%d"
        ).date()

        if start_date_obj < date.today():

            messages.error(
                req,
                "Past Date Leave Not Allowed"
            )

            return redirect("/apply_leave")

        if end_date_obj < start_date_obj:

            messages.error(
                req,
                "End Date Must Be Greater Than Start Date"
            )

            return redirect("/apply_leave")

        # -------------------------
        # Medical Leave Validation
        # -------------------------

        if leave_type == "Medical Leave" and not attachment:

            messages.error(
                req,
                "Medical Certificate Required"
            )

            return redirect("/apply_leave")

        # -------------------------
        # Sick Leave Validation
        # -------------------------

        if leave_type == "Sick Leave":

            sick_leave_count = Leave.objects.filter(
                user=req.user,
                leave_type='Sick Leave',
                start_date__month=date.today().month,
                start_date__year=date.today().year,
                status='Approved'
            ).count()

            if sick_leave_count >= 2:

                messages.error(
                    req,
                    "Monthly Sick Leave Limit Reached"
                )

                return redirect("/apply_leave")

        # -------------------------
        # Save Leave
        # -------------------------

        leave = Leave(
            user=req.user,
            leave_type=leave_type,
            start_date=start_date,
            end_date=end_date,
            leave_duration=leave_duration,
            reason=reason
        )

        if attachment:
            leave.attachment = attachment

        leave.save()

        messages.success(
            req,
            "Leave Applied Successfully"
        )

        return redirect("/leave_list")

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
        leave.leave_duration = req.POST.get("leave_duration")
        leave.reason = req.POST.get("reason")

        if req.FILES.get("attachment"):
            leave.attachment = req.FILES.get("attachment")

        leave.save()

    return redirect("leave_list")

def delete_leave(req,id):
    leave = Leave.objects.get(id=id)
    leave.delete()
    return redirect("/leave_list")