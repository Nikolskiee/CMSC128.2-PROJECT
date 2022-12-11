from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import UserForm

from plotly.offline import plot
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from scipy.integrate import odeint
import numpy as np

from .idmcomp import DengueComp

import json

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

def plot_dengue (request):

    # Inputs na hardcoded muna, manggagaling sa forms yung inputs here

    N_h = 1000 # N (host population)

    N_v = 2000 # N (vector population: mosquitos)

    t_duration = 180 # Simulation duration (in days)

    bite_n = 1 # Number of hosts a mosquito bite in a day

    bv_input = 0.4 # Probability of infection (host to vector)

    bh_input = 0.4 # Probability of infection (vector to host)

    uv_input = 0.25 # Vector mortality rate

    h_recov_input = 0.167 # Recovery rate from dengue in humans

    
    # Create model for dengue using the DengueComp class from IdmComp

    model = DengueComp(
            Nv = N_v,
            Nh = N_h,
            time = t_duration,
            t_bite = bite_n,
            bv = bv_input,
            bh = bh_input,
            uv = uv_input,
            h_recov = h_recov_input)

    duration, bite_rate, bv, bh, uv, h_recov = model.dengue_rates()


    # Initial State Inputs:

    Ih_in = 1 # Initial infected host population

    Rh_in = 0 # Initial recovered host population

    Iv_in = 1 # Initial infected vector population

    y_in_dengue = model.initial_state_dengue(Ih_in=Ih_in,
                                            Rh_in=Rh_in,
                                            Iv_in=Iv_in)
    
    # Define the Ross MacDonald function:

    def RM_model(y, N_h, N_v, time, bite_rate, bv, bh, uv, h_recov):
        Sh, Ih, Rh, Sv, Iv = y

        ## Total host and vector population:
        N_h = Sh+Ih+Rh
        N_v = Sv+Iv

        ## Host calculation
        dSh = -bite_rate*bh*Sh*Iv/N_h
        dIh = (bite_rate*bh*Sh*Iv/N_h)-h_recov*Ih
        dRh = h_recov*Ih

        ## Vector calculation
        dSv = uv*N_v-(bite_rate*bv*Sv*Ih/N_h)-uv*Sv
        dIv = ((bite_rate*bv/N_h)*Sv*Ih)-uv*Iv

        return dSh, dIh, dRh, dSv, dIv
    
    # Solve the ordinary differential equations:

    output = odeint(func=RM_model, y0=y_in_dengue, t=duration, args=(N_h, N_v, bite_rate, bv, bh, uv, h_recov))
    Sh, Ih, Rh, Sv, Iv = output.T
    output_df = pd.DataFrame(output)
    output_df = output_df.rename(columns={  0: 'Sh',
                                            1: 'Ih',
                                            2: 'Rh',
                                            3: 'Sv',
                                            4: 'Iv'
                                        }
                                )
    output_df.index = output_df.index + 1
    output_df['Days'] = output_df.index
    output_df = output_df.apply(np.ceil)

    model_plot = []

    # Plot of Susceptible host (Sh)
    model_plot.append(go.Scatter(x=output_df['Days'],
                                    y=output_df['Sh'],
                                    legendgroup=1,
                                    name='Susceptible Host')
                        )

    # Plot of Infected host (Ih)
    model_plot.append(go.Scatter(x=output_df['Days'],
                                    y=output_df['Ih'],
                                    legendgroup=1,
                                    name='Infected Host')
                        )
    
    # Plot of Recovered (Rh)
    model_plot.append(go.Scatter(x=output_df['Days'],
                                    y=output_df['Rh'],
                                    legendgroup=1,
                                    name='Recovered Host')
                        )

    # Plot of Susceptible vector (Sv)
    model_plot.append(go.Scatter(x=output_df['Days'],
                                    y=output_df['Sv'],
                                    legendgroup=1,
                                    name='Susceptible Vector')
                        )
    
    # Plot of Infected vector (Iv)
    model_plot.append(go.Scatter(x=output_df['Days'],
                                    y=output_df['Iv'],
                                    legendgroup=1,
                                    name='Infected Vector')
                        )
    
    # Update graph layout
    
    layout = {
        'title' : 'Ross Macdonald Model Projection for Dengue (Vector = Aedes aegypti Mosquito)',
        'xaxis_title': 'Time (Days)',
        'yaxis_title': 'Population',
        'height': 500,
        'width': 600
    }

    # Getting the HTML needed to render the plot.

    plot_div = plot(
        {
            'data': model_plot,
            'layout': layout
        },
        output_type='div'
    )

    # Getting the HTML needed to render the dataframe

    table_frame = output_df.reset_index().to_json(orient = 'records')
    table = json.loads(table_frame)

    return render(request, 'demo-plot.html', context={'plot_div' : plot_div, 'table': table})


def demo_plot_view(request):
    """ 
    View demonstrating how to display a graph object
    on a web page with Plotly. 
    """
    
    # Generating some data for plots.
    x = [i for i in range(-10, 11)]
    y1 = [3*i for i in x]
    y2 = [i**2 for i in x]
    y3 = [10*abs(i) for i in x]

    # List of graph objects for figure.
    # Each object will contain on series of data.
    graphs = []

    # Adding linear plot of y1 vs. x.
    graphs.append(
        go.Scatter(x=x, y=y1, mode='lines', name='Line y1')
    )

    # Adding scatter plot of y2 vs. x. 
    # Size of markers defined by y2 value.
    graphs.append(
        go.Scatter(x=x, y=y2, mode='markers', opacity=0.8, 
                   marker_size=y2, name='Scatter y2')
    )

    # Adding bar plot of y3 vs x.
    graphs.append(
        go.Bar(x=x, y=y3, name='Bar y3')
    )

    # Setting layout of the figure.
    layout = {
        'title': 'Title of the figure',
        'xaxis_title': 'X',
        'yaxis_title': 'Y',
        'height': 420,
        'width': 560,
    }

    # Getting HTML needed to render the plot.
    plot_div = plot({'data': graphs, 'layout': layout}, 
                    output_type='div')

    return render(request, 'demo-plot.html', 
                  context={'plot_div': plot_div})