# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
from app import app


# Read in 3T study list data
data_fn = 'assets/multiecho_study_list_3T.csv'
dataframe = pd.read_csv(data_fn, converters={i: str for i in range(0, 100)})
df = dataframe.copy()
df = df.drop(columns=['title', 'vols_from_single_run', 'duration_of_one_run', 'Paper Focus', 'Analysis Method', 'Notes'])

# Replace 'doi' column values with markdown link to actual doi
for index, row in df.iterrows():
    doi = row['doi']
    doi_link = '[' + doi + ']' + '(' + doi + ')'
    row['doi'] = doi_link


table_cols = ['authors', 'year', 'doi', 'field_strength', 'manufacturer', 'x', 'y', 'z', 'number_of_slices', 'slice_gap', 'TR', 'TE1', 'TE2', 'TE3', 'TE4', 'TE5', 'TE6', 'multiband_factor', 'in_plane_accel', 'in_plane_method', 'bandwidth', 'pF', 'flip_angle', 'receive_channels']

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


# # Get data
# filename = 'assets/rtfMRI_methods_review_included_studies_procsteps.txt'
# df_studies = pd.read_csv(filename, sep='\t', lineterminator='\r')
# df_studies = df_studies.dropna(axis='columns')
# df_plot = df_studies.copy()

# colnames = {
#     'author':'Author',
#     'vendor': 'Vendor',
#     'magnet': 'Field strength',
#     'software': 'Software',
#     'stc': 'Slice time correction',
#     'mc': '3D volume realignment',
#     'ss': 'Spatial smoothing',
#     'dr': 'Drift removal',
#     'hmp': 'Realignment parameter regression',
#     'ts': 'Temporal smoothing',
#     'ff': 'Frequency filtering',
#     'or': 'Outlier removal',
#     'droi': 'Differential ROI',
#     'resp': 'Respiratory noise removal',
#     'doi': 'Article DOI'
# }

# plotnames = [
#     {'label': 'Vendor', 'value': 'vendor'},
#     {'label': 'Field strength', 'value': 'magnet'},
#     {'label': 'Software', 'value': 'software'},
#     {'label': 'Slice time correction', 'value': 'stc'},
#     {'label': '3D volume realignment', 'value': 'mc'},
#     {'label': 'Spatial smoothing', 'value': 'ss'},
#     {'label': 'Drift removal', 'value': 'dr'},
#     {'label': 'Realignment parameter regression', 'value': 'hmp'},
#     {'label': 'Temporal smoothing', 'value': 'ts'},
#     {'label': 'Frequency filtering', 'value': 'ff'},
#     {'label': 'Outlier removal', 'value': 'or'},
#     {'label': 'Differential ROI', 'value': 'droi'},
#     {'label': 'Respiratory noise removal', 'value': 'resp'},
# ]

# # Replace 'doi' column values with markdown link to actual doi
# for index, row in df_studies.iterrows():
#     doi = row['doi']
#     doi_link = '[' + doi + ']' + '(https://doi.org/' + doi + ')'
#     row['doi'] = doi_link



main_md = dcc.Markdown('''

The table below contains a list of studies coded for multi-echo fMRI protocol and usage parameters.
You can filter through these studies to find what you are looking for. You can click on the `DOI` link to view the article online.


''')


layout = html.Div([
            html.Div(
                html.H2('Browse'),
                style={
                    'marginBottom': 25,
                    'marginTop': 25,
                    'marginLeft': '5%',
                    'maxWidth': '90%',
                    'textAlign': 'center'
                }
            ),
            html.Div(
                main_md,
                style={
                    'marginLeft': '5%',
                    'maxWidth': '90%',
                }
            ),
            html.Br([]),
            html.Div([
                dcc.Input(id='my-id', value='', type='text',
                    placeholder='Enter a search term...',
                    style={
                        'marginBottom': 0,
                        'marginTop': 0,
                        'width': '40%',
                    }
                )],
                style={
                    'marginBottom': 25,
                    'marginTop': 25,
                    'marginLeft': '5%',
                    'maxWidth': '90%',
                    'textAlign': 'center'
                }
            ),

            dash_table.DataTable(
                id='table',
                columns=[{"name": colnames[i], "id": i, "presentation": "markdown"} for i in df.columns],
                data=df.to_dict('records'),
                style_table={
                    # 'overflowX': 'scroll',
                             'marginLeft': '5%',
                             'maxWidth': '90%',},
                fixed_columns={ 'headers': True, 'data': 0 },
                style_header={
                    'textAlign': 'center',
                    'backgroundColor': '#1E8ED7',
                    'fontWeight': 'bold',
                    'color': '#1FFFFFF',
                },
                style_cell={
                    'height': 'auto',
                    # 'minWidth': '0px', 'maxWidth': '150px',
                    'whiteSpace': 'normal',
                    'padding': '4px',
                    'fontSize': '12px',
                    'textAlign': 'left',
                    'fontFamily': 'Trebuchet MS',

                    # all three widths are needed
                    'minWidth': '70px', 'width': '70px', 'maxWidth': '70px',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                },
                style_cell_conditional=[
                    {'if': {'column_id': 'authors'},
                     'minWidth': '130px', 'width': '130px', 'maxWidth': '130px'},
                    {'if': {'column_id': 'doi'},
                     'minWidth': '130px', 'width': '130px', 'maxWidth': '130px' },
                ],
                filter_action="native",
                sort_action="native",
                sort_mode="multi",
                # css= [{'selector': 'table', 'rule': 'table-layout: fixed;'}]
            )
])


# Callback for table search function
@app.callback(
    Output('table', 'data'),
    [Input(component_id='my-id', component_property='value')]
)
def update_output_div(input_value):

    mask = np.column_stack([df[col].str.contains(input_value, case=False, regex=False, na=False) for col in df])
    df_new = df.loc[mask.any(axis=1)]
    data = df_new.to_dict('records')

    return data
