import os
import copy


from dash.dependencies import Input, Output, State

import pandas as pd

# from ..utils.plot_geojson import dart_plot

from .app_dashboard_functions import (
    discrete_background_color_bins,
    Which_Line,
    # Open_Or_Closed,
    Cancel_Button,
    # Submit_Turn,
    Remove_Last_Round,
    Get_Click_Data,
    # Score_Update_Cricket,
    # Score_Update_Douze,
    # Douze_Turn,
    # Storage_Player_Separation,
    # Update_Live_Stats,
    # Update_Live_Graph,
    Update_Live_Player,
    Number_Open_Close_f,
    Render_Score_Table,
    Temp_To_Historique,
    Get_Stats,
    Save,
)

from .html_components import (
    cricket_layout,
    generate_tab_1,
    generate_tab_2,
    generate_tab_3,
)


from .aux import (
    init_db,
    load_local_dictionnary,
    load_var,
    init_df_live,
    check_if_init,
    Column_Storage,
)

GAME_NAME = "Cricket"


def create_ap(app, room_number):
    df_darts = pd.read_csv("ressources/mapping_dart_geojson.csv")
    local_path = f"ressources/local_games/{GAME_NAME}/{room_number}"
    layout = cricket_layout(local_path)

    @app.callback(Output("tab-content", "children"), Input("tabs", "value"))
    def render_content(tab):

        game_att = load_local_dictionnary(local_path, "Cricket")

        init = init_db(game_att)
        Turn_Counter, Flechette_Compteur = init[0:2]
        data_Fleches_Temp, Stats_Table, Stats_Graph = init[2:5]
        Score_Table, data_Historique = init[5:7]
        legend = init[7]

        if os.path.isfile(os.path.join(local_path, "data_Historique.npy")):

            data_Historique = load_var(local_path)

            Score_Table, data_Historique = Render_Score_Table(
                data_Historique,
                game_att["Team_List"],
                game_att["Cricket_Type"],
                Score_Table,
            )
            Save(local_path, "data_Historique.npy", data_Historique)

        if tab == "tab-main":

            return generate_tab_1(
                Turn_Counter, Flechette_Compteur, data_Fleches_Temp,
                Score_Table, legend
            )

        elif tab == "tab-stat":

            Dropdown_Value = "# Touche/ Tour"
            Stats_Table, Stats_Graph = Get_Stats(
                data_Historique,
                Stats_Table,
                game_att["Team_List"],
                Stats_Graph,
                Dropdown_Value,
            )
            return generate_tab_2(Stats_Table, Stats_Graph)

        elif tab == "tab-historique":

            return generate_tab_3(data_Historique, game_att["Team_List"])

    @app.callback(
        Output("Modification_Historique", "n_clicks"),
        # Output("Historique_Partie", "data"),
        Input("Modification_Historique", "n_clicks"),
        State("Historique_Partie", "data"),
    )
    def Modification_Historique(n_click_Historique, data_Historique):

        clicked_on_Modification_Historique = n_click_Historique == 1

        if clicked_on_Modification_Historique:
            print("I m in modification Historique")
            n_click_Historique = 0

            Save(local_path, "data_Historique.npy", data_Historique)

        return n_click_Historique, data_Historique

    @app.callback(
        Output("Graph_Live_Stat", "figure"),
        Output("Stat_Dropdown", "value"),
        Output("Stat_RadioItems", "value"),
        Output("Stat_Table", "data"),
        Input("Stat_Dropdown", "value"),
        Input("Stat_RadioItems", "value"),
    )
    def Update_DropdownValue(Dropdown_Value, Value_RadioItem):

        game_att = load_local_dictionnary(local_path, "Cricket")
        init = init_db(game_att, Value_RadioItem)
        Stats_Table, Stats_Graph = init[3:5]
        data_Historique = load_var(local_path)
        Stats_Table, Stats_Graph = Get_Stats(
            data_Historique,
            Stats_Table,
            game_att["Team_List"],
            Stats_Graph,
            Dropdown_Value,
            Value_RadioItem,
        )

        return Stats_Graph, Dropdown_Value, Value_RadioItem, Stats_Table

    # Callback called upon whenever you change player
    # or you change the dartnumber.
    # Puts up to date the display of the score tables
    @app.callback(
        Output("Score_Table", "style_header_conditional"),
        Output("Score_Table", "style_data_conditional"),
        Output("Score_Live_New_Way", "style_data_conditional"),
        Input("Dart_Counter", "data"),
        State("Score_Table", "data"),
        State("Score_Live_New_Way", "data"),
    )
    def Update_PlayerTurn_Display(Dart_Number, Score_Table, data_Fleches_Temp):

        game_att = load_local_dictionnary(local_path, "Cricket")
        data_Historique = load_var(local_path)
        N_Team = game_att["n_t"]

        if len(data_Historique) != 0:
            Steps = int(len(data_Historique) / game_att["Darts_Total"])
        else:
            Steps = 0

        Team_Turn_index = Steps % N_Team

        Player_Line_Dart_Column = Which_Line(
            Team_Turn_index, data_Fleches_Temp, Dart_Number
        )

        # Player_Separation = Storage_Player_Separation(Turn_Counter)

        (styles, _) = discrete_background_color_bins(
            pd.DataFrame(Score_Table), 4, game_att["Game"][:-2]
        )
        # Shouldn't it be data_Table instead of df_Score?

        Number_Open_Close = Number_Open_Close_f(
            "Cricket", game_att["n_t"], Score_Table, Team_Turn_index, Steps
        )

        return Number_Open_Close, styles, Player_Line_Dart_Column

    # Callback called upon whenever you click on the dart
    # board, on a button (cancel, submit, previous),
    # or when the list of players is changed. It then updates
    # the score accordingly.

    @app.callback(
        Output("Joueur", "children"),
        Output("Refresh", "n_clicks"),
        Output("cancel_round", "n_clicks"),
        Output("submit_round", "n_clicks"),
        Output("precedent_round", "n_clicks"),
        Output("basic-interactions", "clickData"),
        Output("Dart_Counter", "data"),
        Output("Score_Live_New_Way", "data"),
        Output("Score_Table", "data"),
        Input("Refresh", "n_clicks"),
        Input("cancel_round", "n_clicks"),
        Input("submit_round", "n_clicks"),
        Input("precedent_round", "n_clicks"),
        Input("basic-interactions", "clickData"),
        State("Dart_Counter", "data"),
        State("Score_Live_New_Way", "data"),
    )
    def Tab_Game_Callback(
        n_clicks_Refresh,
        n_clicks_Cancel,
        n_clicks_Submit,
        n_clicks_precedent,
        clickData,
        Dart_Number,
        data_Fleches_Temp,
    ):

        game_att = load_local_dictionnary(local_path, "Cricket")
        data_Historique = load_var(local_path)

        if len(data_Historique) != 0:
            Steps = int(len(data_Historique) / game_att["Darts_Total"])
        else:
            Steps = 0

        init = init_db(game_att)

        Score_Table = copy.deepcopy(init[5])
        Score_Table, data_Historique = Render_Score_Table(
            data_Historique,
            game_att["Team_List"],
            game_att["Cricket_Type"],
            Score_Table,
        )

        N_Team = game_att["n_t"]

        Team_Turn_index = Steps % N_Team
        Next_Team_index = (Steps + 1) % N_Team

        # which click
        clicked_on_refresh = n_clicks_Refresh == 1
        clicked_on_dartboard = clickData is not None
        clicked_on_canceled = n_clicks_Cancel == 1
        clicked_on_submit = n_clicks_Submit == 1
        clicked_on_precedent = n_clicks_precedent == 1

        if check_if_init(data_Fleches_Temp, game_att):
            data_Fleches_Temp = init_df_live(game_att)

        if (
            clicked_on_dartboard
            or clicked_on_canceled  # Something got clicked
            or clicked_on_submit
            or clicked_on_precedent
            or clicked_on_refresh
        ):

            if (
                clicked_on_dartboard
                and not clicked_on_canceled
                and not clicked_on_submit
                and not clicked_on_precedent
            ):
                # We enter here as soon as you click on the dart board
                clickData, Dart_Number, data_Fleches_Temp = Get_Click_Data(
                    clickData,
                    df_darts,
                    Dart_Number,
                    data_Fleches_Temp,
                    Team_Turn_index,
                    game_att["Darts_Total"],
                )

            if clicked_on_refresh:  # You clicked the refresh button
                n_clicks_Refresh = 0
                print("The refresh button has been pushed while having dynamic tabs ")
                data_Historique = load_var(local_path)

            elif (
                not clicked_on_dartboard
                and clicked_on_canceled
                and not clicked_on_submit
                and not clicked_on_precedent
            ):  # the cancel button has been pressed

                print("I can click on cancel button")
                Dart_Number = 0
                n_clicks_Cancel = 0

                data_Fleches_Temp = Cancel_Button(data_Fleches_Temp,
                                                  Team_Turn_index)

            elif (
                not clicked_on_dartboard
                and not clicked_on_canceled
                and clicked_on_submit
                and not clicked_on_precedent
            ):  # The submit button has been pressed

                print("I can click on submit button")

                data_Fleches_Temp = Update_Live_Player(
                    data_Fleches_Temp, Steps, N_Team, game_att["Team_List"]
                )

                Dart_Number = 0
                n_clicks_Submit = 0

                data_Fleches_Temp, data_Historique, Steps = Temp_To_Historique(
                    data_Fleches_Temp,
                    data_Historique,
                    Column_Storage,
                    game_att["Darts_Total"],
                    game_att["Team_List"],
                    Steps,
                    local_path,
                    Team_Turn_index,
                    Next_Team_index,
                    Dart_Number,
                )

            elif (
                not clicked_on_dartboard
                and not clicked_on_canceled
                and not clicked_on_submit
                and clicked_on_precedent
            ):  # The come back a player button has been pressed
                print("I can click on precedent button")
                n_clicks_precedent = 0
                if Steps:  # if it is pressed right at the beginning
                    Steps = Steps - 1  # think about this, maybe not true?
                    data_Fleches_Temp = Update_Live_Player(
                        data_Fleches_Temp, Steps, N_Team, game_att["Team_List"]
                    )
                    data_Historique = Remove_Last_Round(
                        data_Historique, game_att["Darts_Total"]
                    )

            Score_Table = init[5]
            Score_Table, data_Historique = Render_Score_Table(
                data_Historique,
                game_att["Team_List"],
                game_att["Cricket_Type"],
                Score_Table,
            )

            Save(local_path, "data_Historique.npy", data_Historique)

        Affichage = ["Tour numero: {}".format(int(Steps / N_Team) + 1)]

        return (
            Affichage,
            n_clicks_Refresh,
            n_clicks_Cancel,
            n_clicks_Submit,
            n_clicks_precedent,
            clickData,
            Dart_Number,
            data_Fleches_Temp,
            Score_Table,
        )

    return app, layout
