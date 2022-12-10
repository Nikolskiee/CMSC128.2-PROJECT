from django.forms import TextInput, PasswordInput, CharField
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User
#from .models import *

class UserForm(UserCreationForm):
    attrs = { 'class' : 'form-control', 'id' : 'floating-input', 'placeholder' : 'Enter Password', 'required' : True ,}
    password1 = CharField(widget=PasswordInput(attrs=attrs))
    password2 = CharField(widget=PasswordInput(attrs=attrs))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username' : TextInput(attrs = { 'class' : 'form-control', 'id' : 'floating-input', 'name' : 'username', 'placeholder' : 'Enter Username', 'required' : True ,}),
            'email' : TextInput(attrs = { 'type' : 'email' , 'class' : 'form-control', 'id' : 'floating-input', 'name' : 'email', 'placeholder' : 'Enter Email', 'required' : True ,})
            }