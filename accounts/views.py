from django.db.models import Q
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.models import User
from departments.models import Department


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
        user.password = password
        user.salary = salary
        user.address = address
        user.date_joined = date_joined
        user.department = department
        user.role = role
        user.profile_image = profile_image

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


        # Department update
        department_id = req.POST.get('department')

        if department_id:
            user.department = Department.objects.get(
                id=department_id
            )


        user.role = "manager"


        # Password update
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