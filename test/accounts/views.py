from django.shortcuts import render, redirect
from .forms import EquipmentForm,HorsesForm, CustomUserForm, SlotsForm, ServicesForm, TicketsForm
from django.contrib.auth.decorators import login_required
from .models import Horses, Equipment, Slots, Services, Tickets
from members import models

from authenticate.models import CustomUser




from datetime import date
from django.db.models import Sum


@login_required(login_url='login')
def home(request):
    try:
        if request.user.is_admin==False:
            return redirect('member_dashboard')
        no_members = models.Member.objects.all().count()
        membership = models.Membership.objects.all()
        try:
            polo_payment_sum = models.PayHistory.objects.filter(activity="Polo").aggregate(Sum('amount'))['amount__sum']
            riding_payment_sum = models.PayHistory.objects.filter(activity="Riding").aggregate(Sum('amount'))['amount__sum']
        except models.PayHistory.DoesNotExist:
            polo_payment_sum = 0
            riding_payment_sum = 0
        try:
            polo_count = models.Member.objects.filter(activity="Polo").count()
            riding_count = models.Member.objects.filter(activity="Riding").count()
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
        form = models.Member.objects.all()
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
    members = models.Member.objects.get(id=pk)
    # form = SuspendForm(instance=members)
    if request.method == "POST":
        models.Member.objects.update(
            suspend=True
        )
        return redirect('members')
    context = {"form":members,"members":members}
    return render(request, 'accounts/admin2/suspend.html', context)

@login_required(login_url='login')
def resumeMembers(request,pk):
    if request.user.is_member:
        return redirect('member_dashboard')
    members = models.Member.objects.get(id=pk)
    # form = SuspendForm(instance=members)
    if request.method == "POST":
        models.Member.objects.update(
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
