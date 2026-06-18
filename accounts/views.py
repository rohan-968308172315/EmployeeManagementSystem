from django.db.models import Q
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.models import User


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

    return redirect('login')


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