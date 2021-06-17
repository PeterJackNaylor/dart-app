import pandas as pd

import dash_core_components as dcc
import dash_html_components as html
import dash_table

from ..utils.plot_geojson import dart_plot
from .aux import (
    load_local_dictionnary,
    init_db,
    Column_Live_Stats,
    Column_Live_Stats_Graph,
    Column_Storage,
)
from .styles_dash import (
    align_style,
    style_table,
    style_data_conditional,
    style_data_basic,
    style_header,
    tab_style,
    score_style_table,
    tab_selected_style,
    style_data_conditional,
    style_data_cond_historic,
)

from .app_dashboard_functions import Save


def generate_tab_1(
    turn_n, dart_n, data_Fleches_Temp, Score_Table, legend  # df_Stat_Live,
):

    children = []

    var = [("Dart_Counter", dart_n)]

    for id_, data in var:
        children.append(dcc.Store(id=id_, data=data))

    #    children.append( dcc.Store(id= 'Stat_Live', data= df_Stat_Live.to_dict('records')) )

    children += [
        html.Div(
            [
                html.H1(id="Joueur", children=["Tour numero: {}".format(turn_n)]),
            ]
        )
    ]

    children += [html.Div([html.Button("Mise à jour", id="Refresh", n_clicks=0)])]

    children += [html.Button("Valider ce tour", id="submit_round", n_clicks=0)]

    children += [html.Button("Annuler ce tour", id="cancel_round", n_clicks=0)]

    children += [
        html.Button("Revenir au joueur precedent ", id="precedent_round", n_clicks=0)
    ]

    first_dash_table = [
        {"name": ["Joueur", ""], "id": "index"},
        {"name": ["Equipe", ""], "id": "Equipe"},
        {"name": ["Fleche 1", "Value"], "id": "Fleche 1"},
        {"name": ["Fleche 1", "Coef"], "id": "Coef 1"},
        {"name": ["Fleche 2", "Value"], "id": "Fleche 2"},
        {"name": ["Fleche 2", "Coef"], "id": "Coef 2"},
        {"name": ["Fleche 3", "Value"], "id": "Fleche 3"},
        {"name": ["Fleche 3", "Coef"], "id": "Coef 3"},
    ]

    live_score_table = dash_table.DataTable(
        id="Score_Live_New_Way",
        columns=first_dash_table,
        data=data_Fleches_Temp,
        style_cell=align_style,
        style_table=style_table,
        style_data_conditional=style_data_conditional(turn_n),
        style_header=style_header,
        merge_duplicate_headers=True,
    )

    tab_child_child = [html.Div(live_score_table, className="six columns")]

    current_score_table = dash_table.DataTable(
        id="Score_Table",
        #   columns=[{"name": i, "id": i} for i in df_score.columns],
        columns=[{"name": i, "id": i} for i in list(Score_Table[0].keys())],
        data=Score_Table,
        style_cell=align_style,
        style_table=score_style_table,
        # style_data_conditional=styles,
        style_header=style_header,
    )

    tab_child_child += [
        html.Div(
            [legend, current_score_table],
            # Table displaying the total score
            # (refreshes only after submission of the round)
            className="height columns",
        )
    ]

    children += [
        html.Div(html.Div(tab_child_child, className="row"), className="container")
    ]

    fig = dart_plot()

    children += [dcc.Graph(id="basic-interactions", figure=fig)]

    return children


def generate_tab_2(Stats_Table, Stats_Graph):

    children = []

    children += [
        dcc.RadioItems(
            id="Stat_RadioItems",
            options=[
                {"label": "Equipe", "value": "Stat_Equipe"},
                {"label": "Individuelle", "value": "Stat_Indiv"},
            ],
            value="Stat_Equipe",
            labelStyle={"display": "inline-block"},
        )
    ]

    children += [
        dash_table.DataTable(
            id="Stat_Table",
            columns=[{"name": i, "id": i} for i in Column_Live_Stats],
            style_cell=align_style,
            style_table=style_table,
            style_data_conditional=style_data_basic,
            style_header=style_header,
            data=Stats_Table,
        )
    ]

    children += [
        dcc.Dropdown(
            id="Stat_Dropdown",
            options=[
                {
                    "label": Column_Live_Stats_Graph[i],
                    "value": Column_Live_Stats_Graph[i],
                }
                for i in range(len(Column_Live_Stats_Graph))
            ],
            value=Column_Live_Stats_Graph[0],
        )
    ]
    children += [dcc.Graph(id="Graph_Live_Stat", animate=True, figure=Stats_Graph)]

    children += [html.Button("Mise à jour Graphiques", id="Button_Graph", n_clicks=0)]

    children += [
        dcc.Graph(
            figure={
                "data": [
                    {"x": [1, 2, 3], "y": [2, 4, 3], "type": "bar", "name": "SF"},
                    {
                        "x": [1, 2, 3],
                        "y": [5, 4, 3],
                        "type": "bar",
                        "name": u"Montréal",
                    },
                ]
            }
        )
    ]

    return children


def generate_tab_3(data_Historique, Team_List):

    style_data_cond = style_data_cond_historic(Team_List)

    children = []

    children += [
        html.Button("Confirmer Modification", id="Modification_Historique", n_clicks=0)
    ]

    children += [
        dash_table.DataTable(
            id="Historique_Partie",
            columns=[
                {"name": i, "id": i, "editable": Editable(i), "type": which_type(i)}
                for i in Column_Storage
            ],
            style_cell={"textAlign": "center"},
            style_table=style_table,
            style_data_conditional=style_data_cond,
            style_header=style_header,
            data=data_Historique,
            #    editable= True,
        )
    ]

    return children


def Editable(i):
    if i == "Valeur" or i == "Coef":
        return True
    return False


def which_type(i):
    if i == "Equipe":
        return "any"
    return "numeric"


def cricket_layout(local_path):

    game_att = load_local_dictionnary(local_path, "Cricket")

    init = init_db(game_att)

    layout = html.Div(
        [
            dcc.Tabs(
                id="tabs",
                value="tab-main",
                children=[
                    dcc.Tab(
                        label="Game",
                        value="tab-main",
                        style=tab_style,
                        selected_style=tab_selected_style,
                    ),
                    dcc.Tab(
                        label="Stats",
                        value="tab-stat",
                        style=tab_style,
                        selected_style=tab_selected_style,
                    ),
                    dcc.Tab(
                        label="Historique",
                        value="tab-historique",
                        style=tab_style,
                        selected_style=tab_selected_style,
                    ),
                ],
            ),
            html.Div(id="tab-content"),
        ]
    )
    return layout
