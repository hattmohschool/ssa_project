from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    surname = forms.CharField(max_length=30, required=True)
    nickname = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'surname', 'nickname']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['surname']       
        if commit:
            user.save()
            profile = user.profile
            profile.first_name = self.cleaned_data['first_name']
            profile.surname = self.cleaned_data['surname']
            profile.nickname = self.cleaned_data['nickname']
            profile.save()
        return user

class TopUpForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=5,            # Max dig
        decimal_places=2,        # deci
        min_value=0.01,          # Min val
        label="Amount to Top-Up",  
        widget=forms.NumberInput(attrs={
            'step': '0.01',        
            'min': '0.01'          
        }),
        error_messages={
            'min_value': "Please enter an amount greater than $0.00.",
            'invalid': "Enter a valid amount in dollars and cents.",
        }
    )