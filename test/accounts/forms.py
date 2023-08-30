from django import forms
from .models import Equipment, Horses, Slots, Services, Tickets
from authenticate import models as md
from members import models as member_models
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Layout, Fieldset, Submit
from django.contrib.auth.forms import UserCreationForm



class CustomUserForm(forms.ModelForm):
    class Meta:
        model = md.CustomUser
        fields = ('username', 'is_super_admin','is_admin','is_member')










class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
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

