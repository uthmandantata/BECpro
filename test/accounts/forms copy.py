from django import forms
from .models import Profile, Member, Equipment, Horses, ForgetPassword, Slots, Membership, Services, Tickets
from authenticate import models as md
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Layout, Fieldset, Submit
from django.contrib.auth.forms import UserCreationForm



class CustomUserForm(forms.ModelForm):
    class Meta:
        model = md.CustomUser
        fields = ('username', 'is_super_admin','is_admin','is_member')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name','email', 'phone', 'address')


class MembershipForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields = '__all__'





class MemberRegistrationForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('email', 'guardian_name','guardian_age', 'guardian_weight', 'guardian_height',
                  'member1_full_name', 'member1_age','member1_email', 'member1_weight', 'member1_height','member1_address',
                  'member2_full_name', 'member2_age','member2_email', 'member2_weight', 'member2_height','member2_address')
        
        

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.save()
        return instance
    
class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('guardian_name', 'guardian_age', 'guardian_weight', 'guardian_height', 'email','day1','day2','day3')

        def __init__(self, *args, **kwargs):
            super(MemberForm, self).__init__(*args, **kwargs)
            self.fields['membership'].disabled = True


class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = '__all__'



class ForgetPasswordForm(forms.ModelForm):
    class Meta:
        model = ForgetPassword
        fields = '__all__'

class HorsesForm(forms.ModelForm):
    class Meta:
        model = Horses
        fields = '__all__'
        

class SlotsForm(forms.ModelForm):
    class Meta:
        model = Slots
        fields = '__all__'


class ServicesForm(forms.ModelForm):
    class Meta:
        model = Services
        fields = '__all__'
        

class TicketsForm(forms.ModelForm):
    class Meta:
        model = Tickets
        fields = '__all__'

