from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from apps.func import groupbygenderbar, groupbyclassbar
from app import app
from apps.layouts import summary
from apps import query
import pandas as pd
from dash.exceptions import PreventUpdate
from app import server


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    dcc.Store(id='intermediate-value', storage_type='memory'),
    dcc.Interval(
        id='interval-component',
        interval=30000,
        n_intervals=0
    )
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/summary' or pathname == '/summary/':
        return summary
    else:
        return summary


@app.callback(Output('intermediate-value', 'data'),
              [Input('interval-component', 'n_intervals')])
def update_data(n):
    # uncomment to prevent initial call on app launch
    #   if n is None or n==0:
    #       raise PreventUpdate
    #   else:
    data_df = query.queryData()
    return data_df.to_json(date_format='iso', orient='split')


@app.callback([Output('detail_table', 'data'),
               Output('detail_table', 'page_current'),
               Output('gender_bar', 'figure'),
               Output('class_bar', 'figure')],
              [Input('intermediate-value', 'data'),
               Input('metric_select', 'value'),
               Input('embark_select', 'value'),
               Input('toggle_switch', 'on')])
def update_figures(json_data, metric, location, toggle):
    # prevent callback from firing on startup
    if json_data is None:
        raise PreventUpdate
    else:
        temp_df = pd.read_json(json_data, orient='split')

        if location is not None and len(location) >= 1:
            temp_df = temp_df.loc[temp_df['Embarked'].isin(location)]

        if toggle == True:
            temp_df = temp_df[temp_df['Survived'] == 1]

        if metric == 'Passenger_Count':
            gender_breakout_bar = groupbygenderbar(temp_df, 'PassengerID', 'count')
            class_breakout_bar = groupbyclassbar(temp_df, 'PassengerID', 'count')
        elif metric == 'Price_Average':
            gender_breakout_bar = groupbygenderbar(temp_df, 'Fare', 'average')
            class_breakout_bar = groupbyclassbar(temp_df, 'Fare', 'average')

        return temp_df.to_dict('records'), 0, gender_breakout_bar, class_breakout_bar


if __name__ == '__main__':
    app.run_server(debug=False)
