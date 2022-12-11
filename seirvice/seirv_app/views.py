from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import UserForm


# Create your views here.
@login_required(login_url='/login')
#i-uncomment niyo na lang yung login required kung bet niyo matest ibang html working pa sa user

def home(request):
    return render(request, 'simulation.html')

def history(request):
    return render(request, 'history.html')

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