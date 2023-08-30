from django import forms
from . import models


class familyRidingMemberForm(forms.ModelForm):
    class Meta:
        model = models.Member
        fields = ('email', 'guardian_age', 'guardian_weight', 'guardian_height',
                  'member1_full_name', 'member1_age','member1_email', 'member1_weight', 'member1_height','member1_address',
                  'member2_full_name', 'member2_age','member2_email', 'member2_weight', 'member2_height','member2_address')
        

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.save()
        return instance
    

class MemberRegistrationForm(forms.ModelForm):
    class Meta:
        model = models.Member
        fields = ('email', 'guardian_age', 'guardian_weight', 'guardian_height',
                  'member1_full_name', 'member1_age','member1_email', 'member1_weight', 'member1_height','member1_address',
                  'member2_full_name', 'member2_age','member2_email', 'member2_weight', 'member2_height','member2_address', 'days')
        

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.save()
        return instance
    
class MemberForm(forms.ModelForm):
    class Meta:
        model = models.Member
        fields = ('guardian_age', 'guardian_weight', 'guardian_height', 'email','days')
        widgets = {
            'guardian_age': forms.DateInput(attrs={
                'class': 'form-control',
                }),
            'guardian_weight': forms.DateInput(attrs={
                'class': 'form-control',
                }),
            'email': forms.DateInput(attrs={
                'class': 'form-control',
                'type':'email',
                }),
            'guardian_height': forms.DateInput(attrs={
                'class': 'form-control',
                'type':'number',
                }),
            
                }

class ridingMemberForm(forms.ModelForm):
    class Meta:
        model = models.Member
        fields = ('guardian_age', 'guardian_weight', 'guardian_height', 'email')
        widgets = {
            'guardian_age': forms.DateInput(attrs={
                'class': 'form-control',
                }),
            'guardian_weight': forms.DateInput(attrs={
                'class': 'form-control',
                }),
            'email': forms.DateInput(attrs={
                'class': 'form-control',
                'type':'email',
                }),
            'guardian_height': forms.DateInput(attrs={
                'class': 'form-control',
                'type':'number',
                }),
            
                }
    


class ForgetPasswordForm(forms.ModelForm):
    class Meta:
        model = models.ForgetPassword
        fields = '__all__'




class MembershipForm(forms.ModelForm):
    class Meta:
        model = models.Membership
        fields = '__all__'
