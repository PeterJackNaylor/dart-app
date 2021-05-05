import os

from numpy import savetxt
from numpy import loadtxt

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import pandas as pd

# from ..utils.plot_geojson import dart_plot

from .app_dashboard_functions import (discrete_background_color_bins,
                                      Which_Line,
                                      # Open_Or_Closed,
                                      # Tables_Up_to_Date,
                                      Cancel_Button,
                                      # Submit_Turn,
                                      Remove_Last_Round_New,
                                      Get_Click_Data,
                                      # Score_Update_Cricket,
                                      # Score_Update_Douze,
                                      # Douze_Turn,
                                      Storage_Player_Separation,
                                      # Update_Live_Stats,
                                      Update_Live_Graph,
                                      Update_Live_Player,
                                      Number_Open_Close_f,
                                      submit_score,
                                      Save_Everyone,
                                      End_Game)

from .html_components import (generate_tab_1,
                              generate_tab_2,
                              generate_tab_3)

from .styles_dash import tab_style


from .aux import init_db, load_local_dictionnary, load_var #load_local_cricket, 

GAME_NAME = "Bruno"


def create_ap(app, room_number):
    df_darts = pd.read_csv('ressources/mapping_dart_geojson.csv')
    local_path = f"ressources/local_games/{GAME_NAME}/{room_number}"

    Darts_Total = 3  # Maybe some games use a different number of darts....
    Cricket = ['20', '19', '18', '17', '16', '15', 'Bull', 'Score']
    Game = Cricket
    Cricket_Type = 'Cut_Throat'  # other mode is 'Cut_Throat'

    Team_List, n_t = load_local_dictionnary(local_path)
    game_att = {
        "Game": Game,
        "n_t": n_t,
        "Team_List": Team_List
    }
    init = init_db(Team_List, n_t, Cricket)
    Turn_Counter, Flechette_Compteur, Score_Storage, Y_Live_Stats = init[0:4]
    df_Score_Live_New_Way, df_Score, df_Stat_Live, Column_Live_Stats_Graph = init[4:8]
    fig_Stat, df_Score_Storage, legend, Column_Storage = init[8:12]

    layout = html.Div([
        dcc.Tabs(children=[
                generate_tab_1(Turn_Counter, Flechette_Compteur, Score_Storage,
                               Y_Live_Stats, Team_List, n_t, df_Score_Live_New_Way,
                               df_Score, tab_style, legend),
                generate_tab_2(df_Stat_Live, Column_Live_Stats_Graph, fig_Stat),
                generate_tab_3(df_Score_Storage)
            ]),
    ])

    # Callback called upon whenever you change player or you change the dartnumber. 
    # Puts up to date the display of the score tables
    @app.callback( 
        Output('Score_Table', 'style_header_conditional'),
        Output('Score_Table', 'style_data_conditional'),
        Output('Score_Live_New_Way', 'style_data_conditional'),
        Output('Historique_Partie', 'style_data_conditional'),

        Input('Dart_Counter', 'data'),
#        Input('Turn_Counter', 'data'),

        State('Score_Table', 'data'),
        State('Score_Live_New_Way', 'data'),
#        State('Team_Number', 'data'),
        State('Historique_Partie', 'data'),
    )
    def Update_PlayerTurn_Display(Dart_Number,# Turn_Counter, 
                                  data_Table, data_Live_New_Way, 
                                  # Team_Number_Game, 
                                  data_Historique):
                    # 'Partie_Historique.npy', 'Partie_Live.npy', 'Score.npy', 'Graph_Partie.npy', 'Stats_Partie.npy'
        var_to_load = ["Turn_Counter"]# , 'Partie_Historique', 'Stats_Partie']
        Turn_Counter = load_var(local_path, var_to_load, game_att)[0]
        Turn_Counter_Index = Turn_Counter % n_t
        
        Player_Line_Dart_Column = Which_Line(Turn_Counter_Index,
                                             data_Live_New_Way,
                                             Dart_Number)

        Player_Separation = Storage_Player_Separation(Turn_Counter)

        (styles, _) = discrete_background_color_bins(df_Score, 4, Game[:-1])
        # Shouldn't it be data_Table instead of df_Score?
        
        Number_Open_Close = Number_Open_Close_f("Cricket", n_t, data_Table,
                                                Turn_Counter_Index, Turn_Counter)

        ### Borders is something I'm working on, to color the border lines, doesn't work yet    
        # Borders ={
        #         'if': {'row_index': Turn_Counter % Team_Number_Game},
        #         'border': '1px solid blue'
                #'backgroundColor': 'rgb(250, 200, 250)',
                #'fontWeight': 'bold'
                # },
    #   { 'border': '1px solid blue' }
        
    #    styles.append(Borders)            
        
        return Number_Open_Close, styles, Player_Line_Dart_Column, Player_Separation


    ### Callback called upon whenever you click on the dart board, on a button (cancel, submit, previous)
    ### , or when the list of players is changed. It then updates the score accordingly.

    @app.callback(
        Output( 'Dart_Counter','data'),
        Output( 'cancel_round','n_clicks'),
        Output('Score_Table', 'data'),
        Output( 'submit_round','n_clicks'),
        # Output( 'Turn_Counter','data'),
        # Output( 'Score_Storage','data'),
        Output('basic-interactions', 'clickData'),
        Output('precedent_round', 'n_clicks'),
        Output( 'Joueur','children'),
        Output('Score_Live_New_Way', 'data'),    
        Output('Stat_Live', 'data'),
        Output('Historique_Partie','data'),
        # Output('Y_Live-Stat','data'),
        Output( 'Refresh','n_clicks'),
    #   Output('Graph_Live_Stat', 'figure'),
    #  Output('Stat_Graph', 'data'),

        Input('basic-interactions', 'clickData'),
        Input( 'Refresh','n_clicks'),
        Input('cancel_round','n_clicks'),
        Input('submit_round','n_clicks'),
        Input('precedent_round','n_clicks'),
        Input('Stat_Dropdown', 'value'),

        # State('Turn_Counter','data'),
        State('Dart_Counter','data'),
        # State('Score_Storage','data'),
        State('Score_Table', 'data'),
        State('Score_Live_New_Way', 'data'), 
        State('Stat_Live', 'data'),
        State('Historique_Partie','data'),
        State('Graph_Live_Stat', 'figure'),
        # State('Y_Live-Stat','data')
    #   State('Stat_Graph', 'data'),
        )

    def Score_All_In_One(clickData, n_clicks_Refresh, n_clicks_Cancel,#Input 
                         n_clicks_Submit, n_clicks_precedent, Dropdown_Value,
                         #Turn, 
                         Dart_Number, 
                         data_Table,#State 
                         data_Live_New_Way, Stat_Live, data_Historique,
                         fig_Stat_Live):#, Y_Live):
        print("data_Table", data_Table)
        # which click
        clicked_on_refresh = n_clicks_Refresh == 1
        clicked_on_dartboard = clickData is not None
        clicked_on_canceled = n_clicks_Cancel == 1
        clicked_on_submit = n_clicks_Submit == 1
        clicked_on_precedent = n_clicks_precedent == 1

        Team_List, n_t = load_local_dictionnary(local_path)
        
        for i in range(len(data_Live_New_Way) ):
            data_Live_New_Way[ i ]['Equipe'] = list(Team_List.keys())[i]
            data_Live_New_Way[ i ]["index"] = Team_List[list(Team_List.keys())[i]][0]
            


        var_to_load = ["Turn_Counter", 'data_Historique', 'Stat_Live',
                       'Score_History', 'data_Table', 'Y_Live']

        Turn, data_Historique, Stat_Live, Score_History, data_Table, Y_Live = load_var(local_path, var_to_load, game_att)
        print("Score history load", Score_History)
        print('Stat_Live load:',Stat_Live)

        if clicked_on_refresh: # You clicked the refresh button
            n_clicks_Refresh = 0
            var_to_load = ["Turn_Counter", 'Partie_Historique', 'Stat_Live',
                            'Score', 'Y_Live']
            Turn, data_Historique, Stat_Live, Score_History, data_Table, Y_Live = load_var(local_path, var_to_load, game_att)
            
     #   else : # This means the game has already started and we want to extract data from the files
        Team_Number_Game = len(list(Team_List.keys()))

        Turn_Number = int(Turn / Team_Number_Game) + 1
        Team_Turn = Turn % Team_Number_Game
        Next_Player = (Turn + 1) % Team_Number_Game

        data_Live_New_Way = Update_Live_Player(data_Live_New_Way,Turn, Team_Number_Game, Team_List)

        if (clicked_on_dartboard or # We enter here as soon as you click on the dart board
            clicked_on_canceled or 
            clicked_on_submit or 
            clicked_on_precedent):
            if (clicked_on_dartboard and # We enter here as soon as you click on the dart board
                not clicked_on_canceled and 
                not clicked_on_submit and
                not clicked_on_precedent):
            # We have not pressed cancel nor submit. We are therefore filling in the livetable    
                clickData, Dart_Number, data_Live_New_Way = Get_Click_Data(clickData,
                                                                            df_darts,
                                                                            Dart_Number,
                                                                            data_Live_New_Way,
                                                                            Team_Turn,
                                                                            Darts_Total)
            # if one of the three is clicked

            elif (not clicked_on_dartboard and
                clicked_on_canceled and 
                not clicked_on_submit and 
                not clicked_on_precedent): 
                # the cancel button has been pressed
                Dart_Number = 0 # reinitializing n_clicks and the dart number
                n_clicks_Cancel = 0
                data_Live_New_Way = Cancel_Button(data_Live_New_Way, Team_Turn)
                    
            elif (not clicked_on_dartboard and
                  not clicked_on_canceled and 
                  clicked_on_submit and 
                  not clicked_on_precedent):  
                # The submit button has been pressed
                Dart_Number = 0 # reinitialize the dart number
                n_clicks_Submit = 0 # reinitializing n_clicks
                
                outputs = submit_score("Cricket", Cricket_Type, data_Live_New_Way, Team_Turn, 
                                    Next_Player, Dart_Number, Turn, Team_Number_Game, data_Table, 
                                    Score_History, Darts_Total, data_Historique, Column_Storage, 
                                    Team_List, Stat_Live, Y_Live, local_path)
                data_Live_New_Way, Stat_Live, Y_Live, Turn, data_Historique, data_Table, Score_History = outputs
            #  Dart_Number, data_Table, data_Live_New_Way, Score_History = Submit_Turn(Turn, data_Live_New_Way, data_Table, Player_Turn, Next_Player, Player_Number_Game,Dart_Number, Score_History)

            elif (not clicked_on_dartboard and
                  not clicked_on_canceled and 
                  not clicked_on_submit and 
                  clicked_on_precedent): # The come back a player button has been pressed 
                n_clicks_precedent = 0
                if Turn: # if it is pressed right at the beginning
                    Player_Precedent = (Turn - 1) % Team_Number_Game
                    Turn = Turn - 1 # think about this, maybe not true?
                    print("score history", Score_History)
                    data_Table, Score_History, data_Historique, Stat_Live, fig_Stat_Live, Y_Live = Remove_Last_Round_New(Team_Number_Game, 
                                        data_Table, Score_History, Darts_Total, Player_Precedent,Game,Turn,data_Historique, Stat_Live, fig_Stat_Live, Y_Live)
                    print("score_history2", Score_History)

            Save_Everyone(local_path, Turn, Score_History, 
                          data_Historique, data_Table, Y_Live, Stat_Live)

            print("data", data_Live_New_Way)
            print("stat", Stat_Live)
            print("datahisto", data_Historique)

            # Game ending criteria. Saves all the data.   
            End_Game(data_Table,
                    Team_Number_Game,
                    Team_Turn,
                    Score_History,
                    Team_List,
                    Darts_Total,
                    Cricket)
            f2 = open(os.path.join(local_path, "Flechette_Compteur.txt"), "w")
            f2.write(str(Dart_Number))
            f2.close()

        Affichage = ['Tour numéro: {}'.format(Turn_Number) ]  

        print("data_Table2", )

        return Dart_Number, n_clicks_Cancel, data_Table, n_clicks_Submit, clickData, n_clicks_precedent, Affichage, data_Live_New_Way, Stat_Live, data_Historique, n_clicks_Refresh#, fig_Stat_Live, Y_Live #Stat_Graph_Live                

        # Output( 'Dart_Counter','data'),
        # Output( 'cancel_round','n_clicks'),
        # Output('Score_Table', 'data'),
        # Output( 'submit_round','n_clicks'),
        # Output('basic-interactions', 'clickData'),
        # Output('precedent_round', 'n_clicks'),
        # Output( 'Joueur','children'),
        # Output('Score_Live_New_Way', 'data'),    
        # Output('Stat_Live', 'data'),
        # Output('Historique_Partie','data'),
        # Output( 'Refresh','n_clicks'),


    @app.callback(

        Output('Graph_Live_Stat', 'figure'),
        Output('Button_Graph', 'n_clicks'),
    #  Output('Y_Live-Stat','data'),

        Input('Button_Graph', 'n_clicks'),
    # Input( 'cancel_round','n_clicks'),
    # Input( 'submit_round','n_clicks'),
    # Input( 'precedent_round','n_clicks'),

        State( 'Stat_Dropdown', 'value'),
        State('Stat_Live', 'data'),
        State('Graph_Live_Stat', 'figure'),
        # State('Y_Live-Stat','data'),
        # State( 'Turn_Counter','data'),
        # State( 'Score_Storage','data'),


    )


    def Update_Graphs(n_click_Graph, #Input
                      Dropdown_Value, Stat_Live, fig_Stat_Live): #State
                      # Y_Live,Turn, Score_History

        if n_click_Graph:
            n_click_Graph = 0
            # , 'Partie_Live.npy', 'Score.npy', 'Graph_Partie.npy', 
            # output = load_local_cricket(local_path, data_Table, data_Historique)
            # 'Partie_Historique.npy', 'Partie_Live.npy', 'Score.npy', 'Graph_Partie.npy', 'Stats_Partie.npy'
            var_to_load = ["Turn_Counter", 'Partie_Historique', 'Stat_Live']
            Turn, Score_History, Y_live = load_var(local_path, var_to_load, game_att)
            Team_Number_Game = len(list(Team_List.keys()))
            Team_Turn = Turn % Team_Number_Game    
            
            fig_Stat_Live = Update_Live_Graph(Stat_Live,Team_Turn,
                                              list(Team_List.keys()),
                                              Y_Live,fig_Stat_Live,
                                              Dropdown_Value,
                                              Column_Live_Stats_Graph,
                                              Score_History)

        return fig_Stat_Live, n_click_Graph


    return app, layout


            

 
        

if __name__ == '__main__':
    app.run_server(debug = True, port = 8000)