from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import (
    MemberRegistrationForm,
    MemberForm,
    ridingMemberForm,
    familyRidingMemberForm,
)


from django.contrib.auth.decorators import login_required
from .models import PayHistory, Member, Membership, Days
from staff.models import Field, Notification
from authenticate.models import CustomUser, Profile

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
    if request.method == "POST":
        password_form = PasswordResetForm(request.POST)
        if password_form.is_valid():
            data = password_form.cleaned_data["email"]
            user_email = CustomUser.objects.filter(Q(email=data))
            if user_email.exists():
                for user in user_email:
                    subject = "Your forget password link"
                    email_template_name = "password_message.txt"
                    email_from = settings.EMAIL_HOST_USER
                    parameters = {
                        "email": user.email,
                        "domain": "https://4ffe-197-157-218-200.ngrok-free.app",
                        "domain": "https://17d3-197-157-218-195.ngrok-free.app",
                        "site_name": "Focalleap",
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "token": default_token_generator.make_token(user),
                        "protocol": "http",
                    }
                    email = render_to_string(email_template_name, parameters)
                    try:
                        send_mail(
                            subject,
                            email,
                            email_from,
                            [user.email],
                            fail_silently=False,
                        )
                    except:
                        return HttpResponse("invalid header")
                    return redirect("password_reset_done")
    context = {"password_form": password_form}
    return render(request, "password_reset.html", context)


# --------------    User Complaints       ------------------
@login_required(login_url="login")
def complaints(request):
    if request.user.is_staff:
        return redirect("staff")
    notifications = Notification.objects.all()
    notification_count = Notification.objects.filter(is_read=False).count()
    context = {"notifications": notifications, "notification_count": notification_count}
    return render(request, "members/complaints.html", context)


# --------------   End of User Complaints       ------------------


# --------------    Notifications       ------------------
@login_required(login_url="login")
def notifications(request):
    if request.user.is_staff:
        return redirect("home")
    notifications = Notification.objects.all()
    notification_count = Notification.objects.filter(is_read=False).count()

    context = {"notifications": notifications, "notification_count": notification_count}
    return render(request, "members/rest/notifications.html", context)


@login_required(login_url="login")
def viewNotifications(request, pk):
    notifications = Notification.objects.get(pk=pk)
    if request.user.is_staff:
        return redirect("home")

    notifications = Notification.objects.get(pk=pk)
    notifications.is_read = True
    notifications.save()
    notification_count = Notification.objects.filter(is_read=False).count()
    context = {"notifications": notifications, "notification_count": notification_count}
    return render(request, "members/rest/view_notifications.html", context)


# --------------   End of Notifications       ------------------


# --------------   End of Payments      ------------------
@login_required(login_url="login")
def subscription(request):
    # form = Membership.objects.all()
    # print(f"form: {form}")
    # context = {"form":form}
    # return render(request, 'members/rest/subscription.html', context)
    if request.user.is_staff:
        return redirect("home")
    form = Membership.objects.all()
    print(f"form: {form}")
    context = {"form": form}
    return render(request, "members/rest/subscription.html", context)


@login_required(login_url="login")
def subscribe(request):
    username = request.user
    user = CustomUser.objects.get(email=username.email)
    plan = request.GET.get("membership_plan")
    fetch_memberhip = Membership.objects.filter(membership_type=plan).exists()
    if fetch_memberhip == False:
        return redirect(subscribe)
    membership = Membership.objects.get(membership_type=plan)
    price = float(membership.price * 100)
    price = int(price)
    activity = membership.activity

    def init_payment(request):
        url = "https://api.paystack.co/transaction/initialize"
        headers = {
            "Authorization": "Bearer "
            + "sk_test_088df86667579a1e72eeee77795861d7aae6e17f",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        datum = {
            "email": request.user.email,
            "full_name": request.user.email,
            "amount": price,
        }
        x = requests.post(url, data=json.dumps(datum), headers=headers)
        print(datum)
        if x.status_code != 200:
            return str(x.status_code)

        results = x.json()
        return results

    initialized = init_payment(request)
    print(initialized["data"]["authorization_url"])
    amount = price / 100
    membership_duration = Membership.objects.get(membership_type=plan)
    duration = membership_duration.duration_in_months
    current_date = date.today()
    months = 0
    expiry_date = current_date + relativedelta(months=int(duration))
    print(f"duration:{duration},months:{months}")
    months = 0
    expiry_date = current_date + relativedelta(months=int(duration))
    full_name = request.user.first_name + " " + request.user.last_name

    print(f"full_name: {full_name}")

    if user.is_member == False:
        Member.objects.create(
            user=username,
            membership=membership,
            guardian_name=full_name,
            email=request.user.email,
            activity=activity,
            date_paid=current_date,
            paid_until=expiry_date,
        )

        CustomUser.objects.update(is_member=True)

    Member.objects.update(
        guardian_name=full_name,
        membership=membership,
        activity=activity,
        paid=True,
        date_paid=current_date,
        paid_until=expiry_date,
    )

    CustomUser.objects.update(is_member=True, is_allowed=True)

    PayHistory.objects.create(
        amount=amount,
        payment_for=membership,
        user=request.user,
        paystack_charge_id=initialized["data"]["reference"],
        paystack_access_code=initialized["data"]["access_code"],
        activity=activity,
        expiry_date=expiry_date,
        is_verified=True,
        date_paid=current_date,
    )

    link = initialized["data"]["authorization_url"]
    print(user.is_member)
    return HttpResponseRedirect(link)


# return render(request, "members/rest/subscribe.html")


@login_required(login_url="login")
def call_back_url(request):
    reference = request.GET.get("reference_code")
    check_pay = PayHistory.objects.filter(paystack_charge_id=reference).exists()
    if check_pay == False:
        print("Error")
        return HttpResponse("Fuck of")

    payment = PayHistory.objects.get(paystack_charge_id=reference)
    member = Member.objects.get(user=payment.user)
    membership_duration = Membership.objects.get(membership_type=payment.payment_for)
    duration = membership_duration.duration_in_months
    current_date = date.today()

    def verify_payment(request):
        url = "https://api.paystack.co/transaction/verify"
        headers = {
            "Authorization": "Bearer " + settings.PAYSTACK_SECRET_KEY,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        datum = {"reference": check_pay.paystack_charge_id}
        x = requests.post(url, data=json.dumps(datum), headers=headers)
        print(datum)
        if x.status_code != 200:
            return str(x.status_code)
        results = x.json()
        return results

    initialized = verify_payment(request)

    print(f"verified:{initialized['data']['authorization_url']}")
    return render(request, "members/payment.html")


# --------------   End of payments      ------------------


# --------------   End of Members      ------------------


@login_required(login_url="login")
def change_subscription(request):
    form = Membership.objects.all()
    member = Member.objects.get(user=request.user)
    my_membership = member.membership

    context = {"form": form, "member": member, "my_membership": my_membership}
    return render(request, "members/billing/change_subscription.html", context)


@login_required(login_url="login")
def billing_history(request):
    user = request.user
    if request.user.is_staff:
        return redirect("home")
    if user.is_member == False:
        return redirect("subscription")
    payment_history = PayHistory.objects.filter(user=user).order_by("-date_created")
    if user.is_member:
        member = Member.objects.get(user=user)
        if member.paid:
            notifications = Notification.objects.all()
            notification_count = Notification.objects.filter(is_read=False).count()
    context = {
        "notifications": notifications,
        "notification_count": notification_count,
        "payment_history": payment_history,
    }
    # return render(request, 'members/dashboard.html', context)
    return render(request, "members/billing/billing_history.html", context)


@login_required(login_url="login")
def subscription_guide(request):
    if request.user.is_staff:
        return redirect("home")
    context = {}
    return render(request, "members/rest/subscription_guide.html", context)


@login_required(login_url="login")
def errors(request):
    context = {}
    return render(request, "error_page.html", context)


# --------------    Member Dashboard       ------------------


@login_required(login_url="login")
def member_dashboard(request):
    user = request.user
    if request.user.is_staff:
        return redirect("home")
    if request.user.is_admin == True:
        return redirect("home")
    status = Field.objects.all()
    if user.is_member == False:
        return redirect("subscription")
    else:
        form = Member.objects.get(user=user)

        profile = Profile.objects.get(user=user)
        activity_status = form.activity
        days = form.days.all()
        payment_history = PayHistory.objects.filter(user=user).order_by(
            "-date_created"
        )[:3]
        paid = "Not Payed"
        if form.paid == True:
            paid = "Payed"
        membership_status = "Not Suspended"
        if form.suspend == True:
            membership_status = "Suspended"
        user = request.user
        if user.is_member:
            member = Member.objects.get(user=user)
            days_remaining = member.paid_until - member.date_paid

            if days_remaining == 0:
                member.paid = False
                member.save()

        if member.paid:
            notifications = Notification.objects.all()
            notification_count = Notification.objects.filter(is_read=False).count()

        today = date.today().strftime("%A")
        permis = ""
        if today == "Wednesday" or today == "Saturday" or today == "Sunday":
            if activity_status == "Riding":
                permis = "No Riding Today"
            elif activity_status == "Polo":
                permis = "Polo open Today"
        else:
            if activity_status == "Riding":
                permis = " Riding open Today"
            elif activity_status == "Polo":
                permis = "No Polo Today"

        context = {
            "activity_status": activity_status,
            "permis": permis,
            "today": today,
            "notifications": notifications,
            "notification_count": notification_count,
            "membership_status": membership_status,
            "days_remaining": days_remaining.days,
            "status": status,
            "paid": paid,
            "payment_history": payment_history,
            "days": days,
            "form": form,
            "profile": profile,
        }
    return render(request, "members/dashboard/dashboard.html", context)


# --------------   End of Member Dashboard      ------------------
@login_required(login_url="login")
def members_details(request):
    user = request.user
    if request.user.is_staff:
        return redirect("home")
    notifications = None
    notification_count = None
    if user.is_member == False:
        return redirect("subscription")

    form = Member.objects.get(user=user)
    profile = Profile.objects.get(user=user)
    days = form.days.all()
    membership = str(form.membership)
    payment_history = PayHistory.objects.filter(user=user).order_by("-date_created")[:4]
    fm = membership.split()
    first = fm[0]
    membership_status = "Not Suspended"
    if form.suspend == True:
        membership_status = "Suspended"
        return redirect("member_dashboar")
    # Change the

    time_remaining = form.paid_until - form.date_paid
    days_remaining = time_remaining.days
    print(days_remaining)

    if int(days_remaining) <= 0:
        return redirect("member_dashboard")

    if user.is_member == False:
        return redirect("subscription")
    stat = ""
    if first == "Family":
        stat = "Family"
    else:
        stat = "Single"
    if form.paid:
        notifications = Notification.objects.all()
        notification_count = Notification.objects.filter(is_read=False).count()
    context = {
        "notifications": notifications,
        "notification_count": notification_count,
        "user": user,
        "form": form,
        "stat": stat,
        "membership": membership,
        "days": days,
        "payment_history": payment_history,
        "membership_status": membership_status,
        "profile": profile,
    }
    return render(request, "members/membership/membership_details.html", context)


@login_required(login_url="login")
def updateMembersDetails(request):
    if request.user.is_staff:
        return redirect("home")
    user = request.user
    if user.is_member == False:
        return redirect("subscribe")

    member = Member.objects.get(user=user)

    time_remaining = member.paid_until - member.date_paid
    days_remaining = time_remaining.days
    print(days_remaining)

    if int(days_remaining) <= 0:
        return redirect("member_dashboard")

    activity = member.activity
    membership = str(member.membership)
    days = Days.objects.all()

    fm = membership.split()
    first = fm[0]

    form_one = MemberForm(instance=member)
    form_alot = MemberRegistrationForm(instance=member)
    single_riding_form = ridingMemberForm(instance=member)
    family_riding_form = familyRidingMemberForm(instance=member)
    days_selected = member.days.all()
    print(days_selected)

    if request.method == "POST":
        if first == "Family":
            if activity == "Riding":
                family_riding_form = familyRidingMemberForm(
                    request.POST, instance=member
                )
                if family_riding_form.is_valid():
                    family_riding_form.save()
                    return redirect("members-details")
                elif activity == "Polo":
                    form_alot = MemberRegistrationForm(request.POST, instance=member)
                    days_selected = member.days
                    if form_alot.is_valid():
                        chosen_days_ids = request.POST.getlist("days")
                        chosen_days = Days.objects.filter(id__in=chosen_days_ids)

                        update_member = form_alot.save(commit=False)
                        print(
                            f"""chosen_days_ids: {chosen_days_ids}
    chosen_days: {chosen_days}"""
                        )
                        update_member.days.clear()
                        update_member.days.add(*chosen_days)
                        update_member.save()
                        return redirect("members-details")
        elif first == "Single":
            if activity == "Riding":
                single_riding_form = ridingMemberForm(request.POST, instance=member)
                if single_riding_form.is_valid():
                    single_riding_form.save()
                    return redirect("members-details")
            elif activity == "Polo":
                form_one = MemberForm(request.POST, instance=member)
                days_selected = member.days
                if form_one.is_valid():
                    chosen_days_ids = request.POST.getlist("days")
                    chosen_days = Days.objects.filter(id__in=chosen_days_ids)

                    update_member = form_alot.save(commit=False)
                    print(
                        f"""chosen_days_ids: {chosen_days_ids}
chosen_days: {chosen_days}"""
                    )
                    update_member.days.clear()
                    update_member.days.add(*chosen_days)
                    update_member.save()
                    return redirect("members-details")

    context = {
        "activity": activity,
        "form_alot": form_alot,
        "form_one": form_one,
        "first": first,
        "days": days,
        "days_selected": days_selected,
    }
    return render(request, "members/membership/member_details_form.html", context)
