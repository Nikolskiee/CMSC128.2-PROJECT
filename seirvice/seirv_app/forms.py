from django.forms import TextInput, PasswordInput, CharField, Select
from django.contrib.auth.forms import UserCreationForm


#from django.contrib.auth.models import User
from .models import CustomUser

class UserForm(UserCreationForm):
    attrs = { 'class' : 'form-control', 'id' : 'floating-input', 'placeholder' : 'Enter Password', 'required' : True ,}
    password1 = CharField(widget=PasswordInput(attrs=attrs))
    password2 = CharField(widget=PasswordInput(attrs=attrs))
    profession = CharField(widget=Select)
    
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'profession']
        widgets = {
            'username' : TextInput(attrs = { 'class' : 'form-control', 'id' : 'floating-input', 'name' : 'username', 'placeholder' : 'Enter Username', 'required' : True ,}),
            'email' : TextInput(attrs = { 'type' : 'email' , 'class' : 'form-control', 'id' : 'floating-input', 'name' : 'email', 'placeholder' : 'Enter Email', 'required' : True ,})
            }