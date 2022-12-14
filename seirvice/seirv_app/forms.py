from django.forms import TextInput, PasswordInput, CharField, Select, ModelForm, NumberInput, CheckboxInput, HiddenInput, EmailInput
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm


#from django.contrib.auth.models import User
from .models import CustomUser, USER_CHOICES, InfectiousDisease, Dengue, MASK_CHOICES

class UserForm(UserCreationForm):
    password1 = CharField(widget=PasswordInput(attrs={ 'class' : 'form-control form-control-lg', 'placeholder' : 'Password', 'required' : True ,}))
    password2 = CharField(widget=PasswordInput(attrs={ 'class' : 'form-control form-control-lg', 'placeholder' : 'Confirm Password', 'required' : True ,}))
    profession = CharField(widget=Select(attrs={'class' : 'form-select mb-4', 'name' : 'role'}, choices=USER_CHOICES ))
    
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'profession']
        widgets = {
            'username' : TextInput(attrs = { 'class' : 'form-control form-control-lg', 'name' : 'username', 'placeholder' : 'Username', 'required' : True ,}),
            'email' : TextInput(attrs = { 'type' : 'email' , 'class' : 'form-control form-control-lg', 'name' : 'email', 'placeholder' : 'Email', 'required' : True ,})
            }


class InfectiousDiseaseForm(ModelForm):
    class Meta:
        model = InfectiousDisease
        mask_use : CharField(widget=Select(attrs={'class' : 'simulation-textinput input', 'name' : 'mask-use'}, choices=MASK_CHOICES))
        fields = ['user', 'N_in', 't_duration', 'R0_input', 't_incubation', 't_infection', 'E_in', 'I_in', 'R_in', 'v_eff', 'mask_use', 'cov_val']
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
            'cov_val' : NumberInput(attrs = {'class' : 'simulation-textinput input', 'name' : 'cov_val', 'required' : True, 'placeholder' : 'Vaccine Coverage'})
        }

class DengueForm(ModelForm):
    class Meta:
        model = Dengue
        fields = ['user', 'N_h', 'N_v', 't_duration', 'bite_n', 'bv_input', 'bh_input', 'uv_input', 'h_recov_input', 'Ih_in', 'Rh_in', 'Iv_in']
        widgets = {
            'user': HiddenInput(attrs={'name' : 'user'}),
            'N_h' : NumberInput(attrs = {'class' : 'simulation-textinput input', 'name' : 'N_in', 'required' : True, 'placeholder' : 'N (host population)'}), 
            'N_v' : NumberInput(attrs = {'class' : 'simulation-textinput input', 'name' : 'N_in', 'required' : True, 'placeholder' : 'N (vector population: mosquitos)'}), 
            't_duration' : NumberInput(attrs = {'class' : 'simulation-textinput input', 'name' : 'N_in', 'required' : True, 'placeholder' : 'Simulation duration (in days)'}),
            'bite_n' : NumberInput(attrs = {'class' : 'simulation-textinput input', 'name' : 'N_in', 'required' : True, 'placeholder' : 'Number of hosts a mosquito bite in a day'}),
            'bv_input' : NumberInput(attrs = {'class' : 'simulation-textinput input', 'name' : 'N_in', 'required' : True, 'placeholder' : 'Probability of infection (host to vector)'}),
            'bh_input' : NumberInput(attrs = {'class' : 'simulation-textinput input', 'name' : 'N_in', 'required' : True, 'placeholder' : 'Probability of infection (vector to host)'}),
            'uv_input' : NumberInput(attrs = {'class' : 'simulation-textinput input', 'name' : 'N_in', 'required' : True, 'placeholder' : 'Vector mortality rate'}),
            'h_recov_input' : NumberInput(attrs = {'class' : 'simulation-textinput input', 'name' : 'N_in', 'required' : True, 'placeholder' : 'Recovery rate from dengue in humans'}),
            'Ih_in' : NumberInput(attrs = {'class' : 'simulation-textinput input', 'name' : 'Ih_in', 'required' : True, 'placeholder' : 'Initial infected host population'}),
            'Rh_in' : NumberInput(attrs = {'class' : 'simulation-textinput input', 'name' : 'Rh_in', 'required' : True, 'placeholder' : 'Initial recovered host population'}),
            'Iv_in' : NumberInput(attrs = {'class' : 'simulation-textinput input', 'name' : 'Iv_in', 'required' : True, 'placeholder' : 'Initial infected vector population'})
        }

class MyPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        attrs = { 'class' : 'form-control', 'id' : 'floating-input', 'required' : True ,}
        
        for fieldname in ['email']:
            self.fields[fieldname].widget=EmailInput(attrs=attrs)