from django.db.models import Q
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.models import User,CompanyDetails
from departments.models import Department
from leave_management.models import Leave
from django.contrib.auth.hashers import make_password


def _redirect_for_role(role):

    if not role:
        return None

    role = str(role).strip().lower()

    if role == "admin":
        return redirect("admin_dashboard")

    if role == "manager":
        return redirect("manager_dashboard")

    if role == "employee":
        return redirect("employee_dashboard")

    return None


def _get_login_user(request, identifier, password):

    identifier = (identifier or "").strip()
    password = password or ""

    if not identifier or not password:
        return None

    user = authenticate(
        request=request,
        username=identifier,
        password=password
    )

    if user:
        return user

    user = User.objects.filter(
        Q(username__iexact=identifier) | Q(email__iexact=identifier)
    ).first()

    if user and user.check_password(password) and user.is_active:
        return user

    return None

def login_view(request):

    if request.user.is_authenticated:
        redirect_response = _redirect_for_role(getattr(request.user, "role", None))

        if redirect_response:
            return redirect_response

        logout(request)
        messages.error(
            request,
            "User role is not configured correctly"
        )

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = _get_login_user(request, username, password)
        
        # print(user)

        if user:

            login(request,user)

            redirect_response = _redirect_for_role(getattr(user, "role", None))

            if redirect_response:
                return redirect_response

            logout(request)
            messages.error(
                request,
                "User role is not configured correctly"
            )

        else:

            messages.error(
                request,
                "Invalid Username Or Password"
            )

    return render(
        request,
        "login.html"
    )


def logout_view(request):

    logout(request)

    return redirect('/login')


@login_required(login_url='login')
def admin_dashboard(request):

    return render(
        request,
        "admin/admin_dashboard.html"
    )


@login_required(login_url='login')
def manager_dashboard(request):

    return render(
        request,
        "manager/manager_dashboard.html"
    )


@login_required(login_url='login')
def employee_dashboard(request):

    return render(
        request,
        "employee/employee_dashboard.html"
    )
    
def forgot_password(request):

    if request.method == "POST":

        email = request.POST.get("email")

        try:

            user = User.objects.get(email=email)

            return redirect(
                'reset_password',
                user_id=user.id
            )

        except User.DoesNotExist:

            messages.error(
                request,
                "Email Not Found"
            )

    return render(
        request,
        "forgot_password.html"
    )
    
def reset_password(request, user_id):
    
    user = User.objects.get(id=user_id)

    if request.method == "POST":

        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:

            messages.error(
                request,
                "Password And Confirm Password Not Match"
            )

            return redirect(
                'reset_password',
                user_id=user.id
            )

        user.set_password(password)
        user.save()

        messages.success(
            request,
            "Password Changed Successfully"
        )

        return redirect('login')

    return render(
        request,
        "reset_password.html",
        {
            "user": user
        }
    )
    
def add_manager(request):
    
    used_departments = User.objects.filter(
        role='manager',
    ).values_list(
        'department_id',
        flat=True
    )

    departments = Department.objects.filter(
        status='Active'
    ).exclude(
        id__in=used_departments
    ).order_by('department_name')

    return render(
        request,
        'admin/add_manager.html',
        {
            'department': departments
        }
    )
    
def save_manager(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        password = request.POST.get("password")
        salary = request.POST.get("salary")
        address = request.POST.get("address")
        department_id = request.POST.get("department")
        role = request.POST.get("role")
        date_joined = request.POST.get("date_joined")
        profile_image = request.FILES.get('profile_image')

        # duplicate username check
        if User.objects.filter(username=username).exists():
            messages.error(request,"Username is already exists")
            return redirect("/add_manager")

        # duplicate email check
        if User.objects.filter(email=email).exists():
            messages.error(request,"Email is already exists")
            return redirect("/add_manager")

        department = Department.objects.get(id = department_id)

        user = User.objects.create_user(username=username,email=email,password=password)

        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        user.mobile = mobile
        user.original_password = password
        user.password = password
        user.salary = salary
        user.address = address
        user.date_joined = date_joined
        user.department = department
        user.role = role
        user.profile_image = profile_image
        user.set_password(password)
        user.save()

        messages.success(request,"Manager Added Successfully")
        return redirect("/add_manager")
    return redirect("/add_manager")

def manager_list(req):
    manager = User.objects.filter(role="manager")
    obj = {"manager":manager}
    return render(req,"admin/manager_list.html",obj)

def edit_manager(req,id):
    
    manager = get_object_or_404(
        User,
        id=id,
        role="manager"
    )

    used_departments = User.objects.filter(
        role="manager"
    ).exclude(
        id=id
    ).values_list(
        'department_id',
        flat=True
    )


    departments = Department.objects.filter(
        status="Active"
    ).exclude(
        id__in=used_departments
    ).order_by(
        'department_name'
    )


    return render(
        req,
        "admin/edit_manager.html",
        {
            "editmanager":manager,
            "department":departments
        }
    )

def update_manager(req,id):
    
    if req.method == "POST":

        user = get_object_or_404(
            User,
            id=id
        )

        user.first_name = req.POST.get('first_name')
        user.last_name = req.POST.get('last_name')
        user.username = req.POST.get('username')
        user.email = req.POST.get('email')
        user.mobile = req.POST.get('mobile')
        user.salary = req.POST.get('salary')
        user.date_joined = req.POST.get('date_joined')
        user.address = req.POST.get('address')
        user.original_password = req.POST.get('password')


        # Department update
        department_id = req.POST.get('department')

        if department_id:
            user.department = Department.objects.get(
                id=department_id
            )


        user.role = "manager"


        password = req.POST.get('password')
        
        if password:
            user.set_password(password)
    

        # Image update
        if req.FILES.get('profile_image'):
            user.profile_image = req.FILES.get(
                'profile_image'
            )


        user.save()

        return redirect('/manager_list')


    return redirect('/manager_list')


def delete_manager(req,id):
    user = get_object_or_404(User,id=id)
    user.delete()
    return redirect("/manager_list")

def add_employee(req):
    departments = Department.objects.filter(status="Active").order_by("department_name")
    return render(
        req,
        "admin/add_employee.html",
        {
            "department": departments
        }
    )

def save_employee(req):
    if req.method == "POST":
        first_name = req.POST.get("first_name")
        last_name = req.POST.get("last_name")
        username = req.POST.get("username")
        email = req.POST.get("email")
        mobile = req.POST.get("mobile")
        password = req.POST.get("password")
        salary = req.POST.get("salary")
        address = req.POST.get("address")
        department_id = req.POST.get("department")
        under_by_id = req.POST.get("under_by")
        date_joined = req.POST.get("date_joined")
        profile_image = req.FILES.get("profile_image")

        if User.objects.filter(username=username).exists():
            messages.error(req, "Username is already exists")
            return redirect("/add_employee")

        if User.objects.filter(email=email).exists():
            messages.error(req, "Email is already exists")
            return redirect("/add_employee")

        department = Department.objects.filter(id=department_id).first()
        under_by = User.objects.filter(id=under_by_id, department_id=department_id).first()

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.first_name = first_name
        user.last_name = last_name
        user.mobile = mobile
        user.salary = salary
        user.address = address
        user.department = department
        user.role = "employee"
        user.under_by = under_by
        user.profile_image = profile_image
        user.date_joined = date_joined
        user.original_password = password
        user.save()

        messages.success(req, "Employee Added Successfully")
        return redirect("/add_employee")

    return redirect("/add_employee")


def department_users(req):
    department_id = req.GET.get("department_id")

    users = User.objects.filter(
        department_id=department_id,
        role="manager"
    ).order_by("first_name", "last_name", "username")

    data = [
        {
            "id": user.id,
            "name": user.get_full_name() or user.username,
        }
        for user in users
    ]

    return JsonResponse({"users": data})


def employee_list(req):
    if req.user.role == "manager":
        emp = User.objects.filter(role="employee",under_by=req.user.id)
    else:
        emp = User.objects.filter(role="employee")
    return render(req,"admin/employee_list.html",{"emp":emp})


@login_required
def profile(req):
    user = req.user
    return render(req,"profile.html",{"user_data":user})

@login_required
def edit_profile(req):
    user = req.user
    return render(req,"edit_profile.html",{"user_data":user})


def update_profile(req,id):
    if req.method == "POST":
    
        user = get_object_or_404(
            User,
            id=id
        )

        user.first_name = req.POST.get('first_name')
        user.last_name = req.POST.get('last_name')
        user.username = req.POST.get('username')
        user.email = req.POST.get('email')
        user.mobile = req.POST.get('mobile')
        user.address = req.POST.get('address')
        user.original_password = req.POST.get('password')


        password = req.POST.get('password')
        
        if password:
            user.set_password(password)
    

        # Image update
        if req.FILES.get('profile_image'):
            user.profile_image = req.FILES.get(
                'profile_image'
            )


        user.save()

        return redirect('/profile')


    return redirect('/profile')

def company_details(req):
    comp = CompanyDetails.objects.get(id=1)
    return render(req,"admin/company_details.html",{"comp":comp})

def update_company_details(req,id):
    if req.method == "POST":
        comp = get_object_or_404(CompanyDetails,id=id)

        comp.company_name = req.POST.get('company_name')
        comp.phone = req.POST.get('phone')
        comp.website = req.POST.get('website')
        comp.email = req.POST.get('email')
        comp.established_on = req.POST.get('established_on')
        comp.address = req.POST.get('address')
        comp.gst_number = req.POST.get('gst_number')
        comp.registration_number = req.POST.get('registration_number')
        comp.city = req.POST.get('city')
        comp.state = req.POST.get('state')
        comp.pincode = req.POST.get('pincode')
        comp.description = req.POST.get('description')

        if req.FILES.get('logo'):
            comp.logo = req.FILES.get('logo')
        comp.save()
    
    return redirect("/company_details")

def employee_pending_leaves(req):
    if req.user.role == "admin":
        leaves = Leave.objects.select_related('user').filter(status='Pending')
    else:
        leaves = Leave.objects.select_related('user').filter(user__under_by_id=req.user.id).filter(status='Pending')
    
    return render(req,"employee/employee_pending_leaves.html",{"leaves": leaves})

def approve_employee_leave(req,id):
    leave = Leave.objects.get(id=id)
    leave.status = "Approved"
    leave.save()
    return redirect("/employee_pending_leaves")

def employee_approve_leaves(req):
    
    if req.user.role == "admin":
        leaves = Leave.objects.select_related('user').filter(status='Approved')
    else:
        leaves = Leave.objects.select_related('user').filter(user__under_by_id=req.user.id).filter(status='Approved')
    return render(req,"employee/employee_approve_leaves.html",{"leaves":leaves})

def employee_rejected_leaves(req):
    if req.user.role == "admin":
            leaves = Leave.objects.select_related('user').filter(status='Rejected')
    else:
        leaves = Leave.objects.select_related('user').filter(user__under_by_id=req.user.id).filter(status='Rejected')
    
    return render(req,"employee/employee_rejected_leaves.html",{"leaves":leaves})

def reject_employee_leave(req,id):
    leave = Leave.objects.get(id=id)
    leave.status = "Rejected"
    leave.save()
    return redirect("/employee_pending_leaves")