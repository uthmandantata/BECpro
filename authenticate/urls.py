from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_views

urlpatterns = [
    path(
        "reset_password/", auth_views.PasswordResetView.as_view(), name="reset_password"
    ),
    path(
        "reset_password_sent/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset_password_complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="authentication/password_reset_done.html"
        ),
        name="password_reset_complete",
    ),
    path("", views.landing, name="authenticate"),
    path("register", views.Registration, name="register"),
    path("registerStaff", views.registerStaff, name="registerStaff"),
    path("login/", views.Login, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path(
        "validate-username/",
        csrf_exempt(views.UsernameValidationView.as_view()),
        name="validate-username",
    ),
    path(
        "validate-email",
        csrf_exempt(views.EmailValidationView.as_view()),
        name="validate-email",
    ),
    path(
        "activate/<uidb64>/<token>/", views.VerificationView.as_view(), name="activate"
    ),
    path(
        "activate_staff/<uidb64>/<token>/",
        views.StaffVerificationView.as_view(),
        name="activate_staff",
    ),
    path("member_profile", views.member_profile, name="member_profile"),
    path("updateMemberProfile", views.updateMemberProfile, name="updateMemberProfile"),
]
