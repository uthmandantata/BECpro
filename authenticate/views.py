from django.shortcuts import render,redirect
from django.views import View
import json
from django.http import JsonResponse

from django.contrib import messages
from validate_email import validate_email 
from django.core.mail import EmailMessage
from django.conf import settings

from django.urls import reverse
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site

from .utils import token_generator

from django.contrib import auth

from . import models
from . import forms

# Create your views here.

class UsernameValidationView(View):
    def post(self, request):
        data=json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error':'Username should ONLY contain alphanumeric characters'},status=400)
        if models.CustomUser.objects.filter(username=username).exists():
            return JsonResponse({'username_error':'Username already in use, Choose another one!'},status=409)
        return JsonResponse({'username_valid': True})
    
class EmailValidationView(View):
    def post(self, request):
        data=json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error':'Email is invalid'},status=400)
        if models.CustomUser.objects.filter(email=email).exists():
            return JsonResponse({'email_error':'Email already in use, Choose another one!'},status=409)
        return JsonResponse({'email_valid': True})


def Registration(request):
    form = forms.SignupForm()
    
    
    if request.method == 'POST':
        username=request.POST['username']
        email_=request.POST['email']
        password=request.POST['password']
        if not models.CustomUser.objects.filter(username=username).exists():
            if not models.CustomUser.objects.filter(email=email_).exists():
                if len(password) < 6:
                    messages.error(request,'Password too short')
                    return render(request, 'authentication/register.html', context)
                registered_user = models.CustomUser.objects.create(username=username, email=email_)
                registered_user.set_password(password)
                registered_user.is_avtive = False
                registered_user.save()
            # path_to_view
            # - getting the domain we are on
            # - relative url to verification
            # - encode uid
            # - token
            uidb64 = urlsafe_base64_encode(force_bytes(registered_user.pk))
            
            domain=get_current_site(request).domain
            link=reverse('activate', kwargs={"uidb64":uidb64,"token":token_generator.make_token(registered_user)},)
            activate_url = f'http://{domain}{link}'
            email_subject = 'Activate your account'
            email_body = f'''Hi {registered_user.username}!
            Please use this link to verify your account
            {activate_url}'''
            email = EmailMessage(
                email_subject,
                email_body,
                settings.EMAIL_HOST_USER,
                [email_],   
            )
            email.send(fail_silently=False)
            messages.success(request,'Account succesfully created!')
            return redirect('membership_dashboard')
    context = {'form':form,'fieldValues':request.POST}
    
    return render(request, 'authentication/register.html',context)

class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id=force_str(urlsafe_base64_decode(uidb64))
            user=models.CustomUser.objects.get(id=id)
            if not token_generator.check_token(user,token):
                return redirect('login'+'?message='+'User already activated')
            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()
            messages.success(request, 'Account activated successfully')
            return redirect('login')

        except Exception as e:
            print(e)
        return redirect('login')
    

def Login(request):
    if request.method == "POST":
        username=request.POST['username']
        password=request.POST['password']

        if username and password:
            user=auth.authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, f'Welcome {user.username} you are now logged in')
                    return redirect('expenses')
                messages.error(request, f'Account is not active, please check your email')
                return render(request, 'authentication/login.html')
        messages.error(request, f'Welcome {user.username} you are now logged in')
    return render(request, 'authentication/login.html')
    


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You ahve been logged out')
        return redirect('login')