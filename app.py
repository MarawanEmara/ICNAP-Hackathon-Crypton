import datetime

import dash
from dash import dcc, html
import dash_daq as daq
import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Input, Output, State
from data_getter import *
from map_creation import *
import random

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
data = [[], []]
item_eff = [[], []]
ingredients = get_ingredients()

#map_filename = os.getcwd() + '\map.png'
#encoded_map = base64.b64encode(open(map_filename, 'rb').read())


def initial_graph():
    oee = get_current_oee()
    time = datetime.datetime.now()

    for _ in range(2):
        data[0].append(time)
        data[1].append(oee)

    fig = go.Figure(data=[go.Scatter(x=data['time'], y=data['OEE'])])
    fig.update_yaxes(range=[0, 100])
    fig.update_xaxes(range=[data['time'][0], data['time'][-1]])

    return fig


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

map_img = app.get_asset_url('map.png')
depend_img = app.get_asset_url('dependencies.png')

app.layout = html.Div([
    # html.Div(children=[html.H1('')], style={
    #         'backgroundColor': '#373837', 'height': '100px', 'width': '100%'}),
    html.Div([
        html.H1(['Factory Monitoring Dashboard'],
                style={'textAlign': 'center'}),
        # html.Div(id='live-update-text'),
        html.Div([
            daq.Gauge(
                color={"gradient": True, "ranges": {
                    "red": [0, 70], "yellow":[70, 80], "green":[80, 100]}},
                id="live-update-gauge",
                label="Current Overall Equipment Efficiency",
                value=0,
                min=0,
                max=100
            )
        ], style={}),
        html.Div([
            dcc.Graph(id='live-update-graph')
        ], style={}),
        html.H2(['Map of the Factory'],
                style={'text-align': 'center'}),
        html.Div([
            html.Img(
                 id="live-update-map",
                 height='512px',
                 width='512px',
                 # src=f'data:image/png;base64,{encoded_map}',
                 src=map_img,
                 style={'display': 'block', 'float': 'center', 'marginLeft': 'auto', 'marginRight': 'auto'}),
            html.Div([html.Button('Update Map', id='map-update-button')])
        ], style={'marginLeft': 'auto', 'marginRight': 'auto'}),
        html.H2(['High-Level Map of Machine Dependencies'],
                style={'text-align': 'center'}),
        html.Div([
            html.Img(
                 id="depend-img",
                 height='512px',
                 width='auto',
                 # src=f'data:image/png;base64,{encoded_map}',
                 src=depend_img,
                 style={'display': 'block', 'float': 'center', 'marginLeft': 'auto', 'marginRight': 'auto'}),
            html.Div(
                [html.Button('Update Dependencies', id='depend-update')], style={})
        ], style={'marginLeft': 'auto', 'marginRight': 'auto'}),
        html.Div([
            dcc.Dropdown(ingredients, placeholder='Select an item',
                         id='item-dropdown'),
            dcc.Dropdown(['consumption percentage', 'consumption', 'production'],
                         'consumption percentage', id='pc-dropdown'),
            html.H3('', id="response")
        ]),
        # dcc.Graph(figure = initial_graph()),
        dcc.Interval(
            id='interval-component',
            interval=7*1000,  # in milliseconds
            n_intervals=0
        )
    ])
], style={'margins': '0px', 'padding': '0px', 'fontFamily': 'Arial'})


""" @app.callback(Output('live-update-text', 'children'),
              Input('interval-component', 'n_intervals'))
def update_metrics(n):
    oee = get_current_oee()
    style = {'padding': '5px', 'fontSize': '16px'}
    return [
        html.Span('Overall Equipment Efficiency: {0:.2f}'.format(
            oee), style=style)
    ] """


# Multiple components can update everytime interval gets fired.
@ app.callback(Output('live-update-graph', 'figure'),
               Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    oee = get_current_oee()
    time = datetime.datetime.now()

    data[0].append(time)
    data[1].append(oee)

    fig = go.Figure(data=[go.Scatter(x=data[0], y=data[1])])
    fig.update_yaxes(range=[0, 100])
    if len(data[0]) > 15:
        fig.update_xaxes(range=[data[0][-15], data[0][-1]])
    else:
        fig.update_xaxes(range=[data[0][0], data[0][-1]])

    return fig


""" # Multiple components can update everytime interval gets fired.
@ app.callback(Output('live-item-graph', 'figure'),
               Input('interval-component', 'n_intervals'))
def update_item_eff_live(n):
    total = 65
    new_total = total + random.randrange(-total, total)/20

    item_eff[0].append(time)
    item_eff[1].append(new_total)

    fig = go.Figure(item_eff=[go.Scatter(x=item_eff[0], y=item_eff[1])])
    fig.update_yaxes(range=[0, 100])
    if len(item_eff[0]) > 15:
        fig.update_xaxes(range=[item_eff[0][-15], item_eff[0][-1]])
    else:
        fig.update_xaxes(range=[item_eff[0][0], item_eff[0][-1]])

    return fig """


@ app.callback(Output('live-update-gauge', 'value'),
               Input('interval-component', 'n_intervals'))
def update_gauge_output(n):
    return get_current_oee()


@ app.callback(Output(component_id="live-update-map", component_property='src'),
               [Input('map-update-button', 'n_clicks')])
def update_map(n_clicks):
    if n_clicks:
        print('Updating map...')
        draw_map(1000, 1000, 3)
        return app.get_asset_url('map.png')
    raise dash.exceptions.PreventUpdate


@ app.callback(Output(component_id="depend-img", component_property='src'),
               [Input('depend-update', 'n_clicks')])
def update_map(n_clicks):
    if n_clicks:
        print('Updating dependences...')
        get_dependencies()
        return app.get_asset_url('dependencies.png')
    raise dash.exceptions.PreventUpdate


@ app.callback(Output('response', 'children'),
               [Input('item-dropdown', 'value'), Input('pc-dropdown', 'value')])
def get_values(item, function):
    if(function == 'consumption percentage'):
        value = (get_current_consumption_of(item) /
                 get_current_production_of(item))*100
    if(function == 'consumption'):
        value = get_current_consumption_of(item)
    if(function == 'production'):
        value = get_current_production_of(item)
    return f'Current {function} of {item} is {value}'


if __name__ == '__main__':
    app.run_server(debug=True)
