
import os
import numpy as np
import pandas as pd 

import plotly.express as px
from .app_dashboard_functions import discrete_background_color_bins
from ..utils.pickle import open_dic

def init_db(Team_List, n_t, Game):
    Score_Storage = []
    # Douze = ['12', '13', '14', 'Double', '15', '16', '17', 'Triple',
    #          '18', '19', '20', 'Bull', 'Score']

    # Game = Douze
    # Score_Init = [0 for _ in Game]
    

    Score_Live = [[t] + [None]*6 for t in Team_List]

    Turn_Counter = 0
    Flechette_Compteur = 0

    df_Score = init_df_score(n_t, Game, Team_List)

    darts_3_column = ['Equipe'] + \
                     [n.format(i) for i in range(1, 4) for n in ['Fleche {}', 'Coef {}']]
    index_3 = [Team_List[list(Team_List.keys())[i]][0] for i in range(n_t)]

    df_Score_Live_New_Way = pd.DataFrame(np.array(Score_Live),
                                         columns=darts_3_column)
    df_Score_Live_New_Way["index"] = index_3

    Column_Live_Stats = ['# Touche/ Tour',
                         '# de triple',
                         '# de double',
                         '# de tour à vide',
                         'Longest streak',
                         'Tour']

    stat_init = np.zeros((n_t, len(Column_Live_Stats)), dtype=int)
    df_Stat_Live = pd.DataFrame(stat_init,
                                columns=Column_Live_Stats)
    df_Stat_Live["index"] = list(Team_List.keys())

    Column_Storage = ['Player',
                      'Tour',
                      'Flèche numéro',
                      'Valeur',
                      'Coef',
                      'Dégats',
                      'Ferme le chiffre']
    df_Score_Storage = pd.DataFrame(columns=Column_Storage)
    Column_Live_Stats_Graph, df_Graph_Live = init_stat_live(n_t, Team_List) 
    fig_Stat = px.scatter(df_Graph_Live,
                          x="Tour",
                          y="# Touche/ Tour",
                          color=list(Team_List.keys()),
                          hover_data=[]) #,size='petal_length', hover_data=['Dernier_Tour'])
    Y_Live_Stats = [[0] * len(Column_Live_Stats_Graph)]

    for i in range(n_t):
        fig_Stat.data[i].update(mode='markers+lines')



    (styles, legend) = discrete_background_color_bins(df_Score, 4, Game[:-1])
    return Turn_Counter, Flechette_Compteur, Score_Storage, Y_Live_Stats, df_Score_Live_New_Way, df_Score, df_Stat_Live, Column_Live_Stats_Graph, fig_Stat, df_Score_Storage, legend, Column_Storage

def init_stat_live(n, teams):
    Column_Live_Stats_Graph = ['# Touche/ Tour',
                               '# de triple',
                               '# de double',
                               '# de tour à vide',
                               'Longest streak',
                               'Tour',
                               'Player']

    init_graph_live = np.zeros((n, len(Column_Live_Stats_Graph)), dtype=int)

    df_Graph_Live = pd.DataFrame(init_graph_live,
                                 columns=Column_Live_Stats_Graph)
    df_Graph_Live["index"] = list(teams.keys())
    return Column_Live_Stats_Graph, df_Graph_Live

def init_df_score(n, game, teams):
    return pd.DataFrame(np.zeros((n, len(game)), dtype=int),
                        columns=game, index=list(teams.keys()))


def load_local_dictionnary(local_path):
    if os.path.isdir(local_path):
        print("loading local files")
        dic = open_dic(os.path.join(local_path, "meta.pickle"))
    else:
        print("taking default dic")
        dic = {"teams": ["Blue", "Red"],
               "picked_players": ["Peter", "Bruno"],
               "picked_game": "Just a template"}
        
    Team_List = {}
    for i, t in enumerate(dic["teams"]):
        player = dic["picked_players"][i]
        if t in Team_List.keys():
            Team_List[t].append(player)
        else:
            Team_List[t] = [player]

    n_t = len(Team_List)
    return Team_List, n_t



def load_var(local_path, list_variables, att):
    outputs = []
    simple_integer = ["Turn_Counter"]

# ["Turn_Counter", 'Partie_Historique', 'Stats_Partie',
#                             'Partie_Live', 'Score', 'Graph_Partie']
    if not os.path.isdir(local_path):
        os.mkdir(local_path)
    for name in list_variables:
        if name in simple_integer:
            if os.path.isfile(os.path.join(local_path, name + ".txt")):
                f = open(os.path.join(local_path, name + ".txt"), "r")
                item = int(f.read())
            else:
                item = 0
        else:
            if os.path.isfile(os.path.join(local_path, name + ".npy")):
                f = np.load(os.path.join(local_path, name + ".npy"), allow_pickle=True)
                item = f.tolist()
            else:
                if name == 'Stats_Partie':
                    _, item = init_stat_live(att['n_t'], att['Team_List'])
                    item = item.to_dict("records")
                elif name == "data_Table":
                    item = init_df_score(att['n_t'], att["Game"], att['Team_List']).to_dict("records")
                else:
                    item = []
        outputs.append(item)
    return outputs

    # else:
    #     print('the file needs to be created')
    #     Turn = 0
    #     Dart_Number = 0
    #     Score_History= []
    #     f1 = open(os.path.join(local_path, "Turn_Counter.txt"), "x")
    #     f1.write(str(Turn))
    #     f1.close()

    #     np.save(os.path.join(local_path, 'Partie_Live.npy'),Score_History)
    #     np.save(os.path.join(local_path, 'Partie_Historique.npy'),data_Historique)
    #     np.save(os.path.join(local_path, 'Score.npy'),data_Table)
    #     np.save(os.path.join(local_path, 'Graph_Partie.npy'),y_live)
    #     np.save(os.path.join(local_path, 'Stats_Partie.npy'),stat_live)

    return Turn, Score_History, data_Table, data_Historique, y_live, stat_live

def Save_Everyone(local_path,Turn,Score_History,data_Historique,data_Table,Y_Live,Stat_Live):

    f1 = open(os.path.join(local_path, "Turn_Counter.txt"), "w")
    f1.write(str(Turn))
    f1.close()

    np.save(os.path.join(local_path, 'Partie_Live.npy'),Score_History)
    np.save(os.path.join(local_path, 'Partie_Historique.npy'),data_Historique)
    np.save(os.path.join(local_path, 'Score.npy'),data_Table)
    np.save(os.path.join(local_path, 'Graph_Partie.npy'),Y_Live)
    np.save(os.path.join(local_path, 'Stats_Partie.npy'),Stat_Live)


