
import os
import pandas as pd
import dash_html_components as html
from dash.dependencies import Input, Output

from ..utils.pickle import open_dic

GAME_NAME = "Template"


def gen_name_teams(players, teams):
    out = ""
    for i in range(len(players)):
        p, t = players[i], teams[i]
        out += f"{p} ({t}) "
    return out

def gen_table(players, teams):
    dic = {}
    for i in range(len(players)):
        p, t = players[i], teams[i]
        dic[p] = [t] * 4
    return pd.DataFrame(dic)
import dash_table



def create_ap(app, room_number):
    local_path = f"ressources/local_games/{GAME_NAME}/{room_number}"

    
    
    def layout_temp():
        if os.path.isdir(local_path):
            dic = open_dic(os.path.join(local_path, "meta.pickle"))
        else:
            dic = {"teams": ["Blue", "Red"],
                    "picked_players": ["Peter", "Bruno"],
                    "picked_game": "Just a template"}

        string_out = gen_name_teams(dic["picked_players"],
                                dic["teams"])
        tmp = gen_table(dic["picked_players"],
                    dic["teams"])
        tab =  dash_table.DataTable(
                        id=f'table-{room_number}',
                        columns=[{"name": i, "id": i, 'deletable': True} for i in tmp.columns],
                        data=tmp.to_dict('records'),
                        row_deletable=True
                )
        return html.Div([
            html.H6("Minimal example of loading dash template"),
            html.Div("Selected players and teams"),
            html.Br(),
            html.Div(tab),
            html.Div(string_out, id=f'my-output-{room_number}'),
            html.Button("load game", id=f'submit-button-state-{room_number}',
                        n_clicks=0)])

    layout = layout_temp()

    @app.callback(
        Output(f'my-output-{room_number}', 'children'),
        Input(f'submit-button-state-{room_number}', 'n_clicks')
    )
    def update_output_div(input_value):
        dic = open_dic(os.path.join(local_path, "meta.pickle"))
        string_out = gen_name_teams(dic["picked_players"],
                                    dic["teams"])
        return string_out
    return app, layout
