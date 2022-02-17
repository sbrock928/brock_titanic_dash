from dash import dcc
from dash import html
from dash import dash_table
import dash_daq as daq
import dash_bootstrap_components as dbc

from app import app
from apps import query

data_df = query.queryData()

detail_table = dash_table.DataTable(id='detail_table',
                                    columns=[{"name": i, "id": i} for i in data_df],
                                    data=data_df.to_dict('records'),
                                    page_size=10,
                                    style_table={'overflowX': 'auto',
                                                 'border': '3px solid black'},
                                    style_header={'textAlign': 'left',
                                                  'fontWeight': 'bold',
                                                  'backgroundColor': '#3B3331',
                                                  'color': 'white'},
                                    style_cell={'padding-left': '0px',
                                                'textAlign': 'left',
                                                'overflow': 'hidden',
                                                'textOverflow': 'ellipsis',
                                                'color': 'black',
                                                'minWidth': '10px',
                                                'width': '10px',
                                                'maxWidth': '250px'},
                                    style_as_list_view=True,
                                    sort_action='native')

summary = html.Div([

    html.H2('Stephen Brock | Titanic Dataset',
                     style={'padding-left': 25,
                            'padding-top': 10,
                            'padding-bottom': 5,
                            'background-color': '#FF0000',
                            'color': 'white',
                            'border-bottom': 'black'}),

    dbc.Container([
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(id='metric_select',
                             options=[{'label': 'Passenger Count', 'value': 'Passenger_Count'},
                                      {'label': 'Ticket Price Average', 'value': 'Price_Average'}],
                             clearable=False,
                             value='Passenger_Count')
            ], width=3),
            dbc.Col(
                daq.BooleanSwitch(id='toggle_switch',
                                  on=False,
                                  label="Survivors Only",
                                  labelPosition="top",
                                  style={'float': 'left', 'font-weight': 'bold'})
            )
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(id='embark_select',
                             options=[{'label': 'Cherbourg', 'value': 'Cherbourg'},
                                      {'label': 'Queenstown', 'value': 'Queenstown'},
                                      {'label': 'Southampton', 'value': 'Southampton'}],
                             multi=True,
                             placeholder='Select Embark Location (empty defaults to all)',
                             value=['Cherbourg', 'Queenstown', 'Southampton'])
            ], width=3),
        ], style={'padding-top': '10px'}),
        dbc.Row(
            dbc.Tabs([
                dbc.Tab([
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardHeader("Gender Breakout"),
                                dbc.CardBody([dcc.Graph(id='gender_bar', config={'displayModeBar': False})])
                            ])
                        ], width=6),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardHeader("Class Breakout"),
                                dbc.CardBody(dcc.Graph(id='class_bar', config={'displayModeBar': False}))
                            ])
                        ], width=6)
                    ], style={'padding-top': '10px', 'padding-bottom': '10px'})
                ], label='Summary')
            ], style={'margin-left': '10px', 'padding-top': '10px'})
        ),
        dbc.Row(detail_table)
    ], fluid=True)
])








