# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import pandas as pd
from app import app

# Get data
data_fn = 'assets/multiecho_study_list_3T.csv'
dataframe = pd.read_csv(data_fn, converters={i: str for i in range(0, 100)})
df = dataframe.copy()
df = df.drop(columns=['title', 'vols_from_single_run', 'duration_of_one_run', 'Paper Focus', 'Analysis Method', 'Notes'])
df_plot = df.copy()

colnames = {
    'authors':'Authors',
    'year': 'Year',
    'doi': 'Article DOI',
    'field_strength': 'Field strength',
    'manufacturer': 'Manufacturer',
    'x': 'Voxel X',
    'y': 'Voxel Y',
    'z': 'Voxel Z',
    'number_of_slices': 'Nr of Slices',
    'slice_gap': 'Slice Gap',
    'TR': 'Repetition Time',
    'TE1': 'Echo 1',
    'TE2': 'Echo 2',
    'TE3': 'Echo 3',
    'TE4': 'Echo 4',
    'TE5': 'Echo 5',
    'TE6': 'Echo 6',
    'number_of_echoes': 'Nr of Echoes',
    'multiband_factor': 'MB Factor',
    'in_plane_accel': 'in_plane_accel',
    'in_plane_method': 'in_plane_method',
    'bandwidth': 'Bandwidth',
    'pF': 'pF',
    'flip_angle': 'flip_angle',
    'receive_channels': 'receive_channels'
}
plotnames = [
    {'label': 'Year', 'value': 'year'},
    {'label': 'Manufacturer', 'value': 'manufacturer'},
    {'label': 'Nr of Slices', 'value': 'number_of_slices'},
    {'label': 'Nr of Echoes', 'value': 'number_of_echoes'},
    {'label': 'MB Factor', 'value': 'multiband_factor'},
    {'label': 'In-plane acceleration', 'value': 'in_plane_accel'},
    {'label': 'In-plane method', 'value': 'in_plane_method'},
]

srs = df_plot['year'].value_counts()
xx = srs.index.to_list()
yy = srs.values

dataframe = df_plot.loc[df_plot['year'] == '2016']
srs2 = dataframe['manufacturer'].value_counts()
xx2 = srs2.index.to_list()
yy2 = srs2.values


main_md = dcc.Markdown('''

In this section you can visualize and interact with the coded data from the multi-echo studies.
There are two plots below, for which you can display data of a method selected from the respective dropdowns.

Say you want to view the distribution of scanner manufacturers used in these studies, select the `Manufacturer` option for the plot on the left hand side.
You can then *hover* over each of the bars in the plot to see the actual number of studies per manufacturer.
You can also *click* on the bar to display these specific studies in a table below the plots.

Say, now, that you want to see which multiband factors were used for each of the manufacturers, select the `MB Factor` option for the plot on the right hand side.
By hovering over each bar on the `Manufacturer` plot, the `MB Factor` plot will update with the relevant distribution.

''')

layout = html.Div([
            html.Div([
                html.H2('Visualize'),
                ],
                style={
                    'marginBottom': 25,
                    'marginTop': 25,
                    'marginLeft': '5%',
                    'maxWidth': '90%',
                    'textAlign': 'center'
                }
            ),
            html.Div(main_md,
                style={
                    'marginLeft': '5%',
                    'maxWidth': '90%',
                }
            ),
            html.Br([]),
            html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(dcc.Dropdown(
                                id='drop-1',
                                options=plotnames,
                                value='year',
                                ),
                                width={"size": 4, "offset": 1}, # figure out offset
                            ),
                            dbc.Col(dcc.Dropdown(
                                id='drop-2',
                                options=plotnames,
                                value='manufacturer',
                                ),
                                width={"size": 4, "offset": 2},
                            ),
                        ],
                        justify="start"
                    ),
                    html.Br([]),
                    dbc.Row(
                        [
                            dbc.Col(html.H6(
                                id='graph-1-title',
                                children='Year (hover to show options of second feature; click to display studies)',
                                style={
                                    'textAlign': 'center',
                                }),
                                # width={"size": 6, "offset": 3}
                            ),
                            dbc.Col(html.H6(
                                id='graph-2-title',
                                children='Manufacturer options when Year = 2016',
                                style={
                                    'textAlign': 'center',
                                }),
                                # width={"size": 6, "offset": 3}
                            )
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(html.Div(
                                dcc.Graph(
                                    id='graph-1',
                                    figure={
                                        'data': [
                                            {'x': xx, 'y': yy, 'type': 'bar', 'name': 'Year', 'marker': {'color': '#9EBC9F'}},
                                        ],
                                    }
                                ),
                            )),
                            dbc.Col(html.Div(
                               dcc.Graph(
                                id='graph-2',
                                    figure={
                                        'data': [
                                            {'x': xx2, 'y': yy2, 'type': 'bar', 'name': 'Manufacturer', 'marker': {'color': '#D3B88C'}},
                                        ],
                                    }
                                ),
                            )),
                        ]
                    ),
                ],
                style={
                    'marginBottom': 25,
                    'marginTop': 25,
                    'marginLeft': '5%',
                    'maxWidth': '90%',
                }
            ),
            html.Div(
                id='table-1',
                style={
                    'marginBottom': 25,
                    'marginTop': 25,
                    'marginLeft': '5%',
                    'maxWidth': '90%',
                }
            )
])

# Callback for updating graph 1
@app.callback(
    [Output('graph-1', 'figure'),
     Output('graph-1-title', 'children')],
    [Input('drop-1','value')]
)
def update_graph(feature):

    srs = df_plot[feature].value_counts()
    xx = srs.index.to_list()
    yy = srs.values
    txt = colnames[feature]

    fig={
        'data': [
            {'x': xx, 'y': yy, 'type': 'bar', 'name': txt, 'marker': {'color': '#9EBC9F'}},
        ],
    }

    title = txt + ' (hover to show options of second feature; click to display studies)'

    return [fig, title]

# Callback for updating dropdown2 based on dropdown1 value
@app.callback(
    [Output('drop-2', 'options'),
     Output('drop-2', 'value')],
    [Input('drop-1','value')]
)
def reset_dropdown2_opts(value):
    plotnames_2 = [x for x in plotnames if x['value'] != value]
    value_2 = plotnames_2[0]['value']
    return plotnames_2, value_2


# Callback for updating graph 2 based on graph1 hoverData and dropdowns
@app.callback(
    [Output('graph-2', 'figure'),
     Output('graph-2-title', 'children')],
    [Input('graph-1', 'hoverData'),
     Input('drop-1','value'),
     Input('drop-2','value')]
)
def update_graph(hoverData, feature1, feature2):
    if hoverData is None or feature1 is None or feature2 is None:
        raise PreventUpdate
    else:
        x = hoverData['points'][0]['x']
        dataframe = df_plot.loc[df_plot[feature1] == str(x)]
        srs = dataframe[feature2].value_counts()
        xx = srs.index.to_list()
        yy = srs.values
        txt = str(colnames[feature2]) + ' options when ' + str(colnames[feature1]) + ' = ' + str(x)

        fig={
            'data': [
                {'x': xx, 'y': yy, 'type': 'bar', 'name': txt, 'marker': {'color': '#D3B88C'}},
            ],
        }

        title = txt

        return [fig, title]


# Callback for showing table 1 after filtering on feature 1
@app.callback(
    Output('table-1', 'children'),
    [Input('graph-1', 'clickData'),
     Input('drop-1','value')])
def generate_table(clickData, feature, max_rows=20):

    if clickData is None:
        raise PreventUpdate
    else:
        x = clickData['points'][0]['x']

        dataframe = df_plot.loc[df_plot[feature] == str(x)]
        table=html.Table([
            html.Thead(
                html.Tr([html.Th(colnames[col]) for col in df.columns], style={}),
                style={
                  'border': '1px solid',
                  'padding': '4px',
                  'max-width': '150px',
                  'padding-top': '12px',
                  'padding-bottom': '12px',
                  'text-align': 'center',
                  'background-color': '#1E8ED7',
                  'color': 'white',
                }
            ),
            html.Tbody([
                html.Tr([
                    html.Td(writeElement(i, col, dataframe), style={'border': '1px solid', 'padding': '4px', 'max-width': '150px', 'min-width': '60px', 'overflow': 'hidden', 'whiteSpace': 'nowrap'}) for col in dataframe.columns],
                style={
                  'border': '1px solid',
                  'padding': '4px',
                  'max-width': '150px',
                  'padding-top': '12px',
                  'padding-bottom': '12px',
                  'text-align': 'center',
                }
                ) for i in range(min(len(dataframe), max_rows))
            ]),
            ],
            style={'borderCollapse': 'collapse',
                      'width': '90%',
                      'fontSize': '12px',
            }
        )

        # class="table-row" data-href="http://tutorialsplane.com"

        heading=html.H4('Showing studies where ' + str(colnames[feature]) + ' = ' + str(x),
                        style={'textAlign': 'center',})

        # table = dbc.Table.from_dataframe(dataframe,
        #                                  striped=True,
        #                                  bordered=True,
        #                                  hover=True,
        #                                  responsive=True,
        #                                  className='qcsummary'
        #                                  )

        return [heading, table]


def writeElement(i, col, dataframe):
    if col == 'doi':
        hrf = 'https://doi.org/'+dataframe.iloc[i][col]
        return html.A([dataframe.iloc[i][col]], href=hrf, target="_blank")
    else:
        return dataframe.iloc[i][col]


# # Callback for updating graph 1
# @app.callback(
#     [Output('graph-1', 'figure'),
#      Output('graph-1-title', 'children')],
#     [Input('drop-1','value')]
# )
# def update_graph(feature):

#     srs = df_plot[feature].value_counts()
#     xx = srs.index.to_list()
#     yy = srs.values
#     txt = colnames[feature]

#     fig={
#         'data': [
#             {'x': xx, 'y': yy, 'type': 'bar', 'name': txt, 'marker': {'color': '#9EBC9F'}},
#         ],
#     }

#     title = txt + ' (hover to show options of second feature; click to display studies)'

#     return [fig, title]

# # Callback for updating dropdown2 based on dropdown1 value
# @app.callback(
#     [Output('drop-2', 'options'),
#      Output('drop-2', 'value')],
#     [Input('drop-1','value')]
# )
# def reset_dropdown2_opts(value):
#     plotnames_2 = [x for x in plotnames if x['value'] != value]
#     value_2 = plotnames_2[0]['value']
#     return plotnames_2, value_2


# # Callback for updating graph 2 based on graph1 hoverData and dropdowns
# @app.callback(
#     [Output('graph-2', 'figure'),
#      Output('graph-2-title', 'children')],
#     [Input('graph-1', 'hoverData'),
#      Input('drop-1','value'),
#      Input('drop-2','value')]
# )
# def update_graph(hoverData, feature1, feature2):
#     if hoverData is None or feature1 is None or feature2 is None:
#         raise PreventUpdate
#     else:
#         x = hoverData['points'][0]['x']
#         dataframe = df_plot.loc[df_plot[feature1] == x]
#         srs = dataframe[feature2].value_counts()
#         xx = srs.index.to_list()
#         yy = srs.values
#         txt = colnames[feature2] + ' options when ' + colnames[feature1] + ' = ' + x

#         fig={
#             'data': [
#                 {'x': xx, 'y': yy, 'type': 'bar', 'name': txt, 'marker': {'color': '#D3B88C'}},
#             ],
#         }

#         title = txt

#         return [fig, title]


# # Callback for showing table 1 after filtering on feature 1
# @app.callback(
#     Output('table-1', 'children'),
#     [Input('graph-1', 'clickData'),
#      Input('drop-1','value')])
# def generate_table(clickData, feature, max_rows=20):

#     if clickData is None:
#         raise PreventUpdate
#     else:
#         x = clickData['points'][0]['x']

#         dataframe = df_plot.loc[df_plot[feature] == x]
#         table=html.Table([
#             html.Thead(
#                 html.Tr([html.Th(col) for col in list(colnames.values())])
#             ),
#             html.Tbody([
#                 html.Tr([
#                     html.Td(writeElement(i, col, dataframe)) for col in dataframe.columns],
#                 ) for i in range(min(len(dataframe), max_rows))
#             ]),
#             ],
#             className='qcsummary',
#         )

#         # class="table-row" data-href="http://tutorialsplane.com"

#         heading=html.H4('Showing studies where ' + colnames[feature] + ' = ' + x,
#                         style={'textAlign': 'center',})

#         # table = dbc.Table.from_dataframe(dataframe,
#         #                                  striped=True,
#         #                                  bordered=True,
#         #                                  hover=True,
#         #                                  responsive=True,
#         #                                  className='qcsummary'
#         #                                  )

#         return [heading, table]


# def writeElement(i, col, dataframe):
#     if col == 'doi':
#         hrf = 'https://doi.org/'+dataframe.iloc[i][col]
#         return html.A([dataframe.iloc[i][col]], href=hrf, target="_blank")
#     else:
#         return dataframe.iloc[i][col]

