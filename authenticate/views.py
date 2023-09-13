from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, SignupForm

from .models import Profile, CustomUser

from members.models import Member
from staff.models import Notification


from django.contrib import messages

from validate_email import validate_email
from django.core.mail import EmailMessage
from django.conf import settings

from django.urls import reverse
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site

from .utils import token_generator

from django.contrib.auth import authenticate, login


# Create your views here.


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data["username"]
        if not str(username).isalnum():
            return JsonResponse(
                {
                    "username_error": "Username should ONLY contain alphanumeric characters"
                },
                status=400,
            )
        if CustomUser.objects.filter(username=username).exists():
            return JsonResponse(
                {"username_error": "Username already in use, Choose another one!"},
                status=409,
            )
        return JsonResponse({"username_valid": True})


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data["email"]
        if not validate_email(email):
            return JsonResponse({"email_error": "Email is invalid"}, status=400)
        if CustomUser.objects.filter(email=email).exists():
            return JsonResponse(
                {"email_error": "Email already in use, Choose another one!"}, status=409
            )
        return JsonResponse({"email_valid": True})


def landing(request):
    return render(request, "authentication/landing.html")


def Registration(request):
    form = SignupForm()
    if request.method == "POST":
        username = request.POST["username"]
        email_ = request.POST["email"]
        password = request.POST["password"]
        if not CustomUser.objects.filter(username=username).exists():
            if not CustomUser.objects.filter(email=email_).exists():
                if len(password) < 6:
                    messages.error(request, "Password too short")
                    return render(request, "authentication/register.html", context)
                registered_user = CustomUser.objects.create(
                    username=username, email=email_
                )
                registered_user.set_password(password)
                registered_user.is_avtive = False
                registered_user.save()
                Profile.objects.create(
                    user=registered_user,
                    email=registered_user.email,
                    username=registered_user.username,
                )

            # path_to_view
            # - getting the domain we are on
            # - relative url to verification
            # - encode uid
            # - token
            uidb64 = urlsafe_base64_encode(force_bytes(registered_user.pk))

            domain = get_current_site(request).domain
            link = reverse(
                "activate",
                kwargs={
                    "uidb64": uidb64,
                    "token": token_generator.make_token(registered_user),
                },
            )
            activate_url = f"http://{domain}{link}"
            email_subject = "Activate your account"
            email_body = f"""Hi {registered_user.username}!
            Please use this link to verify your account
            {activate_url}"""
            email = EmailMessage(
                email_subject,
                email_body,
                settings.EMAIL_HOST_USER,
                [email_],
            )
            email.send(fail_silently=False)
            messages.success(request, "Account succesfully created!")
            return redirect("member_dashboard")
    context = {"form": form, "fieldValues": request.POST}

    return render(request, "authentication/register.html", context)


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(id=id)
            if not token_generator.check_token(user, token):
                return redirect("login" + "?message=" + "User already activated")
            if user.is_allowed:
                return redirect("login")
            user.is_active = True
            user.save()
            messages.success(request, "Account activated successfully")
            return redirect("login")

        except Exception as e:
            print(e)
        return redirect("login")


def Login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                messages.error(request, "Invalid username or password")

            else:
                if user.is_allowed:
                    login(request, user)
                    messages.success(
                        request, f"Welcome {user.username} you are now logged in"
                    )
                    if user.is_staff:
                        return redirect("home")
                    return redirect("member_dashboard")
                messages.success(
                    request, "Account is not active, please check your email"
                )

    return render(request, "authentication/login.html")


def logoutUser(request):
    logout(request)
    return redirect("login")


@login_required(login_url="login")
def member_profile(request):
    user = request.user
    first_name = user.first_name
    form = Profile.objects.get(user=user)
    print(f"first_name: {first_name}")
    notifications = None
    notification_count = 0

    if Member.objects.filter(guardian_name=user.first_name).exists():
        member = Member.objects.get(guardian_name=user.first_name)
        if member.paid:
            notifications = Notification.objects.all()
            notification_count = Notification.objects.filter(is_read=False).count()

    context = {
        "user": user,
        "form": form,
        "notifications": notifications,
        "notification_count": notification_count,
    }
    return render(request, "members/profile/profile.html", context)


@login_required(login_url="login")
def updateMemberProfile(request):
    user = CustomUser.objects.get(username=request.user)
    notifications = None
    notification_count = None
    profile = Profile.objects.get(user=user)
    form = ProfileForm(instance=profile)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            user.first_name = profile.first_name
            user.last_name = profile.last_name
            full_name = user.first_name + " " + user.last_name

            if Member.objects.filter(user=user).exists():
                member = Member.objects.get(user=user)
                if member.paid:
                    member.email = profile.email
                    member.guardian_name = full_name
                    member.phone = profile.phone
                    member.address = profile.address
                    print(f"guardian name: {member.guardian_name}")
                    member.save()
            user.save()
            profile.save()
            return redirect("member_profile")

    if Member.objects.filter(user=user).exists():
        member = Member.objects.get(user=user)
        if member.paid:
            notifications = Notification.objects.all()
            notification_count = Notification.objects.filter(is_read=False).count()
    context = {
        "form": form,
        "notifications": notifications,
        "notification_count": notification_count,
    }
    return render(request, "members/profile/profile_form.html", context)


def registerStaff(request):
    form = SignupForm()
    if request.method == "POST":
        username = request.POST["username"]
        email_ = request.POST["email"]
        password = request.POST["password"]
        if not CustomUser.objects.filter(username=username).exists():
            if not CustomUser.objects.filter(email=email_).exists():
                if len(password) < 6:
                    messages.error(request, "Password too short")
                    return render(request, "authentication/register.html", context)
                registered_user = CustomUser.objects.create(
                    username=username, email=email_
                )
                registered_user.set_password(password)
                registered_user.is_avtive = False
                registered_user.save()
                Profile.objects.create(
                    user=registered_user,
                    email=registered_user.email,
                    username=registered_user.username,
                )
                print(f"registered_user.username: {registered_user.username}")

            # path_to_view
            # - getting the domain we are on
            # - relative url to verification
            # - encode uid
            # - token
            uidb64 = urlsafe_base64_encode(force_bytes(registered_user.pk))

            domain = get_current_site(request).domain
            link = reverse(
                "activate_staff",
                kwargs={
                    "uidb64": uidb64,
                    "token": token_generator.make_token(registered_user),
                },
            )
            activate_url = f"http://{domain}{link}"
            email_subject = "Activate your account"
            email_body = f"""Hi {registered_user.username}!
            Please use this link to verify your account
            {activate_url}"""
            email = EmailMessage(
                email_subject,
                email_body,
                settings.EMAIL_HOST_USER,
                [email_],
            )
            email.send(fail_silently=False)
            messages.success(request, "Account succesfully created!")
            return redirect("login")
    context = {"form": form, "fieldValues": request.POST}

    return render(request, "authentication/register_staff.html", context)


class StaffVerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(id=id)
            if not token_generator.check_token(user, token):
                return redirect("login" + "?message=" + "User already activated")
            if user.is_allowed:
                return redirect("login")
            user.is_allowed = True
            user.is_staff = True
            user.save()
            messages.success(request, "Account activated successfully")
            return redirect("login")
        except Exception as e:
            print(e)
        return redirect("login")
