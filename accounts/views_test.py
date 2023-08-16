from django.shortcuts import render, redirect
from .forms import MemberForm, ProfileForm, SignupForm, MemberRegistrationForm, EquipmentForm,HorsesForm, CustomUserForm, SlotsForm, MembershipForm, ServicesForm, TicketsForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Field,Notification, Day1,Day2,Day3, Member, Horses, Equipment, CustomUser, Slots,Membership, PayHistory, Services, Tickets, Profile
from django.core.exceptions import ValidationError
from django.contrib import messages
# import date
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
from django.db.models import Sum


        
     


def landing(request):
    context = {}
    return render(request, 'accounts/admin2/landing.html', context)

@login_required(login_url='login')
def home(request):
    try:
        if request.user.is_admin==False:
            return redirect('member_dashboard')
        no_members = Member.objects.all().count()
        membership = Membership.objects.all()
        try:
            polo_payment_sum = PayHistory.objects.filter(activity="Polo").aggregate(Sum('amount'))['amount__sum']
            riding_payment_sum = PayHistory.objects.filter(activity="Riding").aggregate(Sum('amount'))['amount__sum']
        except PayHistory.DoesNotExist:
            polo_payment_sum = 0
            riding_payment_sum = 0
        try:
            polo_count = Member.objects.filter(activity="Polo").count()
            riding_count = Member.objects.filter(activity="Riding").count()
        except Member.DoesNotExist:
            polo_payment_sum = 0
            riding_payment_sum = 0
    except Exception as e:
        print(e)
        return e
    context = {"riding_count":riding_count,"polo_count":polo_count,"membership":membership,"no_members":no_members,"polo_payment_sum":polo_payment_sum,"riding_payment_sum":riding_payment_sum}
    return render(request, 'accounts/admin2/index.html', context)

@login_required(login_url='login')
def staff(request):
    try:
        if request.user.is_admin==False:
            return redirect('member_dashboard')
        elif request.user.is_admin != True:
            return redirect('member_dashboard')
    except Exception as e:
        print(e)
        return e
    context = {}
    return render(request, 'accounts/admin2/staff.html', context)

# --------------    Horses      ------------------

@login_required(login_url='login')
def horses(request):
    try:
        if request.user.is_admin==False:
            return redirect('member_dashboard')
        elif request.user.is_admin != True:
            return redirect('member_dashboard')
        form = Horses.objects.all()
    except Exception as e:
        print(e)
        return e
    context = {'form':form}
    return render(request, 'accounts/admin2/horses.html', context)

@login_required(login_url='login')
def addHorses(request):
    try:
        if request.user.is_admin==False:
            return redirect('member_dashboard')
        elif request.user.is_admin != True:
            return redirect('member_dashboard')
        form = HorsesForm()
        if request.method == 'POST':
            form = HorsesForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('horses')
    except Exception as e:
        print(e)
        return e
    context = {"form":form}
    return render(request, 'accounts/admin2/horses_form.html', context)

@login_required(login_url='login')
def updateHorses(request,pk):
    try:
        if request.user.is_admin==False:
            return redirect('member_dashboard')
        elif request.user.is_admin != True:
            return redirect('member_dashboard')
        horses = Horses.objects.get(id=pk)
        form = HorsesForm(instance=horses)
        if request.method == "POST":
            form = HorsesForm(request.POST, instance=horses)
            if form.is_valid():
                form.save()
                return redirect('horses')
    except Exception as e:
        print(e)
        return e
    context = {"form":form}
    return render(request, 'accounts/admin2/horses_form.html', context)

@login_required(login_url='login')
def removeHorses(request,pk):
    try:
        if request.user.is_admin==False:
            return redirect('member_dashboard')
        elif request.user.is_admin != True:
            return redirect('member_dashboard')
        horses = Horses.objects.get(id=pk)
        if request.method == "POST":
            horses.delete()
            return redirect('horses')
    except Exception as e:
        print(e)
    return render(request, 'accounts/admin2/delete.html', {'obj':horses})

# --------------   End of Horses      ------------------


# --------------    Admin members      ------------------

@login_required(login_url='login')
def members(request):
    try:
        if request.user.is_admin==False:
            return redirect('member_dashboard')
        elif request.user.is_admin != True:
            return redirect('member_dashboard')
        form = Member.objects.all()
    except Exception as e:
        print(e)
    context = {'form':form}
    return render(request, 'accounts/admin2/members.html', context)

@login_required(login_url='login')
def addMembers(request):
    try:
        if request.user.is_admin==False:
            return redirect('member_dashboard')
        form = HorsesForm()
        if request.method == 'POST':
            form = HorsesForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('horses')
    except Exception as e:
        print(e)
    context = {"form":form}
    return render(request, 'accounts/admin2/horses_form.html', context)

@login_required(login_url='login')
def updateMembers(request,pk):
    try:
        if request.user.is_admin==False:
            return redirect('member_dashboard')
        elif request.user.is_admin != True:
            return redirect('member_dashboard')
        horses = Horses.objects.get(id=pk)
        form = HorsesForm(instance=horses)
        if request.method == "POST":
            form = HorsesForm(request.POST, instance=horses)
            if form.is_valid():
                form.save()
                return redirect('horses')
    except Exception as e:
        print(e)
    context = {"form":form}
    return render(request, 'accounts/admin2/horses_form.html', context)


@login_required(login_url='login')
def suspendMembers(request,pk):
    if request.user.is_member:
        return redirect('member_dashboard')
    members = Member.objects.get(id=pk)
    # form = SuspendForm(instance=members)
    if request.method == "POST":
        Member.objects.update(
            suspend=True
        )
        return redirect('members')
    context = {"form":members,"members":members}
    return render(request, 'accounts/admin2/suspend.html', context)

@login_required(login_url='login')
def resumeMembers(request,pk):
    if request.user.is_member:
        return redirect('member_dashboard')
    members = Member.objects.get(id=pk)
    # form = SuspendForm(instance=members)
    if request.method == "POST":
        Member.objects.update(
            suspend=False
        )
        return redirect('members')
    context = {"form":members,"members":members}
    return render(request, 'accounts/admin2/suspend.html', context)
    
    



# --------------   End of Admin members      ------------------

# --------------    Services      ------------------

@login_required(login_url='login')
def services(request):
    try:
        if request.user.is_admin==False:
            return redirect('member_dashboard')
        elif request.user.is_admin != True:
            return redirect('member_dashboard')
        form = Services.objects.all()
    except Exception as e:
        print(e)
    context = {'form':form}
    return render(request, 'accounts/admin2/services.html', context)

@login_required(login_url='login')
def addServices(request):
    try:
        if request.user.is_admin==False:
            return redirect('member_dashboard')
        elif request.user.is_admin != True:
            return redirect('member_dashboard')
        form = ServicesForm()
        if request.method == 'POST':
            form = ServicesForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('services')
    except Exception as e:
        print(e)
    context = {"form":form}
    return render(request, 'accounts/admin2/service_form.html', context)

@login_required(login_url='login')
def updateServices(request,pk):
    try:
        if request.user.is_admin==False:
            return redirect('member_dashboard')
        elif request.user.is_admin != True:
            return redirect('member_dashboard')
        services = Services.objects.get(id=pk)
        form = ServicesForm(instance=services)
        if request.method == "POST":
            form = ServicesForm(request.POST, instance=services)
            if form.is_valid():
                form.save()
                return redirect('services')
    except Exception as e:
        print(e)
    context = {"form":form}
    return render(request, 'accounts/admin2/service_form.html', context)

@login_required(login_url='login')
def removeServices(request,pk):
    try:
        if request.user.is_admin==False:
            return redirect('member_dashboard')
        elif request.user.is_admin != True:
            return redirect('member_dashboard')
        services = Services.objects.get(id=pk)
        if request.method == "POST":
            services.delete()
            return redirect('services')
    except Exception as e:
        print(e)
    return render(request, 'accounts/admin2/delete.html', {'obj':services})

# --------------   End of Services      ------------------

# --------------    Tickets      ------------------

@login_required(login_url='login')
def tickets(request):
    try:
        if request.user.is_admin==False:
            return redirect('member_dashboard')
        elif request.user.is_admin != True:
            return redirect('member_dashboard')
        form = Tickets.objects.all()
        # price = Tickets.objects.all()
    except Exception as e:
        print(e)
    context = {'form':form}
    return render(request, 'accounts/admin2/tickets.html', context)

@login_required(login_url='login')
def test(request):
    if request.user.is_member:
        return redirect('member_dashboard')
    today = date.today()
    print("Today's date:", today)
    return render(request, 'accounts/admin2/test.html',{'today':today})

@login_required(login_url='login')
def addTickets(request):
    try:
        if request.user.is_admin==False:
            return redirect('member_dashboard')
        elif request.user.is_admin != True:
            return redirect('member_dashboard')
        form = TicketsForm()
        if request.method == 'POST':
            form = TicketsForm(request.POST)
            user = request.user.username
            service = request.POST.get('service')
            services = Services.objects.get(id=service)
            print(services,user)
            quantity = request.POST.get('quantity')
            price = services.price
            total = quantity * price
            if form.is_valid():
                form.save()
                return redirect('tickets')
    except Exception as e:
        print(e)
    context = {"form":form}
    return render(request, 'accounts/admin2/tickets_form.html', context)

@login_required(login_url='login')
def updateTickets(request,pk):
    try:
        if request.user.is_admin==False:
            return redirect('member_dashboard')
        elif request.user.is_admin != True:
            return redirect('member_dashboard')
        tickets = Tickets.objects.get(id=pk)
        form = TicketsForm(instance=tickets)
        if request.method == "POST":
            form = TicketsForm(request.POST, instance=tickets)
            if form.is_valid():
                form.save()
                return redirect('tickets')
    except Exception as e:
        print(e)
    context = {"form":form}
    return render(request, 'accounts/admin2/tickets_form.html', context)

@login_required(login_url='login')
def removeTickets(request,pk):
    try:
        if request.user.is_admin==False:
            return redirect('member_dashboard')
        elif request.user.is_admin != True:
            return redirect('member_dashboard')
        tickets = Tickets.objects.get(id=pk)
        if request.method == "POST":
            tickets.delete()
            return redirect('tickets')
    except Exception as e:
        print(e)
    return render(request, 'accounts/admin2/delete.html', {'obj':tickets})

# --------------   End of Tickets      ------------------

# --------------    Equipment      ------------------
@login_required(login_url='login')
def equipment(request):
    try:
        if request.user.is_admin==False:
            return redirect('member_dashboard')
        elif request.user.is_admin != True:
            return redirect('member_dashboard')
        forms = Equipment.objects.all()
    except Exception as e:
        print(e)
    context = {"forms":forms}
    return render(request, 'accounts/admin2/equipment.html', context)

@login_required(login_url='login')
def addEquipment(request):
    if request.user.is_member:
        return redirect('member_dashboard')
    form = EquipmentForm()
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('equipment')
    context = {"form":form}
    return render(request, 'accounts/admin2/equipment_form.html', context)

@login_required(login_url='login')
def updateEquipment(request,pk):
    equipment = Equipment.objects.get(id=pk)
    form = EquipmentForm(instance=equipment)
    if request.method == "POST":
        form = EquipmentForm(request.POST, instance=equipment)
        if form.is_valid():
            form.save()
            return redirect('equipment')
    context = {"form":form}
    return render(request, 'accounts/admin2/equipment_form.html', context)

@login_required(login_url='login')
def removeEquipment(request,pk):
    equipment = Equipment.objects.get(id=pk)

    if request.method == "POST":
        equipment.delete()
        return redirect('equipment')
    
    return render(request, 'accounts/admin2/delete.html', {'obj':equipment})

# --------------   End of Equipment      ------------------

# --------------    Users      ------------------
@login_required(login_url='login')
def costumUser(request):
    form = CustomUser.objects.all()
    context = {'form':form}
    return render(request, 'accounts/admin2/costumUser.html', context)

@login_required(login_url='login')
def updateCostumUser(request,pk):

    costumUser = CustomUser.objects.get(id=pk)
    form = CustomUserForm(instance=costumUser)

    if request.user.is_member == True:
        return HttpResponse('You are not allowed here!!')
    elif request.user != costumUser.username:
        return HttpResponse('You are not allowed here!!')


    if request.method == "POST":
        form = CustomUserForm(request.POST, instance=costumUser)
        if form.is_valid():
            form.save()
            return redirect('costumUser')
    context = {"form":form}
    return render(request, 'accounts/admin2/costumUser_form.html', context)
# --------------   End of Users      ------------------

# --------------    Slots      ------------------

@login_required(login_url='login')
def slots(request):
    form = Slots.objects.all()
    context = {'form':form}
    return render(request, 'accounts/admin2/slots.html', context)

@login_required(login_url='login')
def addSlots(request):
    form = SlotsForm()
    if request.method == 'POST':
        form = SlotsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('slots')
    context = {"form":form}
    return render(request, 'accounts/admin2/slots_form.html', context)

@login_required(login_url='login')
def updateSlots(request,pk):
    slots = Slots.objects.get(id=pk)
    form = SlotsForm(instance=slots)
    if request.method == "POST":
        form = SlotsForm(request.POST, instance=slots)
        if form.is_valid():
            form.save()
            return redirect('slots')
    context = {"form":form}
    return render(request, 'accounts/admin2/slots_form.html', context)

@login_required(login_url='login')
def removeSlots(request,pk):
    slots = Slots.objects.get(id=pk)

    if request.method == "POST":
        slots.delete()
        return redirect('slots')
    
    return render(request, 'accounts/admin2/delete.html', {'obj':slots})

# --------------   End of Slots      ------------------

# --------------   Members Application      ------------------

def loginUser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome {username}!')
            if user.is_allowed:
                return redirect('member_dashboard')
            return redirect('home')        
        else:
            messages.error(request, 'Username or Passowrd DOES NOT exist')
        return redirect('login')
    context = {}
    return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

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

def registerUser(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.is_allowed = True
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('accounts/members/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'accounts/members/register.html', {'form': form})

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