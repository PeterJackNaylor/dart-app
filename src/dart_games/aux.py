import os
import numpy as np
import pandas as pd

import plotly.express as px
from .app_dashboard_functions import discrete_background_color_bins
from ..utils.pickle import open_dic

from .styles_dash import color_mapping


Column_Storage = [
    "Equipe",
    "Joueur",
    "Tour",
    "Fleche numero",
    "Valeur",
    "Coef",
    "Degats",
    "Ferme le chiffre",
]

Column_Live_Stats = [
    "index",
    "# Touche/ Tour",
    "# de triple",
    "# de double",
    "# de tour à vide",
    "# Degats/ Tour",
    "Tour",
]


Column_Live_Stats_Graph = [
    "# Touche/ Tour",
    "# de triple",
    "# de double",
    "# de tour à vide",
    "# Degats/ Tour",
    "Tour",
    "Equipe",
]


def init_db(att, Value_RadioItem="Stat_Equipe"):
    Team_List = att["Team_List"]
    n_t = att["n_t"]
    Game = att["Game"]

    # Douze = ['12', '13', '14', 'Double', '15', '16', '17', 'Triple',
    #          '18', '19', '20', 'Bull', 'Score']

    # Game = Douze
    # Score_Init = [0 for _ in Game]

    Turn_Counter = 0
    Flechette_Compteur = 0

    df_Score = init_df_score(n_t, Game, Team_List)
    Score_Table = df_Score.to_dict("records")

    data_Fleches_Temp = init_df_live(att)

    if Value_RadioItem == "Stat_Equipe":
        stat_init = np.zeros((n_t, len(Column_Live_Stats)), dtype=int)
        df_Stat_Live = pd.DataFrame(stat_init, columns=Column_Live_Stats)
        df_Stat_Live["index"] = list(Team_List.keys())
    else:
        Player_List = [
            element for sublist in list(Team_List.values()) for element in sublist
        ]
        stat_init = np.zeros((len(Player_List), len(Column_Live_Stats)), dtype=int)
        df_Stat_Live = pd.DataFrame(stat_init, columns=Column_Live_Stats)
        df_Stat_Live["index"] = Player_List

    Stats_Table = df_Stat_Live.to_dict("records")

    data_Historique = pd.DataFrame(columns=Column_Storage).to_dict("records")

    if Value_RadioItem == "Stat_Equipe":

        df_Graph_Live = init_stat_live(n_t, list(Team_List.keys()))
        Stats_Graph = px.scatter(
            df_Graph_Live,
            x="Tour",
            y="# Touche/ Tour",
            color=list(Team_List.keys()),
            hover_data=[],
        )  # ,size='petal_length', hover_data=['Dernier_Tour'])
        #   Y_Live_Stats = [[0] * len(Column_Live_Stats_Graph)]
        for i in range(n_t):
            Stats_Graph.data[i].update(mode="markers+lines")
            Stats_Graph.data[i].update(
                marker={
                    "color": color_mapping[list(Team_List.keys())[i]],
                    "symbol": "circle",
                }
            )

        Stats_Graph.layout.update(
            legend={"title": {"text": "Equipe"}, "tracegroupgap": 0}
        )

    else:

        Player_List = [
            element for sublist in list(Team_List.values()) for element in sublist
        ]
        n_players = len(Player_List)
        df_Graph_Live = init_stat_live(n_players, Player_List)

        Stats_Graph = px.scatter(
            df_Graph_Live,
            x="Tour",
            y="# Touche/ Tour",
            color=Player_List,  # need to sort something out here and for colormappin below...
            hover_data=[],
        )  # ,size='petal_length', hover_data=['Dernier_Tour'])
        #   Y_Live_Stats = [[0] * len(Column_Live_Stats_Graph)]
        for i in range(n_players):
            Stats_Graph.data[i].update(mode="markers+lines")
        #            Stats_Graph.data[i].update(marker={'color': color_mapping[list(Team_List.keys())[i]], 'symbol':'circle'})

        Stats_Graph.layout.update(
            legend={"title": {"text": "Joueur"}, "tracegroupgap": 0}
        )

    (styles, legend) = discrete_background_color_bins(df_Score, 4, Game[:-2])
    return (
        Turn_Counter,
        Flechette_Compteur,
        data_Fleches_Temp,
        Stats_Table,
        Stats_Graph,
        Score_Table,
        data_Historique,
        legend,
    )


def init_stat_live(n, teams):

    init_graph_live = np.zeros((n, len(Column_Live_Stats_Graph)), dtype=int)

    df_Graph_Live = pd.DataFrame(init_graph_live, columns=Column_Live_Stats_Graph)
    df_Graph_Live["index"] = teams

    return df_Graph_Live


def init_df_score(n, game, teams):
    return pd.DataFrame(
        np.zeros((n, len(game)), dtype=int), columns=game, index=list(teams.keys())
    )


def init_df_live(att):
    n = att["n_t"]
    game = att["Game"]
    teams = att["Team_List"]

    column = ["Equipe"] + [
        n.format(i) for i in range(1, 4) for n in ["Fleche {}", "Coef {}"]
    ]
    index = [teams[list(teams.keys())[i]][0] for i in range(n)]
    score = [[t] + [None] * 6 for t in teams]
    df_score = pd.DataFrame(np.array(score), columns=column)
    df_score["index"] = index
    data_Fleches_Temp = df_score.to_dict("records")

    return data_Fleches_Temp


def load_local_dictionnary(local_path, name):
    Darts_Total = 3
    if name == "Cricket":
        Game = ["20", "19", "18", "17", "16", "15", "Bull", "Score", "Delta"]
    elif name == "Douze":
        Game = ["12"]
    if os.path.isdir(local_path):
        print("loading local files")
        dic = open_dic(os.path.join(local_path, "meta.pickle"))

    else:
        print("taking default dic")
        dic = {
            "teams": ["Blue", "Red"],
            "picked_players": ["Peter", "Bruno"],
            "picked_game": "Just a template",
        }

    Team_List = {}
    for i, t in enumerate(dic["teams"]):
        player = dic["picked_players"][i]
        if t in Team_List.keys():
            Team_List[t].append(player)
        else:
            Team_List[t] = [player]

    n_t = len(Team_List)

    game_att = {
        "Game": Game,
        "n_t": n_t,
        "Team_List": Team_List,
        "Darts_Total": Darts_Total,
        "Cricket_Type": "Cut_Throat",
    }
    return game_att


def check_if_init(data_Fleches_Temp, game_att):
    if len(data_Fleches_Temp) != game_att["n_t"]:
        return True
    else:
        team_current = [d["Equipe"] for d in data_Fleches_Temp]
        team_file = [k for k in game_att["Team_List"].keys()]
        if team_current != team_file:
            return True
        else:
            return False

def load_var(local_path):
    name = "data_Historique"
    if not os.path.isdir(local_path):
        os.mkdir(local_path)
    if os.path.isfile(os.path.join(local_path, name + ".npy")):
        f = np.load(os.path.join(local_path, name + ".npy"), allow_pickle=True)
        output = f.tolist()
    else:
        output = []
    return output
