from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserForm, InfectiousDiseaseForm, DengueForm
from .seirv import infectious_disease, dengue
from .models import InfectiousDisease, Dengue
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.http import HttpResponse
import io

@login_required(login_url='/welcome')
def home(request):
    return render(request, 'dashboard.html')

def welcome(request):
    return render(request, 'index.html')

@login_required(login_url='/login')
def history(request):
    infectious_history = InfectiousDisease.objects.filter(user=request.user.id).order_by('-id')
    dengue_history = Dengue.objects.filter(user=request.user.id).order_by('-id')

    data = {
        'infectious_history': infectious_history,
        'dengue_history': dengue_history
    }
    return render(request, 'history.html', context=data)

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

@login_required(login_url='/login')
def signout(request):
    logout(request)
    return redirect('/login')

@login_required(login_url='/login')
def infectiousDisease(request, pk=''):
    if pk != '':
        history_inst = InfectiousDisease.objects.get(id=pk)
        form = InfectiousDiseaseForm(instance=history_inst)
        params = {
                'N_in' : history_inst.N_in,
                't_duration' : history_inst.t_duration,
                'R0_input' : history_inst.R0_input,
                't_incubation' : history_inst.t_incubation,
                't_infection' : history_inst.t_infection,
                'E_in' : history_inst.E_in,
                'I_in' : history_inst.I_in,
                'R_in' : history_inst.R_in,
                'v_eff' : history_inst.v_eff,
                'mask_use' : history_inst.mask_use
            }
        context = infectious_disease(params)
        context.update({"form" : form})
        context.update({'hide_simulate': True})
        context.update({'pk': pk})
        return render(request, 'simulation.html', context=context)

    form = InfectiousDiseaseForm()
    if(request.method == "POST"):
        post = request.POST.copy()
        post['user'] = request.user.id
        if request.user.profession == 'Student':
            post['t_incubation'] = '5.1'
        form = InfectiousDiseaseForm(post)
        if(form.is_valid()):
            form.save()
            params = {
                'N_in' : request.POST.get('N_in'),
                't_duration' : request.POST.get('t_duration'),
                'R0_input' : request.POST.get('R0_input'),
                't_incubation' : post['t_incubation'],
                't_infection' : request.POST.get('t_infection'),
                'E_in' : request.POST.get('E_in'),
                'I_in' : request.POST.get('I_in'),
                'R_in' : request.POST.get('R_in'),
                'v_eff' : request.POST.get('v_eff'),
                'mask_use' : request.POST.get('mask_use')
            }
            context = infectious_disease(params)
            context.update({"form" : form})
            context.update({'hide_simulate': False})
            return render(request, 'simulation.html', context=context)

            
    data = {
        'form' : form
    }
    return render(request, 'simulation.html', data)

@login_required(login_url='/login')
def dengueDisease(request, pk=''):
    if pk != '':
        history_inst = Dengue.objects.get(id=pk)
        form = DengueForm(instance=history_inst)
        params = {
                'N_h' : history_inst.N_h,
                'N_v' : history_inst.N_v,
                't_duration' : history_inst.t_duration,
                'bite_n' : history_inst.bite_n,
                'bv_input' : history_inst.bv_input,
                'bh_input' : history_inst.bh_input,
                'uv_input' : history_inst.uv_input,
                'h_recov_input' : history_inst.h_recov_input,
                'Ih_in' : history_inst.Ih_in,
                'Rh_in' : history_inst.Rh_in,
                'Iv_in' : history_inst.Iv_in
            }
        context = dengue(params)
        context.update({"form" : form})
        context.update({'hide_simulate': True})
        context.update({'pk': pk})
        return render(request, 'dengue.html', context=context)
    form = DengueForm()
    if(request.method == "POST"):
        post = request.POST.copy()
        post['user'] = request.user.id
        if request.user.profession == 'Student':
            post['N_v']  = '20000'
        form = DengueForm(post)
        if(form.is_valid()):
            form.save()
            params = {
                'N_h' : request.POST.get('N_h'),
                'N_v' : post['N_v'],
                't_duration' : request.POST.get('t_duration'),
                'bite_n' : request.POST.get('bite_n'),
                'bv_input' : request.POST.get('bv_input'),
                'bh_input' : request.POST.get('bh_input'),
                'uv_input' : request.POST.get('uv_input'),
                'h_recov_input' : request.POST.get('h_recov_input'),
                'Ih_in' : request.POST.get('Ih_in'),
                'Rh_in' : request.POST.get('Rh_in'),
                'Iv_in' : request.POST.get('Iv_in')
            }
            context = dengue(params)
            context.update({"form" : form})
            context.update({'hide_simulate': False})
            return render(request, 'dengue.html', context=context)

            
    data = {
        'form' : form
    }
    return render(request, 'dengue.html', data)

@login_required(login_url='/login')
def download_pdf(request, disease, pk):
    if disease == 'infectious':
        data_inst = InfectiousDisease.objects.get(id=pk)
        params = {
                'N_in' : data_inst.N_in,
                't_duration' : data_inst.t_duration,
                'R0_input' : data_inst.R0_input,
                't_incubation' : data_inst.t_incubation,
                't_infection' : data_inst.t_infection,
                'E_in' : data_inst.E_in,
                'I_in' : data_inst.I_in,
                'R_in' : data_inst.R_in,
                'v_eff' : data_inst.v_eff,
                'mask_use' : data_inst.mask_use
        }
        context = infectious_disease(params, image=True)
        context.update({'title': 'Infectious Disease Model for Coronavirus, Influenza, and Measles'})
        context.update({'infectious_disease': data_inst})
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="simulation_output.pdf"'
        template_path = 'pdf_template_infectious.html'
        template = get_template(template_path)
        html = template.render(context)
        pdf = pisa.CreatePDF(html, dest=response)

        if not pdf.err:
            return response

    if disease == 'dengue':
        data_inst = Dengue.objects.get(id=pk)
        params = {
                'N_h' : data_inst.N_h,
                'N_v' : data_inst.N_v,
                't_duration' : data_inst.t_duration,
                'bite_n' : data_inst.bite_n,
                'bv_input' : data_inst.bv_input,
                'bh_input' : data_inst.bh_input,
                'uv_input' : data_inst.uv_input,
                'h_recov_input' : data_inst.h_recov_input,
                'Ih_in' : data_inst.Ih_in,
                'Rh_in' : data_inst.Rh_in,
                'Iv_in' : data_inst.Iv_in
            }
        context = dengue(params, image=True)
        context.update({'title': 'Infectious Disease Model for Dengue'})
        context.update({'dengue_disease': data_inst})
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="simulation_output.pdf"'
        template_path = 'pdf_template_dengue.html'
        template = get_template(template_path)
        html = template.render(context)
        pdf = pisa.CreatePDF(html, dest=response)

        if not pdf.err:
            return response
    return request

def about(request):
    return render(request, 'about.html')

@login_required(login_url='/login')
def dashboard(request):
    return render(request, 'dashboard.html')
