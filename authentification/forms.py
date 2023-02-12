from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):  
    # remove password confirming
    password2 = None  
    # make email field as required
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'mail_field'})) 
    
    class Meta:
        model = User
        fields = ['username', 'email'] 
        # widgets = {
        #     'email': forms.EmailInput(attrs={'class': 'mail_field'})
        # } 
    

class AuthForm(forms.Form):
    # username = forms.CharField()
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())