# -*- coding: utf-8 -*-
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc


card_browse = [
    dbc.CardBody(
        [
            html.H5("Studies", className="card-title"),
            html.P(
                "This site contains a database of multti-echo fMRI studies. Their study parameters were coded into a common structure, and this site allows you to explore and link to these studies.",
                className="card-text",
            ),
            dbc.Button("Browse", color="light", href="/pages/page1", external_link=True),
        ],
    ),
]

card_visualize = [
    dbc.CardBody(
        [
            html.H5("Study parameters", className="card-title"),
            html.P(
                "To get a better understanding of multi-echo parameters employed in the studies (like the number of echos, multiband factors, and more) you can view and interact with plots of the database.",
                className="card-text",
            ),
            dbc.Button("Visualize", color="light", href="/pages/page2", external_link=True),
        ]
    ),
]

card_parameters = [
    dbc.CardBody(
        [
            html.H5("Sequence parameters", className="card-title"),
            html.P(
                "To understand the typical compromises one needs to make during acquisition of multi-echo data, here you can visualize and compare number of echoes, multislice factors, field of view, and more.",
                className="card-text",
            ),
            dbc.Button("Parameters", color="light", href="/pages/page3", external_link=True),
        ]
    ),
]

md = dcc.Markdown('''

This site is an effort to make scientific data more standardised, accessible, interactive, useful and open, in this case focusing on parameters implemented in multi-echo functional magnetic resonance imaging (fMRI) studies and acquisition sequences.
The study database, coded parameters and visualizations were curated and built by the `tedana` community. For more information about multi-echo fMRI, open source algorithms to process such data, and the community itself, please visit: [tedana.readthedocs.io](https://tedana.readthedocs.io/).


''')


layout = html.Div([

    html.H2(
        children='Multi-echo fMRI: an interactive overview of studies and parameters',
        style={
            'textAlign': 'center',
            'color': '#1E8ED7',
        }
    ),
    html.Div(
                md,
                style={
                    'marginLeft': '5%',
                    'maxWidth': '90%',
                }
            ),
    html.Br(),
    html.Div([
        dbc.Row(
            [
                dbc.Col(dbc.Card(card_browse, color="#1E8ED7", inverse=True)),
                dbc.Col(
                    dbc.Card(card_visualize, color="#1E8ED7", inverse=True)
                ),
                dbc.Col(
                    dbc.Card(card_parameters, color="#1E8ED7", inverse=True)
                ),
            ],
            className="mb-4",
        ),
        ]
    )

    # html.H2(children='Browse through literature to find and visualize studies and their methods',
    #          style={
    #     'textAlign': 'center',
    # }),



],
style={
    'marginBottom': 25,
    'marginTop': 50,
    'marginLeft': '5%',
    'maxWidth': '90%'
})
