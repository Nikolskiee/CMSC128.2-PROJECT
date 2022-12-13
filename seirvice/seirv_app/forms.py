from django.forms import TextInput, PasswordInput, CharField, Select, ModelForm, NumberInput, CheckboxInput, HiddenInput
from django.contrib.auth.forms import UserCreationForm


#from django.contrib.auth.models import User
from .models import CustomUser, USER_CHOICES, InfectiousDisease, Dengue

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


class InfectiousDiseaseForm(ModelForm):
    class Meta:
        model = InfectiousDisease
        fields = ['user', 'N_in', 't_duration', 'R0_input', 't_incubation', 't_infection', 'E_in', 'I_in', 'R_in', 'v_eff', 'mask_use']
        widgets = {
            'user': HiddenInput(attrs={'name' : 'user'}),
            'N_in' : NumberInput(attrs = {'class' : 'simulation-textinput input', 'name' : 'N_in', 'required' : True, 'placeholder' : 'N'}),
            't_duration' : NumberInput(attrs = {'class' : 'simulation-textinput input', 'name' : 't_duration', 'required' : True, 'placeholder' : 'Simulation duration'}),
            'R0_input' : NumberInput(attrs = {'class' : 'simulation-textinput input', 'name' : 'R0_input', 'required' : True, 'placeholder' : 'R0'}),
            't_incubation' : NumberInput(attrs = {'class' : 'simulation-textinput input', 'name' : 't_incubation', 'required' : False, 'placeholder' : 'Incubation period'}),
            't_infection' : NumberInput(attrs = {'class' : 'simulation-textinput input', 'name' : 't_infection', 'required' : True, 'placeholder' : 'Symptomatic infection period'}),
            'E_in' : NumberInput(attrs = {'class' : 'simulation-textinput input', 'name' : 'E_in', 'required' : True, 'placeholder' : 'Initial exposed population'}),
            'I_in' : NumberInput(attrs = {'class' : 'simulation-textinput input', 'name' : 'I_in', 'required' : True, 'placeholder' : 'Initial infected population'}),
            'R_in' : NumberInput(attrs = {'class' : 'simulation-textinput input', 'name' : 'R_in', 'required' : True, 'placeholder' : 'Initial recovered population'}),
            'v_eff' : NumberInput(attrs = {'class' : 'simulation-textinput input', 'name' : 'v_eff', 'required' : True, 'placeholder' : 'Vaccine efficacy'}),
            'mask_use' : CheckboxInput()
        }

class DengueForm(ModelForm):
    class Meta:
        model = Dengue
        fields = ['N_h', 'N_v', 't_duration', 'bite_n', 'bv_input', 'bh_input', 'uv_input', 'h_recov_input']
        widgets = {
            'N_h' : NumberInput(attrs = {'class' : 'simulation-textinput input', 'name' : 'N_in', 'required' : True, 'placeholder' : 'N'}), 
            'N_v' : NumberInput(attrs = {'class' : 'simulation-textinput input', 'name' : 'N_in', 'required' : True, 'placeholder' : 'N'}), 
            't_duration' : NumberInput(attrs = {'class' : 'simulation-textinput input', 'name' : 'N_in', 'required' : True, 'placeholder' : 'N'}),
            'bite_n' : NumberInput(attrs = {'class' : 'simulation-textinput input', 'name' : 'N_in', 'required' : True, 'placeholder' : 'N'}),
            'bv_input' : NumberInput(attrs = {'class' : 'simulation-textinput input', 'name' : 'N_in', 'required' : True, 'placeholder' : 'N'}),
            'bh_input' : NumberInput(attrs = {'class' : 'simulation-textinput input', 'name' : 'N_in', 'required' : True, 'placeholder' : 'N'}),
            'uv_input' : NumberInput(attrs = {'class' : 'simulation-textinput input', 'name' : 'N_in', 'required' : True, 'placeholder' : 'N'}),
            'h_recov_input' : NumberInput(attrs = {'class' : 'simulation-textinput input', 'name' : 'N_in', 'required' : True, 'placeholder' : 'N'})
        }