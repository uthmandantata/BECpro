@login_required(login_url='login')
def updateMembersDetails(request,pk):
    user = request.user
    days = Days.objects.all()
    fetch_member = Member.objects.filter(guardian_name=user.first_name).exists()
    if fetch_member:
        # form = Member.objects.get(guardian_name=user.first_name)
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
                chosen_days_ids = request.POST.getlist('days')
                chosen_days = Days.objects.filter(id__in=chosen_days_ids)

                # Remove existing choices for the user
                Member.objects.filter(user=request.user).delete()

                member_choice = Member(user=request.user)
                member_choice.save()
                member_choice.days.add(*chosen_days)
                form = MemberRegistrationForm(request.POST, instance=members)
                if form.is_valid():
                    form.save()
                    return redirect('_account')
        else:
            stat = "Single"
            form = MemberForm(instance=members)
            if request.method == "POST":
                form = MemberForm(request.POST, instance=members)
                if form.is_valid():
                    chosen_days_ids = request.POST.getlist('days')
                    chosen_days = Days.objects.filter(id__in=chosen_days_ids)
                    update_member = form.save(commit=False)
                    update_member.days.clear()
                    update_member.days.add(*chosen_days)
                    update_member.save()
                    return redirect('_account')
        if member.paid:
            notifications = Notification.objects.all()
            notification_count = Notification.objects.filter(is_read=False).count()
        context ={"notifications":notifications,"notification_count":notification_count,"form":form,"stat":stat,"days":days}
        return render(request, 'members/member_detail_form.html', context)
    return render(request, 'members/member_detail_form.html')
    
# --------------   End of Members      ------------------