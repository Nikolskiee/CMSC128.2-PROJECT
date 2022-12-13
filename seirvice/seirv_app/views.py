from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import UserForm, InfectiousDiseaseForm, DengueForm
from .seirv import infectious_disease, dengue
from .models import InfectiousDisease, Dengue


# Create your views here.
@login_required(login_url='/login')
#i-uncomment niyo na lang yung login required kung bet niyo matest ibang html working pa sa user

def home(request):
    return render(request, 'simulation.html')

def history(request):
    infectious_history = InfectiousDisease.objects.filter(user=request.user.id).order_by('-id')
    dengue_history = Dengue.objects.filter(user=request.user.id).order_by('-id')

    data = {
        'infectious_history': infectious_history,
        'dengue_history': dengue_history
    }
    return render(request, 'try-history.html', context=data)

def signup(request):
    form = UserForm()

    if(request.method == "POST"):
        form = UserForm(request.POST)
        if(form.is_valid()):
            form.save()
            messages.success(request, "Account was created for " + form.cleaned_data.get("username"))
            return redirect('/login')
        
    data = {"form" : form}

    return render(request, 'signup.html', data)

def signin(request):
    if(request.method == "POST"):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            print("Login was successful")
            return redirect('/')
        else:
            print("Login failed")
            messages.error(request, "Incorrect password or username.")
    return render(request, 'login.html')

@login_required
def infectiousDisease(request):
    form = InfectiousDiseaseForm()
    if(request.method == "POST"):
        post = request.POST.copy()
        post['user'] = request.user.id
        form = InfectiousDiseaseForm(post)
        if(form.is_valid()):
            form.save()
            params = {
                'N_in' : request.POST.get('N_in'),
                't_duration' : request.POST.get('t_duration'),
                'R0_input' : request.POST.get('R0_input'),
                't_incubation' : request.POST.get('t_incubation'),
                't_infection' : request.POST.get('t_infection'),
                'E_in' : request.POST.get('E_in'),
                'I_in' : request.POST.get('I_in'),
                'R_in' : request.POST.get('R_in'),
                'v_eff' : request.POST.get('v_eff'),
                'mask_use' : request.POST.get('mask_use')
            }
            context = infectious_disease(params)
            context.update({"form" : form})
            return render(request, 'simulation.html', context=context)

            
    data = {
        'form' : form
    }
    return render(request, 'simulation.html', data)

@login_required
def dengueDisease(request):
    form = DengueForm()
    if(request.method == "POST"):
        post = request.POST.copy()
        post['user'] = request.user.id
        form = DengueForm(post)
        if(form.is_valid()):
            form.save()
            params = {
                'N_h' : request.POST.get('N_h'),
                'N_v' : request.POST.get('N_v'),
                't_duration' : request.POST.get('t_duration'),
                'bite_n' : request.POST.get('bite_n'),
                'bv_input' : request.POST.get('bv_input'),
                'bh_input' : request.POST.get('bh_input'),
                'uv_input' : request.POST.get('uv_input'),
                'h_recov_input' : request.POST.get('h_recov_input')
            }
            context = dengue(params)
            context.update({"form" : form})
            return render(request, 'dengue.html', context=context)

            
    data = {
        'form' : form
    }
    return render(request, 'dengue.html', data)