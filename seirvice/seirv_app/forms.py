from django.forms import TextInput, PasswordInput, CharField, Select
from django.contrib.auth.forms import UserCreationForm


#from django.contrib.auth.models import User
from .models import CustomUser, USER_CHOICES

class UserForm(UserCreationForm):
    attrs = { 'class' : 'sign-up-textinput2 input', 'id' : 'floating-input', 'placeholder' : 'Enter Password', 'required' : True ,}
    password1 = CharField(widget=PasswordInput(attrs=attrs))
    password2 = CharField(widget=PasswordInput(attrs=attrs))
    profession = CharField(widget=Select(attrs={'class' : 'sign-up-select dropdown', 'id' : 'role', 'name' : 'role'}, choices=USER_CHOICES ))
    
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'profession']
        widgets = {
            'username' : TextInput(attrs = { 'class' : 'sign-up-textinput1 input', 'id' : 'floating-input', 'name' : 'username', 'placeholder' : 'Enter Username', 'required' : True ,}),
            'email' : TextInput(attrs = { 'type' : 'email' , 'class' : 'sign-up-textinput1 input', 'id' : 'floating-input', 'name' : 'email', 'placeholder' : 'Enter Email', 'required' : True ,})
            }