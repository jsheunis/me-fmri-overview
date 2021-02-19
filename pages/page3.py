# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import numpy as np
from app import app
import plotly.graph_objs as go

# Get data
data_fn = 'assets/MultiEchoParameterSpace_PrismaVD11_2020_3x3x3.csv'
df = pd.read_csv(data_fn)

sms_list = ["SMS = 1", "SMS = 2", "SMS = 3", "SMS = 4"]
sms_vals = [{'label': sms_list[i], 'value': i+1} for i in range(4)]

grappa_list = ["6/8ths GRAPPA = 1", "GRAPPA = 1", "GRAPPA = 2", "GRAPPA = 3", "GRAPPA = 4"]
grappa_vals = [{'label': grappa_list[i], 'value': i} for i in range(5)]

brain_list = ['Cortex', 'Brain']
brain_vals = [{'label': "Cortex", 'value': 0},
              {'label': "Brain", 'value': 1}
             ]

fig = go.Figure()
slice_thresh = 35

main_md = dcc.Markdown('''

A very frequent question from people who are new to multi-echo fMRI is *"what compromises do I need to make during acquisition to get multi-echo data?"*
The purpose of this section is to allow you explore tradeoffs between multi-echo sequence parameters.
GRAPPA factors and field-of-view can be updated using the dropdown and radio buttons (respectively), and the resulting possibilities for repetition time (TR, in milliseconds), number of echoes, and simultaneous multislice (SMS) settings will be plotted dynamically.

''')

layout = html.Div([
    html.H2('Sequence parameters',
    style={
        'textAlign': 'center',
        'marginBottom': 25,
        'marginTop': 25,
    }),
    main_md,
    html.Br([]),
    html.Div([
        dbc.Row([
            dbc.Col([
                html.Br([]),
                html.Br([]),
                dbc.Row(dbc.Col([
                    # dbc.Label('Participant'),
                    dcc.Dropdown(
                        id='drop1',
                        options=grappa_vals,
                        value=0,
                    )],
                )),
                html.Br([]),
                dbc.Row(dbc.Col([
                    # dbc.Label('Task'),
                    dbc.RadioItems(
                        options=brain_vals,
                        value=0,
                        id="radio1",
                        inline=True,
                    )],
                )),
            ], width={"size": 3, "offset": 0}),
            dbc.Col([

                dcc.Graph(figure=fig, id='fig')],
                style={
                    'textAlign': 'left',
                },
                width={"size": 9, "offset": 0}
            ),
        ]),
    ])
],
style={
    'marginBottom': 25,
    'marginTop': 25,
    'marginLeft': '5%',
    'maxWidth': '90%',
})

# Callback for updating tsnr html and figure based on drop1, radio1, radio2 values
@app.callback(
    Output('fig', 'figure'),
    [Input('drop1','value'),
     Input('radio1','value')]
)
def reset_tsnr_imgs(grappa_val, region):
    if grappa_val == 0:
        grappa = 1
        partial_fourier = '6/8ths'
    else:
        grappa = grappa_val
        partial_fourier = 'off'
        
    if region == 0:
        new_df = df[(df["Inslice Accel"] == grappa) & (df["Slices"] < slice_thresh) & (df["Partial Fourier"] == partial_fourier)]
    else:
        new_df = df[(df["Inslice Accel"] == grappa) & (df["Slices"] > slice_thresh) & (df["Partial Fourier"] == partial_fourier)]

    multislice_accel = np.unique(new_df["Multislice Accel"].to_numpy())
    data = []
    for c, sms in enumerate(multislice_accel):
        df_plotC = new_df[new_df["Multislice Accel"]==sms]
        xC = df_plotC["Number of Echos"].to_numpy()
        yC = df_plotC["TR"].to_numpy()
        d = go.Scatter(x=xC, y=yC, mode='lines+markers', name=f"SMS={sms}")
        data.append(d)

    layout = go.Layout(title=f"{grappa_list[grappa_val]}, {brain_list[region]}",
            xaxis=dict(title='Number of Echos'),
            yaxis=dict(title='TR in ms', range=[0, 13000]))
    
    fig = go.Figure(data=data, layout=layout)
    
    return fig