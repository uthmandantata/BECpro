from django import forms
from . import models

# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Layout, Fieldset, Submit
from django.contrib.auth.forms import UserCreationForm





class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ('first_name', 'last_name','email', 'phone', 'address')


class MemberRegistrationForm(forms.ModelForm):
    class Meta:
        model = models.Member
        fields = ('email', 'guardian_name','guardian_age', 'guardian_weight', 'guardian_height',
                  'member1_full_name', 'member1_age','member1_email', 'member1_weight', 'member1_height','member1_address',
                  'member2_full_name', 'member2_age','member2_email', 'member2_weight', 'member2_height','member2_address')
        
        

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.save()
        return instance
    
class MemberForm(forms.ModelForm):
    class Meta:
        model = models.Member
        fields = ('guardian_name', 'guardian_age', 'guardian_weight', 'guardian_height', 'email','day1','day2','day3')

        def __init__(self, *args, **kwargs):
            super(MemberForm, self).__init__(*args, **kwargs)
            self.fields['membership'].disabled = True


class ForgetPasswordForm(forms.ModelForm):
    class Meta:
        model = models.ForgetPassword
        fields = '__all__'