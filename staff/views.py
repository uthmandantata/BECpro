from django.shortcuts import render, redirect
from .forms import (
    EquipmentForm,
    HorsesForm,
    CustomUserForm,
  
    ServicesForm,
    TicketsForm,
    NotificationForm,
)
from django.contrib.auth.decorators import login_required
from .models import Horses, Equipment, Services, Tickets, Notification
from members import models as mem_models
from members import forms as mem_forms
from authenticate import models as auth_models
import random
from authenticate import views as auth_views
from django.http import HttpResponse
from decimal import Decimal
from django.contrib import messages
from django.views import View
from authenticate.models import CustomUser
from datetime import date
from django.db.models import Sum


@login_required(login_url="login")
def home(request):
    if request.user.is_member == True:
        auth_views.logoutUser(request)
        return HttpResponse("You are not allowed here. You have been logged out.")
    members = mem_models.Member.objects.all()
    member_revenue = 0
    payment = mem_models.PayHistory.objects.all()[:5]
    equipment = Equipment.objects.all()[:5]
    horses = Horses.objects.all()[:5]
    tickets = Tickets.objects.all()[:5]
    profile = auth_models.Profile.objects.get(user=request.user)
    no_members = members.count()
    membership = mem_models.Membership.objects.all()
    polo_payment_sum = 0
    riding_payment_sum = 0
    member_revenue = 0

    try:
        if payment.count() > 0:
            polo_payment_sum = mem_models.PayHistory.objects.filter(
                activity="Polo"
            ).aggregate(Sum("amount"))["amount__sum"]
            riding_payment_sum = mem_models.PayHistory.objects.filter(
                activity="Riding"
            ).aggregate(Sum("amount"))["amount__sum"]
            polo_payment_sum = polo_payment_sum or Decimal("0")
            riding_payment_sum = riding_payment_sum or Decimal("0")
            member_revenue = polo_payment_sum + riding_payment_sum

        member_revenue = polo_payment_sum + riding_payment_sum
    except mem_models.PayHistory.DoesNotExist:
        polo_payment_sum = 0
        riding_payment_sum = 0
    try:
        polo_count = mem_models.Member.objects.filter(activity="Polo").count()
        riding_count = mem_models.Member.objects.filter(activity="Riding").count()
    except mem_models.Member.DoesNotExist:
        polo_payment_sum = 0
        riding_payment_sum = 0

    context = {
        "member_revenue": member_revenue,
        "profile": profile,
        "tickets": tickets,
        "horses": horses,
        "payment": payment,
        "members": members,
        "riding_count": riding_count,
        "polo_count": polo_count,
        "membership": membership,
        "no_members": no_members,
        "polo_payment_sum": polo_payment_sum,
        "riding_payment_sum": riding_payment_sum,
    }
    return render(request, "staff/dashboard/dashboard.html", context)


@login_required(login_url="login")
def staff(request):
    try:
        if request.user.is_admin == False:
            return redirect("member_dashboard")
        elif request.user.is_admin != True:
            return redirect("member_dashboard")
    except Exception as e:
        print(e)
        return e
    context = {}
    return render(request, "staff/dashboard/dashboard.html", context)


# --------------    Horses      ------------------


@login_required(login_url="login")
def horses(request):
    try:
        if request.user.is_member:
            return redirect("member_dashboard")
        horses = Horses.objects.all()
    except Exception as e:
        print(e)
        return e
    context = {"horses": horses}
    return render(request, "staff/inventory/horses.html", context)


@login_required(login_url="login")
def addHorses(request):
    try:
        if request.user.is_member:
            return redirect("member_dashboard")
        form = HorsesForm()
        if request.method == "POST":
            form = HorsesForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("horses")
    except Exception as e:
        print(e)
        return e
    context = {"form": form}
    return render(request, "staff/inventory/horses_form.html", context)


@login_required(login_url="login")
def updateHorses(request, pk):
    try:
        if request.user.is_member:
            return redirect("member_dashboard")
        horses = Horses.objects.get(id=pk)
        form = HorsesForm(instance=horses)
        if request.method == "POST":
            form = HorsesForm(request.POST, instance=horses)
            if form.is_valid():
                form.save()
                return redirect("horses")
    except Exception as e:
        print(e)
    context = {"form": form}
    return render(request, "staff/inventory/horses_form.html", context)


@login_required(login_url="login")
def removeHorses(request, pk):
    try:
        if request.user.is_member:
            return redirect("member_dashboard")
        horses = Horses.objects.get(id=pk)
        if request.method == "POST":
            horses.delete()
            return redirect("horses")
    except Exception as e:
        print(e)
    return render(request, "staff/delete.html", {"obj": horses})


# --------------   End of Horses      ------------------


# --------------    Admin members      ------------------


@login_required(login_url="login")
def staff_members(request):
    try:
        if request.user.is_member == True:
            return redirect("member_dashboard")

        member = mem_models.Member.objects.all()
    except Exception as e:
        print(e)
    context = {"member": member}
    return render(request, "staff/members/members.html", context)


@login_required(login_url="login")
def addMembers(request):
    try:
        if request.user.is_admin == False:
            return redirect("member_dashboard")
        form = HorsesForm()
        if request.method == "POST":
            form = HorsesForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("horses")
    except Exception as e:
        print(e)
    context = {"form": form}
    return render(request, "accounts/admin2/horses_form.html", context)


@login_required(login_url="login")
def updateMembers(request, pk):
    try:
        if request.user.is_admin == False:
            return redirect("member_dashboard")
        elif request.user.is_admin != True:
            return redirect("member_dashboard")
        horses = Horses.objects.get(id=pk)
        form = HorsesForm(instance=horses)
        if request.method == "POST":
            form = HorsesForm(request.POST, instance=horses)
            if form.is_valid():
                form.save()
                return redirect("horses")
    except Exception as e:
        print(e)
    context = {"form": form}
    return render(request, "accounts/admin2/horses_form.html", context)


@login_required(login_url="login")
def suspendMembers(request, pk):
    if request.user.is_member:
        return redirect("member_dashboard")
    members = mem_models.Member.objects.get(id=pk)
    # form = SuspendForm(instance=members)
    if request.method == "POST":
        mem_models.Member.objects.update(suspend=True)
        return redirect("members")
    context = {"form": members, "members": members}
    return render(request, "accounts/admin2/suspend.html", context)


@login_required(login_url="login")
def resumeMembers(request, pk):
    if request.user.is_member:
        return redirect("member_dashboard")
    members = mem_models.Member.objects.get(id=pk)
    # form = SuspendForm(instance=members)
    if request.method == "POST":
        mem_models.Member.objects.update(suspend=False)
        return redirect("members")
    context = {"form": members, "members": members}
    return render(request, "accounts/admin2/suspend.html", context)


# --------------   End of Admin members      ------------------

# --------------    Services      ------------------


@login_required(login_url="login")
def services(request):
    try:
        if request.user.is_admin == False:
            return redirect("member_dashboard")
        elif request.user.is_admin != True:
            return redirect("member_dashboard")
        form = Services.objects.all()
    except Exception as e:
        print(e)
    context = {"form": form}
    return render(request, "accounts/admin2/services.html", context)


@login_required(login_url="login")
def addServices(request):
    try:
        if request.user.is_admin == False:
            return redirect("member_dashboard")
        elif request.user.is_admin != True:
            return redirect("member_dashboard")
        form = ServicesForm()
        if request.method == "POST":
            form = ServicesForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("services")
    except Exception as e:
        print(e)
    context = {"form": form}
    return render(request, "accounts/admin2/service_form.html", context)


@login_required(login_url="login")
def updateServices(request, pk):
    try:
        if request.user.is_admin == False:
            return redirect("member_dashboard")
        elif request.user.is_admin != True:
            return redirect("member_dashboard")
        services = Services.objects.get(id=pk)
        form = ServicesForm(instance=services)
        if request.method == "POST":
            form = ServicesForm(request.POST, instance=services)
            if form.is_valid():
                form.save()
                return redirect("services")
    except Exception as e:
        print(e)
    context = {"form": form}
    return render(request, "accounts/admin2/service_form.html", context)


@login_required(login_url="login")
def removeServices(request, pk):
    try:
        if request.user.is_admin == False:
            return redirect("member_dashboard")
        elif request.user.is_admin != True:
            return redirect("member_dashboard")
        services = Services.objects.get(id=pk)
        if request.method == "POST":
            services.delete()
            return redirect("services")
    except Exception as e:
        print(e)
    return render(request, "accounts/admin2/delete.html", {"obj": services})


# --------------   End of Services      ------------------

# --------------    Tickets      ------------------


@login_required(login_url="login")
def tickets(request):
    try:
        if request.user.is_member:
            return redirect("member_dashboard")
        form = Tickets.objects.all()
    except Exception as e:
        print(e)
    context = {"form": form}
    return render(request, "staff/billing/tickets.html", context)


@login_required(login_url="login")
def printTickets(request, pk):
    if request.user.is_member:
        return redirect("member_dashboard")
    tickets = Tickets.objects.get(id=pk)
    if tickets.used:
        messages.error(request, "Ticket Already used")
        return redirect("tickets")

    form = TicketsForm(instance=tickets)
    today = date.today()
    print("Today's date:", today)
    context = {"today": today, "tickets": tickets, "form": form}
    return render(request, "staff/billing/printed_tickets.html", context)


class printed(View):
    def get(self, request, pk):
        try:
            tickets = Tickets.objects.get(id=pk)
            tickets.used = True
            tickets.save()
            # messages.success(request, 'Ticket Printed Sucessfully')
            return redirect("tickets")

        except Exception as e:
            print(e)
        return redirect("login")


@login_required(login_url="login")
def addTickets(request):
    try:
        if request.user.is_member:
            return redirect("member_dashboard")
        form = TicketsForm()
        if request.method == "POST":
            random_integer = random.randint(1, 1000)
            ticket_number = f"belham{random_integer}"
            form = TicketsForm(request.POST)
            user = request.user.username
            service = request.POST.get("service")
            services = Services.objects.get(id=service)
            print(services, user)
            quantity = request.POST.get("quantity")
            price = services.price
            total = int(quantity) * int(price)
            if form.is_valid():
                tickets = form.save(commit=False)
                tickets.ticket_number = ticket_number
                tickets.attendant = user
                tickets.total_price = total
                tickets.save()
                return redirect("tickets")
    except Exception as e:
        print(e)
    context = {"form": form}
    return render(request, "staff/billing/tickets_form.html", context)


@login_required(login_url="login")
def removeTickets(request, pk):
    try:
        if request.user.is_admin == False:
            return redirect("member_dashboard")
        elif request.user.is_admin != True:
            return redirect("member_dashboard")
        tickets = Tickets.objects.get(id=pk)
        if request.method == "POST":
            tickets.delete()
            return redirect("tickets")
    except Exception as e:
        print(e)
    return render(request, "accounts/admin2/delete.html", {"obj": tickets})


# --------------   End of Tickets      ------------------


# --------------    Equipment      ------------------
@login_required(login_url="login")
def equipment(request):
    try:
        if request.user.is_member:
            return redirect("member_dashboard")
        equipment = Equipment.objects.all()
    except Exception as e:
        print(e)
    context = {"equipment": equipment}
    return render(request, "staff/inventory/equipment.html", context)


@login_required(login_url="login")
def addEquipment(request):
    if request.user.is_member:
        return redirect("member_dashboard")
    form = EquipmentForm()
    if request.method == "POST":
        form = EquipmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("equipment")
    context = {"form": form}
    return render(request, "staff/inventory/equipment_form.html", context)


@login_required(login_url="login")
def updateEquipment(request, pk):
    equipment = Equipment.objects.get(id=pk)
    form = EquipmentForm(instance=equipment)
    if request.method == "POST":
        form = EquipmentForm(request.POST, instance=equipment)
        if form.is_valid():
            form.save()
            return redirect("equipment")
    context = {"form": form}
    return render(request, "staff/inventory/equipment_form.html", context)


@login_required(login_url="login")
def removeEquipment(request, pk):
    equipment = Equipment.objects.get(id=pk)

    if request.method == "POST":
        equipment.delete()
        return redirect("equipment")

    return render(request, "staff/delete.html", {"obj": equipment})


# --------------   End of Equipment      ------------------


# --------------    Users      ------------------
@login_required(login_url="login")
def costumUser(request):
    form = CustomUser.objects.all()
    context = {"form": form}
    return render(request, "accounts/admin2/costumUser.html", context)


@login_required(login_url="login")
def updateCostumUser(request, pk):
    costumUser = CustomUser.objects.get(id=pk)
    form = CustomUserForm(instance=costumUser)

    if request.user.is_member == True:
        return HttpResponse("You are not allowed here!!")
    elif request.user != costumUser.username:
        return HttpResponse("You are not allowed here!!")

    if request.method == "POST":
        form = CustomUserForm(request.POST, instance=costumUser)
        if form.is_valid():
            form.save()
            return redirect("costumUser")
    context = {"form": form}
    return render(request, "accounts/admin2/costumUser_form.html", context)


# --------------   End of Users      ------------------


# --------------   End of Slots      ------------------
@login_required(login_url="login")
def members_history(request):
    user = request.user
    if user.is_member == True:
        return redirect("member_dashboard")
    payment_history = mem_models.PayHistory.objects.all().order_by("-date_created")

    context = {"payment_history": payment_history}
    # return render(request, 'members/dashboard.html', context)
    return render(request, "staff/billing/billing_history.html", context)


@login_required(login_url="login")
def staff_notification(request):
    if request.user.is_member:
        return redirect("member_dashboard")
    form = Notification.objects.all()
    context = {"form": form}
    return render(request, "staff/rest/notification.html", context)


@login_required(login_url="login")
def add_notifications(request):
    if request.user.is_member:
        return redirect("member_dashboard")
    form = NotificationForm()
    if request.method == "POST":
        form = NotificationForm(request.POST)
        if form.is_valid():
            notification = form.save(commit=False)
            notification.user = request.user
            notification.save()
            return redirect("staff_notification")
    context = {"form": form}
    return render(request, "staff/rest/notification_form.html", context)


@login_required(login_url="login")
def update_notifications(request, pk):
    if request.user.is_member:
        return redirect("member_dashboard")
    notifications = Notification.objects.get(id=pk)
    form = NotificationForm(instance=notifications)
    if request.method == "POST":
        form = NotificationForm(request.POST, instance=notifications)
        if form.is_valid():
            notification = form.save(commit=False)
            notification.user = request.user
            notification.save()
            return redirect("staff_notification")
    context = {"form": form}
    return render(request, "staff/rest/notification_form.html", context)


@login_required(login_url="login")
def remove_notifications(request, pk):
    notification = Notification.objects.get(id=pk)

    if request.method == "POST":
        notification.delete()
        return redirect("staff_notification")

    return render(request, "staff/delete.html", {"obj": notification.message})


@login_required(login_url="login")
def polo_schedule(request):
    if request.user.is_member:
        return redirect("member_dashboard")

    days_selected = mem_models.Days.objects.all()

    members_by_day = {}
    for day in days_selected:
        members_for_day = mem_models.Member.objects.filter(days=day)
        members_by_day[day] = members_for_day

    print(f"members_by_day:{members_by_day}")

    context = {"days_selected": days_selected, "members_by_day": members_by_day}
    return render(request, "staff/members/polo_schedule.html", context)
