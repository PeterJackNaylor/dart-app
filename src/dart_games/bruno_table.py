import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import dash_table
import json

import numpy as np

# from utils.plot_geojson import dart_plot
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# df_players = pd.read_csv("players_New.csv")

# app.layout = html.Div([

#     dash_table.DataTable(
#         id='List_Of_Existing_Players',
#         columns=[{
#             'name': df_players.columns[i],
#             'id': df_players.columns[i],
#            # 'renamable': True
#         } for i in range(0,4)],
#         data = df_players.to_dict('records'),
#         page_action='none',
#         style_table={'height': '300px', 'overflowY': 'auto'},
#         style_cell={'textAlign': 'center'},
#         #style_table={
#         #    'maxHeight': '50ex',
#         #    'width': '100%',
#         #    'minWidth': '100%',
#         #    "horizontalAlign": "bottom"
#         #    },         
#         style_header={
#                     'backgroundColor': 'rgb(230, 230, 230)',
#                     'fontWeight': 'bold'
#             },
               
                
#         editable = False,
#         selected_rows=[],
#         row_selectable="multi",
# #        filter_action="native",     # allow filtering of data by user ('native') or not ('none')

        
#         ),
    

#     ### Add a player to the above table or launch the game!
#     dcc.Input(
#         id = 'new-player',
#         placeholder = 'Player Name',
#         type = 'text',
#         value = ''
#         ),
#     html.Button('Add Player', id='editing-rows-button', n_clicks=0),
    
#     html.Button('Lancer la partie', id='Start_Game', n_clicks=0)

# ])



# ### Callback to add a player to the list of players. It is called upon when you double click on 'add player', checks that the players name doesn't already exists, then creates a file for that player and adds him to the genreal available player file. Output brings up to data the list of player table.
# @app.callback(
#     Output('List_Of_Existing_Players', 'data'),
#     Input('editing-rows-button', 'n_clicks'),
#     State('List_Of_Existing_Players', 'data'),
#     State('List_Of_Existing_Players', 'columns'),
#     State('new-player','value')
#     )

# def add_row(n_clicks, rows, columns, New_Player_Name):

#     Name_Exists = 0   
#     if n_clicks > 1 :
#         n_clicks = 0 # need to double click
        
#         for i in range (0, len(rows)):
#             if New_Player_Name == rows[i]['name']:
#                 Name_Exists = 1
#         if Name_Exists == 0:

#             rows.append({'name': New_Player_Name, '# Partie': 0, '% Victoire': None, 'Touche / Tour': None})
#             pd.DataFrame(rows).to_csv("ressources/players_New.csv",index = False)  
#             Player_file = pd.DataFrame(None,columns=['Tour','Fleche','Valeur', 'Coef', 'Degats','Touche'])
#             Player_file.to_csv('ressources/Player_Info/{}.csv'.format(New_Player_Name),index = False) 
    
#     return rows
              


def create_ap(param, url_base):

    app = dash.Dash(__name__, 
                    external_stylesheets=external_stylesheets,
                    url_base_pathname=url_base)
    df_players = pd.read_csv("ressources/players_New.csv")

    app.layout = html.Div([

        dash_table.DataTable(
            id='List_Of_Existing_Players',
            columns=[{
                'name': df_players.columns[i],
                'id': df_players.columns[i],
            # 'renamable': True
            } for i in range(0,4)],
            data = df_players.to_dict('records'),
            page_action='none',
            style_table={'height': '300px', 'overflowY': 'auto'},
            style_cell={'textAlign': 'center'},
            #style_table={
            #    'maxHeight': '50ex',
            #    'width': '100%',
            #    'minWidth': '100%',
            #    "horizontalAlign": "bottom"
            #    },         
            style_header={
                        'backgroundColor': 'rgb(230, 230, 230)',
                        'fontWeight': 'bold'
                },
                
                    
            editable = False,
            selected_rows=[],
            row_selectable="multi",
    #        filter_action="native",     # allow filtering of data by user ('native') or not ('none')

            
            ),
        

        ### Add a player to the above table or launch the game!
        dcc.Input(
            id = 'new-player',
            placeholder = 'Player Name',
            type = 'text',
            value = ''
            ),
        html.Button('Add Player', id='editing-rows-button', n_clicks=0),
        html.Button(param, id='Start_Game', n_clicks=0)

    ])
    print("PARAMETER", param)



    ### Callback to add a player to the list of players. It is called upon when you double click on 'add player', checks that the players name doesn't already exists, then creates a file for that player and adds him to the genreal available player file. Output brings up to data the list of player table.
    @app.callback(
        Output('List_Of_Existing_Players', 'data'),
        Input('editing-rows-button', 'n_clicks'),
        State('List_Of_Existing_Players', 'data'),
        State('List_Of_Existing_Players', 'columns'),
        State('new-player','value')
        )

    def add_row(n_clicks, rows, columns, New_Player_Name):

        Name_Exists = 0   
        if n_clicks > 1 :
            n_clicks = 0 # need to double click
            
            for i in range (0, len(rows)):
                if New_Player_Name == rows[i]['name']:
                    Name_Exists = 1
            if Name_Exists == 0:

                rows.append({'name': New_Player_Name, '# Partie': 0, '% Victoire': None, 'Touche / Tour': None})
                pd.DataFrame(rows).to_csv("ressources/players_New.csv",index = False)  
                Player_file = pd.DataFrame(None,columns=['Tour','Fleche','Valeur', 'Coef', 'Degats','Touche'])
                Player_file.to_csv('ressources/Player_Info/{}.csv'.format(New_Player_Name),index = False) 
        
        return rows
    return app
                

import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int,
                        help="port number")
    parser.add_argument("--url_base",
                        help="base")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="to print information")
    parser.add_argument("--param")
    args = parser.parse_args()

    app = create_ap(args.param, args.url_base)
    app.run_server(debug=False, port = args.port)