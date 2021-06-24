import dash_html_components as html

import os
import pandas as pd
import numpy as np

from .styles_dash import color_mapping


# Function that creates the color scale in the score table
def map_min_bound(f):
    if f == 0.0:
        return 0
    elif f == 0.75:
        return 1
    elif f == 1.5:
        return 2
    elif f == 2.25:
        return 3
    else:
        return None


def discrete_background_color_bins(df, n_bins, columns):

    #    import colorlover
    bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
    if columns == "all":

        # if columns != 'Score':

        if "id" in df:
            df_numeric_columns = df.select_dtypes("number").drop(["id"], axis=1)
        else:
            df_numeric_columns = df.select_dtypes("number")
    else:
        df_numeric_columns = df[columns]
    df_max = 3
    df_min = 0
    ranges = [((df_max - df_min) * i) + df_min for i in bounds]

    styles = []
    legend = []
    for i in range(1, len(bounds)):
        min_bound = ranges[i - 1]
        max_bound = ranges[i]
        # backgroundColor = colorlover.scales[str(n_bins)]['seq']['Blues'][i - 1]
        color = "white" if i > len(bounds) / 2.0 else "inherit"

        if i == 1:
            backgroundColor = "white"

        if i == 2:
            backgroundColor = "rgb(158,202,225)"

        if i == 3:
            backgroundColor = "rgb(49,130,189)"

        if i == 4:
            backgroundColor = "rgb(50, 50, 50)"

        for column in df_numeric_columns:
            styles.append(
                {
                    "if": {
                        "filter_query": (
                            "{{{column}}} >= {min_bound}"
                            + (
                                " && {{{column}}} < {max_bound}"
                                if (i < len(bounds) - 1)
                                else ""
                            )
                        ).format(
                            column=column,
                            min_bound=min_bound,
                            max_bound=max_bound
                        ),
                        "column_id": column,
                    },
                    "backgroundColor": backgroundColor,
                    "color": color,
                }
            )
        s_dic = {
            "backgroundColor": backgroundColor,
            "borderLeft": "1px rgb(50, 50, 50) solid",
            "textAlign": "center",
            "height": "25px",
        }

        if min_bound == 2.25:
            s_dic["color"] = "white"

        legend.append(
            html.Div(
                style={"display": "inline-block", "width": "60px"},
                children=[html.Div(map_min_bound(min_bound), style=s_dic)],
            )
        )

    return (
        styles,
        html.Div(legend, style={"padding": "5px 0px 0px 0px", "margin-left": "15px"}),
    )


def Storage_Player_Separation(turn):
    if turn > 1:
        style_data_conditional = [
            {
                "if": {
                    "filter_query": "{Fleche numero} = 1",
                },
                "backgroundColor": "RebeccaPurple",
                "color": "white",
            },
        ]
    else:
        style_data_conditional = [
            {"if": {"row_index": "odd"}, "backgroundColor": "rgb(248, 248, 248)"}
        ]
    return style_data_conditional


def Which_Line(Turn_Counter_Index, data_Fleches_Temp, Dart_Number):

    Player_Line = [
        {"if": {"row_index": "odd"}, "backgroundColor": "rgb(248, 248, 248)"},
        {
            "if": {"row_index": Turn_Counter_Index},
            "backgroundColor": color_mapping[
                data_Fleches_Temp[Turn_Counter_Index]["Equipe"] + "Light"
            ],
            "fontWeight": "bold",
        },
        {
            "if": {
                "column_id": list(data_Fleches_Temp[Turn_Counter_Index])[
                    2 * Dart_Number + 1
                ],
                "row_index": Turn_Counter_Index,
            },
            "backgroundColor": color_mapping[
                data_Fleches_Temp[Turn_Counter_Index]["Equipe"]
            ],
            "color": "white",
        },
        {
            "if": {
                "column_id": list(data_Fleches_Temp[Turn_Counter_Index])[
                    2 * Dart_Number + 2
                ],
                "row_index": Turn_Counter_Index,
            },
            "backgroundColor": color_mapping[
                data_Fleches_Temp[Turn_Counter_Index]["Equipe"]
            ],
            "color": "white",
        },
    ]

    return Player_Line


def Douze_Turn(Game, Turn):

    if Game == "Douze":
        Game = [
            "12",
            "13",
            "14",
            "Double",
            "15",
            "16",
            "17",
            "Triple",
            "18",
            "19",
            "20",
            "Bull",
            "Score",
        ]
    Number_Open_Close = [
        {
            "if": {"column_id": Game[Turn]},
            "backgroundColor": "rgb(85, 85, 85)",  # gris
            "color": "white",
        }
    ]

    return Number_Open_Close


def Open_Or_Closed(name, Team_Number_Game, Score_Table, Turn_Counter_Index):
    if name == "Cricket":
        Game = ["20", "19", "18", "17", "16", "15", "Bull"]  # , 'Score', 'Delta']
    Number_Open_Close = [
        None,
        None,
        None,
        None,
        None,
        None,
        None,
    ]  # doesn't do anything for the total Score

    for j in range(0, len(Number_Open_Close)):

        Compteur_Fermer = 0

        for i in range(0, Team_Number_Game):
            if Score_Table[i][Game[j]] == 3:
                Compteur_Fermer = Compteur_Fermer + 1

        if Compteur_Fermer == Team_Number_Game:  # Tout le monde a fermer
            Number_Open_Close[j] = {
                "if": {"column_id": Game[j]},
                "backgroundColor": "rgb(85, 85, 85)",  # gris
                "color": "white",
            }

        elif Compteur_Fermer == 0:  # Personne n'a fermé
            Number_Open_Close[j] = {
                "if": {"column_id": Game[j]},
                "backgroundColor": "rgb(230, 230, 230)",
                "fontWeight": "bold",
            }

        else:  # au moins une personne a fermé
            if (
                Score_Table[Turn_Counter_Index][Game[j]] == 3
            ):  # celui qui est en train de jouer a fermé, il peut donc marquer des points

                Number_Open_Close[j] = {
                    "if": {"column_id": Game[j]},
                    "backgroundColor": "rgb(12, 124, 27)",  # vert
                    "color": "white",
                }

            else:  # celui qui est en train de jouer n'a pas fermé, il peut donc se prendre des points.
                Number_Open_Close[j] = {
                    "if": {"column_id": Game[j]},
                    "backgroundColor": "rgb(232, 45, 82)",  # rouge
                    "color": "white",
                }

    return Number_Open_Close


def Cancel_Button(data_Fleches_Temp, Team_Turn):

    data_Fleches_Temp[Team_Turn]["Fleche 1"] = None
    data_Fleches_Temp[Team_Turn]["Fleche 2"] = None
    data_Fleches_Temp[Team_Turn]["Fleche 3"] = None
    data_Fleches_Temp[Team_Turn]["Coef 1"] = None
    data_Fleches_Temp[Team_Turn]["Coef 2"] = None
    data_Fleches_Temp[Team_Turn]["Coef 3"] = None

    return data_Fleches_Temp


def Submit_Turn(data_Fleches_Temp, Team_Turn, Next_Player, Dart_Number):

    if data_Fleches_Temp[Team_Turn]["Fleche 1"] is not None:

        coef1 = data_Fleches_Temp[Team_Turn]["Coef 1"]  # Save the shots
        Dart1 = data_Fleches_Temp[Team_Turn]["Fleche 1"]
    else:  # submitted with no entry
        coef1 = 1
        Dart1 = 0

    if data_Fleches_Temp[Team_Turn]["Fleche 2"] is not None:

        coef2 = data_Fleches_Temp[Team_Turn]["Coef 2"]
        Dart2 = data_Fleches_Temp[Team_Turn]["Fleche 2"]
    else:  # submitted with no entry
        coef2 = 1
        Dart2 = 0
        Dart_Number = 0

    if data_Fleches_Temp[Team_Turn]["Fleche 3"] is not None:

        coef3 = data_Fleches_Temp[Team_Turn]["Coef 3"]
        Dart3 = data_Fleches_Temp[Team_Turn]["Fleche 3"]
    else:  # submitted with no entry
        coef3 = 1
        Dart3 = 0
        Dart_Number = 0

    Darts = [Dart1, Dart2, Dart3]
    Coef = [coef1, coef2, coef3]

    data_Fleches_Temp[Next_Player][
        "Fleche 1"
    ] = None  # Erase the shots of the next player
    data_Fleches_Temp[Next_Player]["Fleche 2"] = None
    data_Fleches_Temp[Next_Player]["Fleche 3"] = None
    data_Fleches_Temp[Next_Player]["Coef 1"] = None
    data_Fleches_Temp[Next_Player]["Coef 2"] = None
    data_Fleches_Temp[Next_Player]["Coef 3"] = None

    return Darts, Coef, data_Fleches_Temp, Dart_Number


def Score_Update_Cricket(
    Darts,
    Coef,
    Turn,
    Score_Table,
    Team_Turn,
    Team_Number_Game,
    Dart_Number,
    #                Score_History,
    Cricket_Type,
):

    DartRound_Data = []

    Degats = [[0 for j in range(0, Team_Number_Game)] for i in range(0, len(Darts))]

    Fleche_qui_Ferme = [0, 0, 0]

    for j in range(0, len(Darts)):  # for each dart, fill in the score table

        if Darts[j] >= 15:
            value = Darts[j]
            coef = Coef[j]
            if value == 25:
                value_string = "Bull"
            else:
                value_string = str(int(value))

            if (
                Score_Table[Team_Turn][value_string] + coef <= 3
            ):  # Si celui qui joue ne ferme pas le chiffre qu'il a touché
                Score_Table[Team_Turn][value_string] = (
                    Score_Table[Team_Turn][value_string] + coef
                )
                Fleche_qui_Ferme[j] = coef

            elif (
                Score_Table[Team_Turn][value_string] == 3
            ):  # si celui qui joue avait deja fermé

                if Cricket_Type == "Cut_Throat":

                    for i in range(0, Team_Number_Game):

                        if i == Team_Turn:
                            continue

                        if (
                            Score_Table[i][value_string] < 3
                        ):  # mets des points à ceux qui n'ont pas fermé
                            Score_Table[i]["Score"] = (
                                Score_Table[i]["Score"] + value * coef
                            )
                            Degats[j][i] = value * coef

                else:
                    Checking_Other_Scores = 0
                    for i in range(0, Team_Number_Game):

                        if i == Team_Turn:
                            continue

                        if Score_Table[i][value_string] < 3:

                            Checking_Other_Scores = 1

                    if Checking_Other_Scores == 1:
                        Score_Table[Team_Turn]["Score"] = (
                            Score_Table[Team_Turn]["Score"] + value * coef
                        )
                        Degats[j][Team_Turn] = value * coef

            elif (
                Score_Table[Team_Turn][value_string] + coef >= 3
            ):  # Si celui qui joue ferme ce chiffre pendant ce tour

                if Cricket_Type == "Cut_Throat":

                    for i in range(0, Team_Number_Game):

                        if i == Team_Turn:
                            continue

                        if Score_Table[i][value_string] < 3:
                            Score_Table[i]["Score"] = Score_Table[i][
                                "Score"
                            ] + value * (
                                Score_Table[Team_Turn][value_string] + coef - 3
                            )
                            Degats[j][i] = value * (
                                Score_Table[Team_Turn][value_string] + coef - 3
                            )

                        Fleche_qui_Ferme[j] = (
                            3 - Score_Table[Team_Turn][value_string]
                        )  # je crois tous les fleches qui ferme ne doivent pas etre dans le if!

                else:
                    Checking_Other_Scores = 0
                    for i in range(0, Team_Number_Game):

                        if i == Team_Turn:
                            continue

                        if Score_Table[i][value_string] < 3:

                            Checking_Other_Scores = 1

                    if Checking_Other_Scores == 1:

                        Score_Table[Team_Turn]["Score"] = Score_Table[Team_Turn][
                            "Score"
                        ] + value * (Score_Table[Team_Turn][value_string] + coef - 3)
                        Degats[j][Team_Turn] = value * (
                            Score_Table[Team_Turn][value_string] + coef - 3
                        )

                        Fleche_qui_Ferme[j] = 3 - Score_Table[Team_Turn][value_string]

                Score_Table[Team_Turn][
                    value_string
                ] = 3  # (Needs to be after the for loop!)

        ### Calculate the distance in score to the leading score

        # Score_min = min(Score_Table[i]['Score'] for i in range(Team_Number_Game))
        for i in range(Team_Number_Game):
            Score_Table[i]["Delta"] = (
                Score_Table[i]["Score"] - Score_Table[Team_Turn]["Score"]
            )

        DartRound_Data.append(
            [
                Team_Turn,
                Turn + 1,
                j + 1,
                Darts[j],
                Coef[j],
                Degats[j],
                Fleche_qui_Ferme[j],
            ]
        )  # sauvegarde info fleche i

    return Score_Table, DartRound_Data


def Score_Update_Douze(
    Darts,
    Coef,
    Turn_Counter_Index,
    Score_Table,
    Team_Turn,
    Team_Number_Game,
    Dart_Number,
    Douze,
):

    DartRound_Data = []

    Degats = [[0 for i in range(0, Team_Number_Game)] for j in range(0, len(Darts))]

    Fleche_qui_Ferme = [0, 0, 0]

    Factor = 0.51  # stay at 0.5 if you don t hit

    if Turn_Counter_Index % 4 == 3:
        if Douze[Turn_Counter_Index] == "Double":
            for j in range(0, len(Darts)):  # for each dart, fill in the score table
                if Coef[j] == 2:
                    Factor = 1
                    Score_Table[Team_Turn][Douze[Turn_Counter_Index]] = (
                        Score_Table[Team_Turn][Douze[Turn_Counter_Index]] + Coef[j]
                    )
                    Degats[j][Team_Turn] = Degats[j][Team_Turn] + Darts[j] * Coef[j]
                    Fleche_qui_Ferme[j] = Score_Table[Team_Turn][
                        Douze[Turn_Counter_Index]
                    ]

        if Douze[Turn_Counter_Index] == "Triple":
            for j in range(0, len(Darts)):  # for each dart, fill in the score table
                if Coef[j] == 3:
                    Factor = 1
                    Score_Table[Team_Turn][Douze[Turn_Counter_Index]] = (
                        Score_Table[Team_Turn][Douze[Turn_Counter_Index]] + Coef[j]
                    )
                    Degats[j][Team_Turn] = Degats[j][Team_Turn] + Darts[j] * Coef[j]
                    Fleche_qui_Ferme[j] = Score_Table[Team_Turn][
                        Douze[Turn_Counter_Index]
                    ]

        if Douze[Turn_Counter_Index] == "Bull":
            for j in range(0, len(Darts)):  # for each dart, fill in the score table
                if Darts[j] == 25:
                    Factor = 1
                    Score_Table[Team_Turn][Douze[Turn_Counter_Index]] = (
                        Score_Table[Team_Turn][Douze[Turn_Counter_Index]] + Coef[j]
                    )
                    Degats[j][Team_Turn] = Degats[j][Team_Turn] + Darts[j] * Coef[j]
                    Fleche_qui_Ferme[j] = Score_Table[Team_Turn][
                        Douze[Turn_Counter_Index]
                    ]

    else:

        for j in range(0, len(Darts)):  # for each dart, fill in the score table

            if Darts[j] == int(Douze[Turn_Counter_Index]):
                Factor = 1
                Score_Table[Team_Turn][Douze[Turn_Counter_Index]] = (
                    Score_Table[Team_Turn][Douze[Turn_Counter_Index]] + Coef[j]
                )
                Degats[j][Team_Turn] = Degats[j][Team_Turn] + Darts[j] * Coef[j]
                Fleche_qui_Ferme[j] = Coef[j]

    Score_Table[Team_Turn]["Score"] = round(
        Factor * Score_Table[Team_Turn]["Score"]
        + Degats[0][Team_Turn]
        + Degats[1][Team_Turn]
        + Degats[2][Team_Turn]
    )

    for j in range(0, len(Darts)):  # save each dart

        DartRound_Data.append(
            [
                Team_Turn,
                Turn_Counter_Index + 1,
                j + 1,
                Darts[j],
                Coef[j],
                Degats[j],
                Fleche_qui_Ferme[j],
            ]
        )  # sauvegarde info fleche i

    return Score_Table, DartRound_Data


def Remove_Last_Round(data_Historique, Darts_Total):

    for i in range(0, Darts_Total):

        del data_Historique[-1]

    return data_Historique


def Get_Click_Data(
    clickData, df_darts, Dart_Number, data_Fleches_Temp, Player_Turn, Darts_Total
):
    click_Location = clickData["points"][0]["location"]
    touched_polygon = df_darts.loc[df_darts["id"] == click_Location].index[0]
    value = df_darts.loc[touched_polygon, "value"]
    coef = df_darts.loc[touched_polygon, "coef"]

    clickData = None  # To be able to click at the same place

    if Dart_Number == 0:  # Entering the score of the 1st dart

        data_Fleches_Temp[Player_Turn]["Fleche 1"] = value
        data_Fleches_Temp[Player_Turn]["Coef 1"] = coef

    if Dart_Number == 1:  # Entering the score of the 2nd dart

        data_Fleches_Temp[Player_Turn]["Fleche 2"] = value
        data_Fleches_Temp[Player_Turn]["Coef 2"] = coef

    if Dart_Number == 2:  # Entering the score of the 3rd dart

        data_Fleches_Temp[Player_Turn]["Fleche 3"] = value
        data_Fleches_Temp[Player_Turn]["Coef 3"] = coef
        Dart_Number = 1  # (so that the highlight changes once you validate)

    Dart_Number = (Dart_Number + 1) % Darts_Total

    return clickData, Dart_Number, data_Fleches_Temp


def Get_Stats(
    data_Historique,
    Stats_Table,
    Team_List,
    Stats_Graph,
    Dropdown_Value,
    Stats_Histo,
    Value_RadioItem="Stat_Equipe",
):

    if (
        len(data_Historique) != 0
    ):  # still probelm if one of the teams hasnt played yet....
        N_Tours = data_Historique[-1]["Tour"]

        if Value_RadioItem == "Stat_Equipe":
            N_Joueur = len(list(Team_List.keys()))
            print('Stat equipe')
        else:
            Player_List = [el for sublist in list(Team_List.values()) for el in sublist]
            N_Joueur = len(Player_List)

        X = [[j + 1 for j in range(0, N_Tours)]] * N_Joueur
#        Y = np.array([[0.] * N_Tours] * N_Joueur)
        Y = np.empty((N_Joueur,N_Tours), dtype=float)
        Y[:] = np.NaN

#        N_Touche = np.array([[0] * N_Tours] * N_Joueur)
        N_Touche = np.zeros((N_Joueur,N_Tours), dtype=float)

#        N_Degats = np.array([[0.] * N_Tours] * N_Joueur)
        N_Degats = np.zeros((N_Joueur,N_Tours), dtype=float)

        Hover_Data = [ [0  for j in range (0, N_Tours )] for i in range (0,N_Joueur)]
        Game = list(Stats_Histo[0].keys())

        for i in range(0, len(data_Historique) // 3 ):  # Analysing the 3 darts of the turn in one go
            
            f1 = data_Historique[3 * i + 0]
            f2 = data_Historique[3 * i + 1]
            f3 = data_Historique[3 * i + 2]
                        
            if Value_RadioItem == "Stat_Equipe":

                Player_Turn = list(Team_List.keys()).index(f1["Equipe"])
                Tour_Reel = f1["Tour"]

            else:

                Player_Turn = Player_List.index(f1["Joueur"])
                #Tour_Reel = f1["Tour"] / len(Team_List[f1["Equipe"]])
                Tour_Reel = int( (f1["Tour"] -1 ) / len(Team_List[f1["Equipe"]]) ) +1
                print('Tour reel:',Tour_Reel)

            hover_text = f"Fleche 1: {f1['Valeur']:02} Coef: {f1['Coef']} <br>Fleche 2: {f2['Valeur']:02} Coef: {f2['Coef']}<br>Fleche 3: {f3['Valeur']:02} Coef: {f3['Coef']}"
            Hover_Data[Player_Turn][data_Historique[3 * i]["Tour"] - 1] = hover_text

            if (
                f1["Ferme le chiffre"] + f2["Ferme le chiffre"] + f3["Ferme le chiffre"]
                == 0
            ) and (
                np.sum(f1["Degats"]) + np.sum(f2["Degats"]) + np.sum(f3["Degats"]) == 0
            ):  # si tour à vide

                Stats_Table[Player_Turn]["# de tour à vide"] += 1

            else:

                N_Touche_Ferme = 0
                N_Touche_Degats = 0
                for f in [f1, f2, f3]:

                    if (f["Coef"] == 3) and \
                       (f["Degats"] != 0 or f["Ferme le chiffre"] != 0) :
                        # la flechette est un triple et il a compté (meme partiellement)
                        Stats_Table[Player_Turn]["# de triple"] += 1

                    if (
                        (f["Coef"] == 2)
                        and (f["Degats"] != 0 or f["Ferme le chiffre"] != 0)
                        and f["Valeur"] != 25
                    ):
                        # la flechette est un double (mais pas un bull) et il a compté (meme partiellement)
                        Stats_Table[Player_Turn]["# de double"] += 1

                    if f["Valeur"] != 0:
                        
                        #N_Touche_Precedent = N_Touche[Player_Turn][f["Tour"] - 1]
                        N_Touche_Ferme += f["Ferme le chiffre"]
                        N_Touche_Degats += np.max(f["Degats"]) / f["Valeur"]
#                        N_Touche[Player_Turn][f["Tour"] - 1] += (N_Touche_Ferme + N_Touche_Degats)
                        N_Degats[Player_Turn, f["Tour"] - 1] += np.sum(f["Degats"])

                        if str(f["Valeur"]) in Game:
                            Stats_Histo[Player_Turn][str(f["Valeur"])] += 1

                
                N_Touche[Player_Turn, f1["Tour"] - 1] = N_Touche_Ferme + N_Touche_Degats
                

                

            N_Touche_Tot = np.sum(
                N_Touche[Player_Turn]
            )  # = au nombre de touche total pour cette equipe
            N_Degats_Tot = np.sum(
                N_Degats[Player_Turn]
            )  # = au nombre de degats total pour cette equipe

            #        Stats_Table[Player_Turn]['# Touche/ Tour'] = ( Stats_Table[Player_Turn]['# Touche/ Tour'] * ( data_Historique[ 3*i ]['Tour'] -1) + N_Touche ) / (data_Historique[ 3*i ]['Tour'])
            Stats_Table[Player_Turn]["# Touche/ Tour"] = N_Touche_Tot / Tour_Reel
            Stats_Table[Player_Turn]["# Degats/ Tour"] = N_Degats_Tot / Tour_Reel

      

            Y[Player_Turn,f1["Tour"] - 1] = Stats_Table[Player_Turn][Dropdown_Value]
            

        Stats_Graph["layout"]["yaxis"]["title"]["text"] = Dropdown_Value
        print('Histo',Stats_Histo)
        

        for i in range(0, N_Joueur):

            Stats_Graph["data"][i]["x"] = X[i]
            Stats_Graph["data"][i]["y"] = Y[i]

            N_Touche_array = np.array(N_Touche[i])
            #        N_Touche_array_Rescaled = (N_Touche_array+1) *10 #/ max(N_Touche_array)
            N_Touche_array_Rescaled = (N_Touche_array / max(N_Touche_array) + 1) * 20
            # need to sort out this colour mapping shit
            #            Stats_Graph.data[i].update(marker={'color': color_mapping[list(Team_List.keys())[i]], 'symbol':'circle', 'size':N_Touche_array_Rescaled})
            Stats_Graph.data[i].update(
                marker={"symbol": "circle", "size": N_Touche_array_Rescaled}
            )
            Stats_Graph.data[i].update(hovertemplate=Hover_Data[i])

    return Stats_Table, Stats_Graph, Stats_Histo


def Update_Live_Player(data_Fleches_Temp, Turn, Team_Number_Game, Team_List):

    Number_Of_Players = len(Team_List[list(Team_List.keys())[Turn % Team_Number_Game]])
    Team_Turn = list(Team_List.keys())[Turn % Team_Number_Game]
    Player_Turn = Team_List[Team_Turn][int(Turn / Team_Number_Game) % Number_Of_Players]

    data_Fleches_Temp[Turn % Team_Number_Game]["index"] = Player_Turn

    return data_Fleches_Temp


def Number_Open_Close_f(
    name, Team_Number_Game, Score_Table, Turn_Counter_Index, Turn_Counter
):
    if name == "Cricket":
        Number_Open_Close = Open_Or_Closed(
            name, Team_Number_Game, Score_Table, Turn_Counter_Index
        )
    elif name == "Douze":
        Number_Open_Close = Douze_Turn(name, int(Turn_Counter / Team_Number_Game))
    return Number_Open_Close


def Render_Score_Table(data_Historique, Team_List, Cricket_Type, Score_Table):

    N_Teams = len(list(Team_List.keys()))

    for j in range(0, len(data_Historique)):
        Fleche = data_Historique[j]["Valeur"]
        Team_Turn = list(Team_List.keys()).index(data_Historique[j]["Equipe"])
        data_Historique[j]["Ferme le chiffre"] = 0
        data_Historique[j]["Degats"] = [0 for i in range(len(data_Historique[j]["Degats"]))]

        if Fleche >= 15:
            value = Fleche
            coef = data_Historique[j]["Coef"]
            if value == 25:
                value_string = "Bull"
            else:
                value_string = str(int(value))

            if (
                Score_Table[Team_Turn][value_string] + coef <= 3
            ):  # Si celui qui joue ne ferme pas le chiffre qu'il a touché
                Score_Table[Team_Turn][value_string] = (
                    Score_Table[Team_Turn][value_string] + coef
                )
                data_Historique[j]["Ferme le chiffre"] = coef
            elif (
                Score_Table[Team_Turn][value_string] == 3
            ):  # si celui qui joue avait deja fermé

                if Cricket_Type == "Cut_Throat":

                    for i in range(0, N_Teams):

                        if i == Team_Turn:
                            continue

                        if (
                            Score_Table[i][value_string] < 3
                        ):  # mets des points à ceux qui n'ont pas fermé
                            Score_Table[i]["Score"] = (
                                Score_Table[i]["Score"] + value * coef
                            )
                            print("###############", i)
                            print("###############", data_Historique[j]["Degats"])
                            data_Historique[j]["Degats"][i] = value * coef

                else:
                    Checking_Other_Scores = 0
                    for i in range(0, N_Teams):

                        if i == Team_Turn:
                            continue

                        if Score_Table[i][value_string] < 3:

                            Checking_Other_Scores = 1

                    if Checking_Other_Scores == 1:
                        Score_Table[Team_Turn]["Score"] = (
                            Score_Table[Team_Turn]["Score"] + value * coef
                        )
                        data_Historique[j]["Degats"][Team_Turn] = value * coef

            elif (
                Score_Table[Team_Turn][value_string] + coef >= 3
            ):  # Si celui qui joue ferme ce chiffre pendant ce tour

                if Cricket_Type == "Cut_Throat":

                    for i in range(0, N_Teams):

                        if i == Team_Turn:
                            continue

                        if Score_Table[i][value_string] < 3:
                            Score_Table[i]["Score"] = Score_Table[i][
                                "Score"
                            ] + value * (
                                Score_Table[Team_Turn][value_string] + coef - 3
                            )
                            data_Historique[j]["Degats"][i] = value * (
                                Score_Table[Team_Turn][value_string] + coef - 3
                            )

                        data_Historique[j]["Ferme le chiffre"] = (
                            3 - Score_Table[Team_Turn][value_string]
                        )  # je crois tous les fleches qui ferme ne doivent pas etre dans le if!

                else:
                    Checking_Other_Scores = 0
                    for i in range(0, N_Teams):

                        if i == Team_Turn:
                            continue

                        if Score_Table[i][value_string] < 3:

                            Checking_Other_Scores = 1

                    if Checking_Other_Scores == 1:

                        Score_Table[Team_Turn]["Score"] = Score_Table[Team_Turn][
                            "Score"
                        ] + value * (Score_Table[Team_Turn][value_string] + coef - 3)
                        data_Historique[j]["Degats"][Team_Turn] = value * (
                            Score_Table[Team_Turn][value_string] + coef - 3
                        )

                        data_Historique[j]["Ferme le chiffre"] = (
                            3 - Score_Table[Team_Turn][value_string]
                        )

                Score_Table[Team_Turn][
                    value_string
                ] = 3  # (Needs to be after the for loop!)

        ### Calculate the distance in score to the leading score

        for i in range(N_Teams):
            Score_Table[i]["Delta"] = (
                Score_Table[i]["Score"] - Score_Table[Team_Turn]["Score"]
            )

    return Score_Table, data_Historique


def Temp_To_Historique(
    data_Fleches_Temp,
    data_Historique,
    Column_Storage,
    Darts_Total,
    Team_List,
    Step,
    local_path,
    Team_Turn_index,
    Next_Player,
    Dart_Number,
):

    N_Teams = len(list(Team_List.keys()))

    N_Players = len(Team_List[list(Team_List.keys())[Step % N_Teams]])
    Team_Turn = list(Team_List.keys())[Step % N_Teams]

    Player = Team_List[Team_Turn][int(Step / N_Teams) % N_Players]

    Darts, Coef, data_Fleches_Temp, Dart_Number = Submit_Turn(
        data_Fleches_Temp, Team_Turn_index, Next_Player, Dart_Number
    )

    DartRound_Data = []
    Degats = [0 for j in range(0, N_Teams)]
    Fleche_qui_Ferme = [0, 0, 0]

    for i in range(Darts_Total):

        DartRound_Data.append(
            [
                Team_Turn_index,
                Player,
                int(Step / N_Teams) + 1,
                i + 1,
                Darts[i],
                Coef[i],
                Degats,
                Fleche_qui_Ferme[i],
            ]
        )  # sauvegarde info fleche i
        data_Historique.append(
            {
                Column_Storage[j]: DartRound_Data[i][j]
                for j in range(len(Column_Storage))
            }
        )
        #########    data_Historique[-1][Column_Storage[5]] = np.sum(DartRound_Data[i][5])
        data_Historique[-1][Column_Storage[0]] = list(Team_List.keys())[
            DartRound_Data[i][0]
        ]

    Step = Step + 1  # change index for next player

    data_Fleches_Temp = Update_Live_Player(data_Fleches_Temp, Step, N_Teams, Team_List)

    Save(local_path, "data_Historique.npy", data_Historique)

    return data_Fleches_Temp, data_Historique, Step


def End_Game(
    Score_Table,
    Team_Number_Game,
    Team_Turn,
    Score_History,
    Team_List,
    Darts_Total,
    Cricket,
):

    small_victory = all([Score_Table[Team_Turn][el] == 3 for el in Cricket[:-1]])
    if small_victory:  # end game criteria
        print("small victory")
        Score_min = min(Score_Table[i]["Score"] for i in range(Team_Number_Game))

        print("Score_Table:", Score_Table)
        print("Team_Number_Game:", Team_Number_Game)
        print("Team_Turn:", Team_Turn)
        print("Score_History:", Score_History)
        print("Team_List:", Team_List)
        if Score_Table[Team_Turn]["Score"] == Score_min:
            Deroulement_de_Partie = pd.DataFrame(Score_History)
            Deroulement_de_Partie.to_csv(
                "Partie.csv"
            )  # sauvegarde le derouler de partie

            Player_Game_Info = [[] for i in range(len(list(Team_List.keys())))]

            for i in range(len(Score_History)):

                Player_Game_Info[
                    int(i / Darts_Total) % len(list(Team_List.keys()))
                ].append(Score_History[i])

            for i in range(len(Team_List)):
                Historic_Joueur = pd.read_csv(
                    "ressources/Player_Info/{}.csv".format(list(Team_List.keys())[i])
                )
                Partie_Joueur = Player_Game_Info[i]

                Partie_Joueur = pd.DataFrame(Partie_Joueur, columns=Column_Storage)

                Partie_Joueur.to_csv(
                    "{}.csv".format(list(Team_List.keys())[i]), index=False
                )


def Save(local_path, name, file):

    np.save(os.path.join(local_path, name), file)
