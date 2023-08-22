from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    
    path('', views.Registration, name='authenticate'),
    path('registerStaff', views.registerStaff, name='registerStaff'),
    path('login/', views.Login, name='login'),
    path('logout/', views.logoutUser , name='logout'),
    path('validate-username/', csrf_exempt(views.UsernameValidationView.as_view()), name='validate-username'),
    path('validate-email', csrf_exempt(views.EmailValidationView.as_view()), name='validate-email'),
    path('activate/<uidb64>/<token>/', views.VerificationView.as_view(), name='activate'),
    path('activate_staff/<uidb64>/<token>/', views.StaffVerificationView.as_view(), name='activate_staff'),
    path('profile', views.profile, name='profile'),
    path('updateProfile', views.updateProfile, name='updateProfile'),
]
