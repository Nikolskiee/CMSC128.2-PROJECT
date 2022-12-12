from plotly.offline import plot
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from scipy.integrate import odeint
import numpy as np

from .idmcomp import DengueComp, IdmComp

import json

def seir(N_in, t_duration, R0_input, t_incubation, t_infection):
    # Inputs for each of the Parameters

    #N_in = 1000 # N (Total Population)

    #t_duration = 100 # Simulation Duration (in days)

    #R0_input = 2.4 # Basic Reproduction Number (R0)

    #t_incubation = 5.1 # Incubation period (in days):

    #t_infection = 3.3 # Symptomatic infection period (in days)

    # Inputs for each of the Initial Values

    E_in = 1 # Initial exposed population

    I_in = 1 # Initial infected population

    R_in = 0 # Initial recovered population

    # Inputs for Vaccine Efficacy Parameters

    v_eff = 0.6 # Vaccine efficacy or effectiveness

    mask_use = 'Yes' # 100% Strict Mask Use

    if mask_use == 'Yes':
        R0 = R0_input - (R0_input * 0.258)
    else:
        R0 = R0_input
    
    model = IdmComp(
        N=N_in,
        time=t_duration,
        R0=R0,
        t_inc=t_incubation,
        t_inf=t_infection,
        eff=v_eff
    )

    duration, alpha, beta, gamma, c_s = model.idm_rates()

    herd_im = round(model.herd_im(), 2) # Vaccine Coverage to achieve herd immunity. Hindi ito input and need itong ipakita sa frontend.
    
    cov_val = herd_im # ito ay input from the form, vaccine coverage rin, default value yung herd_im 

    y_in = model.initial_state_seirv(
        E_in=E_in,
        I_in=I_in,
        R_in=R_in,
        p=cov_val
    )

    # Define the SEIRV model function:

    def SEIRV_model(y, N, time, beta, alpha, gamma, c_s):
        S, E, I, R, V = y
        lmbda = beta*I/N

        dS = -lmbda*S
        dE = lmbda*S - alpha*E + c_s*lmbda*V
        dI = alpha*E - gamma*I
        dR = gamma*I
        dV = -c_s*lmbda*V

        return dS, dE, dI, dR, dV
    
    # Solve the Ordinary Differential Equations:

    output = odeint(func=SEIRV_model, y0=y_in, t=duration, args=(N_in, beta, alpha, gamma, c_s))
    S, E, I, R, V = output.T
    output_df = pd.DataFrame(output)
    output_df = output_df.rename(
        columns={
            0: 'S',
            1: 'E',
            2: 'I',
            3: 'R',
            4: 'V'
        }
    )
    output_df.index = output_df.index + 1
    output_df['Days'] = output_df.index
    output_df = output_df.apply(np.ceil)

    model_plot_seirv = []

    # Plot of Susceptible (S)
    model_plot_seirv.append(
        go.Scatter(
            x=output_df['Days'],
            y=output_df['S'],
            legendgroup=1,
            name='Susceptible'
        )
    )

    # Plot of Exposed (E)
    model_plot_seirv.append(
        go.Scatter(
            x=output_df['Days'],
            y=output_df['E'],
            legendgroup=1,
            name='Exposed'
        )
    )

    # Plot of Infected (I)
    model_plot_seirv.append(
        go.Scatter(
            x=output_df['Days'],
            y=output_df['I'],
            legendgroup=1,
            name='Infected'
        )
    )

    # Plot of Recovered (R)
    model_plot_seirv.append(
        go.Scatter(
            x=output_df['Days'],
            y=output_df['R'],
            legendgroup=1,
            name='Recovered'
        )
    )

    # Plot of Vaccinated (V)
    model_plot_seirv.append(
        go.Scatter(
            x=output_df['Days'],
            y=output_df['V'],
            legendgroup=1,
            name='Vaccinated ({}% of N)'.format(cov_val)
        )
    )
    # Update graph layout
    
    layout = {
        'title' : f'SEIRV Model Projection <br> (Vaccine Coverage = {cov_val * 100}%, Vaccine Efficacy = {v_eff * 100}%',
        'xaxis_title': 'Time (Days)',
        'yaxis_title': 'Population',
        'height': 500,
        'width': 600
    }

    # Getting the HTML needed to render the plot.

    plot_seirv = plot(
        {
            'data': model_plot_seirv,
            'layout': layout
        },
        output_type='div'
    )

    # Getting the HTML needed to render the dataframe

    table_frame_seirv = output_df.reset_index().to_json(orient = 'records')
    table_seirv = json.loads(table_frame_seirv)

    y_in_seir = model.initial_state_seir(
        E_in=E_in,
        I_in=I_in,
        R_in=R_in
    )

    # Define SEIR model function:

    def SEIR_model(y, N, time, beta, alpha, gamma):
        S, E, I, R = y
        lmbda = beta*I/N

        dS = -lmbda*S
        dE = lmbda*S - alpha*E
        dI = alpha*E - gamma*I
        dR = gamma*I

        return dS, dE, dI, dR

    # Solve the ordianry differential equations:

    output2 = odeint(func=SEIR_model, y0=y_in_seir, t=duration, args=(N_in, beta, alpha, gamma))
    S, E, I, R = output2.T
    output2_df = pd.DataFrame(output2)
    output2_df = output2_df.rename(
        columns={
            0: 'S',
            1: 'E',
            2: 'I',
            3: 'R'
        }
    )

    output2_df.index = output2_df.index+1
    output2_df['Days'] = output2_df.index
    output2_df = output2_df.apply(np.ceil)

    model_plot_seir = []
    
    # Plot of Susceptible (S)
    model_plot_seir.append(
        go.Scatter(
            x=output2_df['Days'],
            y=output2_df['S'],
            legendgroup=1,
            name='Susceptible'
        )
    )

    # Plot of Exposed (E)
    model_plot_seir.append(
        go.Scatter(
            x=output2_df['Days'],
            y=output2_df['E'],
            legendgroup=1,
            name='Exposed'
        )
    )

    # Plot of Infected (I)
    model_plot_seir.append(
        go.Scatter(
            x=output2_df['Days'],
            y=output2_df['I'],
            legendgroup=1,
            name='Infected'
        )
    )

    # Plot of Recovered (R)
    model_plot_seir.append(
        go.Scatter(
            x=output2_df['Days'],
            y=output2_df['R'],
            legendgroup=1,
            name='Recovered'
        )
    )

    layout = {
        'title' : f'SEIR Model Projection <br> (Zero or Negligible Vaccine Coverage)',
        'xaxis_title': 'Time (Days)',
        'yaxis_title': 'Population',
        'height': 500,
        'width': 600
    }

    plot_seir = plot(
        {
            'data': model_plot_seir,
            'layout': layout
        },
        output_type='div'
    )

    # Getting the HTML needed to render the dataframe

    table_frame_seir = output2_df.reset_index().to_json(orient = 'records')
    table_seir = json.loads(table_frame_seir)

    return plot_seirv, table_seirv, plot_seir, table_seir

def dengue(N_h, N_v, t_duration, bite_n, bv_input, bh_input, uv_input, h_recov_input):

    #N_h = 1000 # N (host population)

    #N_v = 2000 # N (vector population: mosquitos)

    #t_duration = 100 # Simulation duration (in days)

    #bite_n = 1 # Number of hosts a mosquito bite in a day

    #bv_input = 0.4 # Probability of infection (host to vector)

    #bh_input = 0.4 # Probability of infection (vector to host)

    #uv_input = 0.25 # Vector mortality rate

    #h_recov_input = 0.167 # Recovery rate from dengue in humans

    
    # Create model for dengue using the DengueComp class from IdmComp

    model = DengueComp(
        Nv = N_v,
        Nh = N_h,
        time = t_duration,
        t_bite = bite_n,
        bv = bv_input,
        bh = bh_input,
        uv = uv_input,
        h_recov = h_recov_input
    )

    duration, bite_rate, bv, bh, uv, h_recov = model.dengue_rates()


    # Initial State Inputs:

    Ih_in = 1 # Initial infected host population

    Rh_in = 0 # Initial recovered host population

    Iv_in = 1 # Initial infected vector population

    y_in_dengue = model.initial_state_dengue(
        Ih_in=Ih_in,
        Rh_in=Rh_in,
        Iv_in=Iv_in
    )
    
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
    output_df = output_df.rename(
        columns={  
            0: 'Sh',
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
    model_plot.append(
        go.Scatter(
            x=output_df['Days'],
            y=output_df['Sh'],
            legendgroup=1,
            name='Susceptible Host'
        )
    )

    # Plot of Infected host (Ih)
    model_plot.append(
        go.Scatter(
            x=output_df['Days'],
            y=output_df['Ih'],
            legendgroup=1,
            name='Infected Host'
        )
    )
    
    # Plot of Recovered (Rh)
    model_plot.append(
        go.Scatter(
            x=output_df['Days'],
            y=output_df['Rh'],
            legendgroup=1,
            name='Recovered Host'
        )
    )

    # Plot of Susceptible vector (Sv)
    model_plot.append(
        go.Scatter(
            x=output_df['Days'],
            y=output_df['Sv'],
            legendgroup=1,
            name='Susceptible Vector'
        )
    )
    
    # Plot of Infected vector (Iv)
    model_plot.append(
        go.Scatter(
            x=output_df['Days'],
            y=output_df['Iv'],
            legendgroup=1,
            name='Infected Vector'
        )
    )
    
    # Update graph layout
    
    layout = {
        'title' : 'Ross Macdonald Model Projection for Dengue <br> (Vector = Aedes aegypti Mosquito)',
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

    return plot_div, table