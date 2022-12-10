from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
#@login_required(login_url='/login')
#i-uncomment niyo na lang yung login required kung bet niyo matest ibang html working pa sa user

def home(request):
    return render(request, 'simulation.html')

def history(request):
    return render(request, 'history.html')

def signup(request):
    return render(request, 'signup.html')

def login(request):
    return render(request, 'login.html')