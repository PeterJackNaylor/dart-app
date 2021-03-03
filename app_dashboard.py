
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import dash_table
import json

from utils.plot_geojson import dart_plot
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}


fig = dart_plot()
## registered players
df_players = pd.read_csv("ressources/players.csv")
df_darts = pd.read_csv('ressources/mapping_dart_geojson.csv')


app.layout = html.Div([
    
    html.Label('Name '),
    dcc.Input(
        id = 'new-player',
        placeholder = 'If you are a new player, input your name',
        type = 'text',
        value = ''
        ),
    html.Button('Register name', id='submit-val', n_clicks=0),



    # dash_table.DataTable(
    #     id='table',
    # columns=[{"name": i, "id": i} for i in df.columns],
    # data=df.to_dict('records'),

    dcc.Graph(
        id='basic-interactions',
        figure=fig
    ),
    
    html.Div(className='row', children=[
        html.Div([
            dcc.Markdown("""
                *Hover Data*

                Mouse over values in the graph.
            """),
            html.Pre(id='hover-data', style=styles['pre'])
        ], className='three columns'),

        html.Div([
            dcc.Markdown("""
                *Click Data*

                Click on points in the graph.
            """),
            html.Pre(id='click-data', style=styles['pre']),
        ], className='three columns'),

        html.Div([
            dcc.Markdown("""
                *Selection Data*

                Choose the lasso or rectangle tool in the graph's menu
                bar and then select points in the graph.

                Note that if `layout.clickmode = 'event+select'`, selection data also
                accumulates (or un-accumulates) selected data if you hold down the shift
                button while clicking.
            """),
            html.Pre(id='selected-data', style=styles['pre']),
        ], className='three columns'),

        html.Div([
            dcc.Markdown("""
                *Zoom and Relayout Data*

                Click and drag on the graph to zoom or click on the zoom
                buttons in the graph's menu bar.
                Clicking on legend items will also fire
                this event.
            """),
            html.Pre(id='relayout-data', style=styles['pre']),
        ], className='three columns')
    ])
])


# @app.callback(
#     Output('table_players', 'children'),
#     [Input('submit-val', 'n_clicks')],
#     [State('new-player', 'value')])
# def update_output(n_clicks, value):
#     last_index = df_players.shape[0]
#     print('ha')
#     last_id = df_players["id_ref"].max()
#     print('he')
#     df_players.loc[last_index + 1, "id_ref"] = last_id + 1
#     print('hi')
#     df_players.loc[last_index + 1, "id_ref"] = value
#     print('ho')
#     return df_players

@app.callback(
    Output('hover-data', 'children'),
    Input('basic-interactions', 'hoverData'))
def display_hover_data(hoverData):
    return json.dumps(hoverData, indent=2)


@app.callback(
    Output('click-data', 'children'),
    Input('basic-interactions', 'clickData'))
def display_click_data(clickData):
    coef, value = 0, 0
    if clickData is not None:
        click_Location = clickData['points'][0]['location']
        touched_polygon = df_darts.loc[df_darts["id"] == click_Location].index[0]
        value = df_darts.loc[touched_polygon, 'value']
        coef  = df_darts.loc[touched_polygon, 'coef']
    return value * coef




@app.callback(
    Output('selected-data', 'children'),
    Input('basic-interactions', 'selectedData'))
def display_selected_data(selectedData):
    return json.dumps(selectedData, indent=2)


@app.callback(
    Output('relayout-data', 'children'),
    Input('basic-interactions', 'relayoutData'))
def display_relayout_data(relayoutData):
    return json.dumps(relayoutData, indent=2)


if __name__ == '__main__':
    app.run_server(debug=True)