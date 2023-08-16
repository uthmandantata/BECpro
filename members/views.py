from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import ProfileForm,MemberRegistrationForm,MemberForm
from django.contrib.auth.decorators import login_required
from .models import Notification,Membership, PayHistory, Profile, Member
from accounts.models import Field
from authenticate.models import CustomUser

from django.contrib import messages
import json, requests 


from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token



from datetime import date
from dateutil.relativedelta import relativedelta



# Create your views here.

def password_reset_request(request):
    password_form = PasswordResetForm()
    if request.method == 'POST':
        password_form = PasswordResetForm(request.POST) 
        if password_form.is_valid():
            data = password_form.cleaned_data['email']
            user_email = CustomUser.objects.filter(Q(email=data))
            if user_email.exists():
                for user in user_email:
                    subject = 'Your forget password link'
                    email_template_name = 'accounts/password_message.txt'
                    email_from = settings.EMAIL_HOST_USER
                    parameters = {
                        'email':user.email,
                        'domain':'https://6e3d-154-120-73-228.ngrok-free.app',
                        'site_name': 'Focalleap',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token':default_token_generator.make_token(user),
                        'protocol': 'http',
                        }
                    email = render_to_string(email_template_name,parameters)
                    try:
                        send_mail(subject, email, email_from, [user.email], fail_silently=False)
                    except:
                        return HttpResponse('invalid header')
                    return redirect('password_reset_done')    
    context = {'password_form':password_form}
    return render(request, 'accounts/password_reset.html', context)

@login_required(login_url='login')
def profile(request):
    user = request.user
    first_name = user.first_name
    print(f"first_name: {first_name}")
    member = Member.objects.get(guardian_name=user.first_name)
    form = Profile.objects.get(user=user)
    if member.paid:
        notifications = Notification.objects.all()
        notification_count = Notification.objects.filter(is_read=False).count()
    
    context ={"user":user,"form":form,"notifications":notifications,"notification_count":notification_count}
    return render(request, 'accounts/members/profile.html', context)

@login_required(login_url='login')
def updateProfile(request):
    user = request.user
    member = Member.objects.get(guardian_name=user.first_name)
    profile = Profile.objects.get(user=user)
    form = ProfileForm(instance=profile)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            CustomUser.objects.update(
                first_name= profile.first_name
            )
            profile.save()
            if member.paid:
                member.email=profile.email,
                member.guardian_name=profile.first_name,
            return redirect('profile')
    if member.paid:
        notifications = Notification.objects.all()
        notification_count = Notification.objects.filter(is_read=False).count()
    context = {"form":form,"notifications":notifications,"notification_count":notification_count}
    return render(request, 'accounts/members/profile_form.html', context)

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        Profile.objects.create(
            user=user,
            email=user.email,
            )
        # login(request, user)
        return redirect('login')
    else:
        return HttpResponse('Activation link is invalid!')

def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
                received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')


# --------------    Member Dashboard       ------------------
@login_required(login_url='login')
def member_dashboard(request):
    user = request.user
    if request.user.is_admin == True:
        return redirect('home')
    status = Field.objects.all()
    user = request.user
    # username = request.user.username
    if user.is_member == False:
        return redirect("subscription")
    else:
        form = Member.objects.get(guardian_name=user.first_name)
        payment_history = PayHistory.objects.filter(user=user)[:3]
        paid = "Not Payed"
        if form.paid == True:
            paid = "Payed"
        membership_status = "Not Suspended"
        if form.suspend == True:
            membership_status = "Suspended"
        user = request.user
        if user.is_member:
            member = Member.objects.get(guardian_name=user.first_name)
            days_remaining = member.paid_until - member.date_paid
            
            if days_remaining == 0:
                Member.objects.update(
                paid=False,
                )
        if member.paid:
            notifications = Notification.objects.all()
            notification_count = Notification.objects.filter(is_read=False).count()
    context ={"notifications":notifications,"notification_count":notification_count,"membership_status":membership_status,"days_remaining":days_remaining,"status":status,"paid":paid,"payment_history":payment_history,"day1" : form.day1,"day2" : form.day2,"day3" : form.day3}
    return render(request, 'accounts/members/dashboard.html', context)
   
# --------------   End of Member Dashboard      ------------------

# --------------    Payment History       ------------------
@login_required(login_url='login')
def paymentHistory(request):
    user = request.user
    if user.is_member == False:
        return redirect("subscription")
    payment_history = PayHistory.objects.filter(user=user)
    if user.is_member:
        member = Member.objects.get(guardian_name=user.first_name)
        if member.paid:
            notifications = Notification.objects.all()
            notification_count = Notification.objects.filter(is_read=False).count()
    context ={"notifications":notifications,"notification_count":notification_count,"payment_history":payment_history}
        # return render(request, 'accounts/members/dashboard.html', context)
    return render(request, 'accounts/members/payment_history.html', context)

# --------------   End of Payment History       ------------------

# --------------    User Complaints       ------------------
@login_required(login_url='login')
def complaints(request):
    notifications = Notification.objects.all()
    notification_count = Notification.objects.filter(is_read=False).count()
    context ={"notifications":notifications,"notification_count":notification_count}
    return render(request, 'accounts/members/complaints.html', context)

# --------------   End of User Complaints       ------------------

# --------------    Notifications       ------------------
@login_required(login_url='login')
def notifications(request):
    notifications = Notification.objects.all()
    notification_count = Notification.objects.filter(is_read=False).count()
    context ={"notifications":notifications,"notification_count":notification_count}
    return render(request, 'accounts/members/notifications.html', context)

# --------------   End of Notifications       ------------------

# --------------   End of Payments      ------------------
def subscription(request):
    form = Membership.objects.all()
    context = {"form":form}
    return render(request, 'accounts/members/subscription.html', context)

def subscribe(request):
    username = request.user
    user = CustomUser.objects.get(email=username.email)
    plan = request.GET.get('membership_plan')
    fetch_memberhip = Membership.objects.filter(membership_type=plan).exists()
    if fetch_memberhip == False:
        return redirect(subscribe)
    membership = Membership.objects.get(membership_type=plan)
    price = float(membership.price*100)
    price = int(price)
    activity = membership.activity
    def init_payment(request):
        url = 'https://api.paystack.co/transaction/initialize'
        headers = {
            'Authorization':'Bearer '+'sk_test_088df86667579a1e72eeee77795861d7aae6e17f',
            'Content-Type':'application/json',
            'Accept':'application/json',
        }
        datum = {
            'email':request.user.email,
            'full_name': request.user.email,
            'amount': price
        }
        x = requests.post(url, data=json.dumps(datum), headers=headers)
        print(datum)
        # print(headers)
        if x.status_code != 200:
            return str(x.status_code)
        
        results = x.json()
        return results
    
    
    initialized = init_payment(request)
    print(initialized['data']['authorization_url'])
    amount = price/100
    # context = {'form':form}

    # member = Member.objects.get(guardian_name=username)
     
    # dtn = member.membership
    membership_duration = Membership.objects.get(membership_type=plan)
    duration = membership_duration.duration_in_months
    current_date = date.today()
    months  = 0
    expiry_date = current_date + relativedelta(months=int(duration))
    print(f'duration:{duration},months:{months}')
    

    print(user.is_member)
  
    if user.is_member == False:
        Member.objects.create(
            user=username,
            membership=membership,  
            guardian_name=request.user, 
            email=request.user.email, 
            activity=activity,
            date_paid=current_date,
            paid_until=expiry_date
        )

        CustomUser.objects.update(
            is_member = True
        )

    Member.objects.update(
        membership=membership, 
        activity=activity,
        paid=True,
        date_paid=current_date,
        paid_until=expiry_date
        )



    PayHistory.objects.create(
        amount=amount, 
        payment_for=membership, 
        user=request.user, 
        paystack_charge_id=initialized['data']['reference'], 
        paystack_access_code=initialized['data']['access_code'],
        activity=activity,
        expiry_date = expiry_date,
        is_verified=True,
        date_paid=current_date,
        )
    CustomUser.objects.update(
        is_member = True
        )
    
    
    link = initialized['data']['authorization_url']
    print(user.is_member)
    return HttpResponseRedirect(link)
    return render(request, 'accounts/members/subscribe.html')

def call_back_url(request):
    reference = request.GET.get('reference_code')
    check_pay = PayHistory.objects.filter(paystack_charge_id=reference).exists()
    if check_pay == False:
        print("Error")
    else:
        payment = PayHistory.objects.get(paystack_charge_id=reference)
        member = payment.user

        #fetch to make sure payment was successful
        def verify_payment(request):
            url = 'https://api.paystack.co/transaction/verify'
            headers = {
                'Authorization':'Bearer '+settings.PAYSTACK_SECRET_KEY,
                'Content-Type':'application/json',
                'Accept':'application/json',
            }
            datum = {
                'reference': check_pay.paystack_charge_id
            }
            print('help')
            x = requests.post(url, data=json.dumps(datum), headers=headers)
            print(datum)
            # print(headers)
            if x.status_code != 200:
                return str(x.status_code)
            
            results = x.json()
            
            return results
    initialized = verify_payment(request)
    

   
    print(f"verified:{initialized['data']['authorization_url']}")
    return render(request, 'accounts/members/payment.html')
# --------------   End of payments      ------------------  

@login_required(login_url='login')
def members_details(request):
    
    user = request.user
    # username = request.user.username

    if user.is_member == False:
        return redirect("subscription")
    
    form = Member.objects.get(guardian_name=user.first_name)
    membership = str(form.membership)
    
    print(f"membership:{membership}")
    fm = membership.split()
    first = fm[0]
    

    if user.is_member == False:
        return redirect(subscription)
    
    stat = ""
    
    if first == "Family":
        stat = "Family"
    else:
        stat = "Single"
    if form.paid:
        notifications = Notification.objects.all()
        notification_count = Notification.objects.filter(is_read=False).count()
    context ={"notifications":notifications,"notification_count":notification_count,"user":user,"form":form,"stat":stat,"membership":membership}
    return render(request, 'accounts/members/membership_details.html', context)

@login_required(login_url='login')
def updateMembersDetails(request,pk):
    user = request.user
    username = request.user.username
    form = Member.objects.get(guardian_name=user.first_name)
    member = Member.objects.get(guardian_name=user.first_name)
    members = Member.objects.get(id=pk)
    membership = str(members.membership)
    fm = membership.split()
    first = fm[0]
    stat = ""
    if first == "Family":
        stat = "Family"
        form = MemberRegistrationForm(instance=members)
        if request.method == "POST":
            form = MemberRegistrationForm(request.POST, instance=members)
            if form.is_valid():
                form.save()
                return redirect('profile')
    else:
        stat = "Single"
        form = MemberForm(instance=members)
        if request.method == "POST":
            form = MemberForm(request.POST, instance=members)
            if form.is_valid():
                form.save()
                return redirect('profile')
    if member.paid:
        notifications = Notification.objects.all()
        notification_count = Notification.objects.filter(is_read=False).count()
    context ={"notifications":notifications,"notification_count":notification_count,"form":form,"stat":stat}
    return render(request, 'accounts/members/member_detail_form.html', context)
    
# --------------   End of Members      ------------------


