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

from .html_components import cricket_layout, generate_tab_1, generate_tab_2, generate_tab_3

from .styles_dash import tab_style


from .aux import (init_db,
                  load_local_dictionnary,
                  load_var,
                  init_df_live,
                  check_if_init,
                  Column_Storage,
                  Column_Live_Stats_Graph) #load_local_cricket, 

GAME_NAME = "Bruno"

def create_ap(app, room_number):
    df_darts = pd.read_csv('ressources/mapping_dart_geojson.csv')
    local_path = f"ressources/local_games/{GAME_NAME}/{room_number}"

    layout = cricket_layout(local_path)


    @app.callback(
        Output('tab-content', 'children'),
        Input('tabs', 'value'))


    def render_content(tab):

        game_att = load_local_dictionnary(local_path, "Cricket")

        init = init_db(game_att)
        Turn_Counter, Flechette_Compteur, Score_Storage, Y_Live_Stats = init[0:4]
        df_Score_Live_New_Way, df_Score, df_Stat_Live, fig_Stat = init[4:8]
        df_Score_Storage, legend = init[8:10]
        
        if tab == 'tab-main':

            return generate_tab_1(Turn_Counter, Flechette_Compteur, Score_Storage,
                               Y_Live_Stats, game_att['Team_List'], game_att['n_t'], 
                               df_Score_Live_New_Way,
                               df_Score, tab_style, legend)

          #  return generate_tab_1(Turn_Counter, Flechette_Compteur, Score_Storage,
          #                     Y_Live_Stats, game_att['Team_List'], game_att['n_t'], 
          #                     df_Score_Live_New_Way,
          #                     df_Score, tab_style, legend)

        elif tab == 'tab-stat':
            return generate_tab_2(df_Stat_Live, fig_Stat)
            
        elif tab == 'tab-historique':
            return generate_tab_3(df_Score_Storage)



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
        game_att = load_local_dictionnary(local_path, "Cricket")
        var_to_load = ["Turn_Counter"]# , 'Partie_Historique', 'Stats_Partie']
        Turn_Counter = load_var(local_path, var_to_load, game_att)[0]
        Turn_Counter_Index = Turn_Counter % game_att['n_t']
        
        Player_Line_Dart_Column = Which_Line(Turn_Counter_Index,
                                             data_Live_New_Way,
                                             Dart_Number)

        Player_Separation = Storage_Player_Separation(Turn_Counter)

        (styles, _) = discrete_background_color_bins(pd.DataFrame(data_Table), 4, game_att['Game'][:-1])
        # Shouldn't it be data_Table instead of df_Score?
        print('data_Table', data_Table)
        print(game_att)
        Number_Open_Close = Number_Open_Close_f("Cricket", game_att['n_t'], data_Table,
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
        Output('Dart_Counter','data'),
        Output('cancel_round','n_clicks'),
        Output('Score_Table', 'data'),
        Output('submit_round','n_clicks'),
        Output('basic-interactions', 'clickData'),
        Output('precedent_round', 'n_clicks'),
        Output('Joueur','children'),
        Output('Score_Live_New_Way', 'data'),    
        Output('Stat_Live', 'data'),
        Output('Historique_Partie','data'),
        Output('Refresh','n_clicks'),

        Input('basic-interactions', 'clickData'),
        Input('Refresh','n_clicks'),
        Input('cancel_round','n_clicks'),
        Input('submit_round','n_clicks'),
        Input('precedent_round','n_clicks'),
        Input('Stat_Dropdown', 'value'),

        State('Dart_Counter','data'),
        State('Score_Table', 'data'),
        State('Score_Live_New_Way', 'data'), 
        State('Stat_Live', 'data'),
        State('Historique_Partie','data'),
        State('Graph_Live_Stat', 'figure'),
        )

    def Score_All_In_One(clickData, n_clicks_Refresh, n_clicks_Cancel,#Input 
                         n_clicks_Submit, n_clicks_precedent, Dropdown_Value,
                         Dart_Number, 
                         data_Table, data_Live_New_Way, Stat_Live, #State 
                         data_Historique, fig_Stat_Live):#, Y_Live):

        # global var
        print('Im here!!!!!!!')
        game_att = load_local_dictionnary(local_path, "Cricket")

        var_to_load = ["Turn_Counter", 'data_Historique', 'Stat_Live',
                       'Score_History', 'data_Table', 'Y_Live']
        Turn, data_Historique, Stat_Live, Score_History, data_Table, Y_Live = load_var(local_path, var_to_load, game_att)

        # which click
        clicked_on_refresh = n_clicks_Refresh == 1
        clicked_on_dartboard = clickData is not None
        clicked_on_canceled = n_clicks_Cancel == 1
        clicked_on_submit = n_clicks_Submit == 1
        clicked_on_precedent = n_clicks_precedent == 1

        if check_if_init(data_Live_New_Way, game_att):
            data_Live_New_Way = init_df_live(game_att).to_dict('records')

        if len( Y_Live) != 0:
            for i in range (0, len( Y_Live)) :
                for j in range (0, len(Y_Live[i])-1): 
                    Y_Live[i][j]= float(Y_Live[i][j])
        print('Y_Live load:',Y_Live)
        if clicked_on_refresh: # You clicked the refresh button
            n_clicks_Refresh = 0
            print('The refresh button has been pushed whuile having dynamic tabs')

            Turn, data_Historique, Stat_Live, Score_History, data_Table, Y_Live = load_var(local_path, var_to_load, game_att)
            
        Team_Number_Game = game_att['n_t']

        Turn_Number = int(Turn / Team_Number_Game) + 1
        Team_Turn = Turn % Team_Number_Game
        Next_Player = (Turn + 1) % Team_Number_Game

        if (clicked_on_dartboard or # We enter here as soon as you click on the dart board
            clicked_on_canceled or 
            clicked_on_submit or 
            clicked_on_precedent):
            
            print('Interaction with dash while having dynamic tabs')

            
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
                                                                           game_att["Darts_Total"])
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
                data_Live_New_Way = Update_Live_Player(data_Live_New_Way,Turn, Team_Number_Game, game_att['Team_List'])
                # The submit button has been pressed
                Dart_Number = 0 # reinitialize the dart number
                n_clicks_Submit = 0 # reinitializing n_clicks
                outputs = submit_score("Cricket", game_att['Cricket_Type'], data_Live_New_Way, Team_Turn, 
                                    Next_Player, Dart_Number, Turn, Team_Number_Game, data_Table, 
                                    Score_History, game_att['Darts_Total'], data_Historique, Column_Storage, 
                                    game_att['Team_List'], Stat_Live, Y_Live, local_path)
                data_Live_New_Way, Stat_Live, Y_Live, Turn, data_Historique, data_Table, Score_History = outputs

            elif (not clicked_on_dartboard and
                  not clicked_on_canceled and 
                  not clicked_on_submit and 
                  clicked_on_precedent): # The come back a player button has been pressed 
                n_clicks_precedent = 0
                if Turn: # if it is pressed right at the beginning
                    Player_Precedent = (Turn - 1) % Team_Number_Game
                    Turn = Turn - 1 # think about this, maybe not true?
                    data_Live_New_Way = Update_Live_Player(data_Live_New_Way,Turn, Team_Number_Game, game_att['Team_List'])

                    outputs = Remove_Last_Round_New(Team_Number_Game, data_Table, Score_History,
                                                    game_att['Darts_Total'], Player_Precedent,
                                                    game_att['Game'], Turn, data_Historique,
                                                    Stat_Live, fig_Stat_Live, Y_Live)
                    data_Table, Score_History, data_Historique, Stat_Live, fig_Stat_Live, Y_Live = outputs

            Save_Everyone(local_path, Turn, Score_History, 
                          data_Historique, data_Table, Y_Live, 
                          Stat_Live)

            # Game ending criteria. Saves all the data.   
            End_Game(data_Table,
                    Team_Number_Game,
                    Team_Turn,
                    Score_History,
                    game_att['Team_List'],
                    game_att['Darts_Total'],
                    game_att['Game'])
            f2 = open(os.path.join(local_path, "Flechette_Compteur.txt"), "w")
            f2.write(str(Dart_Number))
            f2.close()

        Affichage = ['Tour numéro: {}'.format(Turn_Number) ]  


        return (Dart_Number, n_clicks_Cancel, data_Table, n_clicks_Submit,
                clickData, n_clicks_precedent, Affichage, data_Live_New_Way,
                Stat_Live, data_Historique, n_clicks_Refresh)


    @app.callback(
        Output('Graph_Live_Stat', 'figure'),
        Output('Button_Graph', 'n_clicks'),

        Input('Button_Graph', 'n_clicks'),

        State( 'Stat_Dropdown', 'value'),
        State('Stat_Live', 'data'),
        State('Graph_Live_Stat', 'figure'),
    )
    def Update_Graphs(n_click_Graph, #Input
                      Dropdown_Value, Stat_Live, fig_Stat_Live): #State


        if n_click_Graph:
            print('J ai clicke sur le bbouton mise a jour graph')
            n_click_Graph = 0
            game_att = load_local_dictionnary(local_path, "Cricket")
            var_to_load = ["Turn_Counter", 'Partie_Historique', 'Stat_Live']
            Turn, Score_History, Y_live = load_var(local_path, var_to_load, game_att)
            Team_Number_Game = game_att['n_t']
            Team_Turn = Turn % Team_Number_Game    
            
            fig_Stat_Live = Update_Live_Graph(Stat_Live,Team_Turn,
                                              list(game_att['Team_List'].keys()),
                                              Y_Live,fig_Stat_Live,
                                              Dropdown_Value,
                                              Column_Live_Stats_Graph,
                                              Score_History)

        return fig_Stat_Live, n_click_Graph

    return app, layout


if __name__ == '__main__':
    app.run_server(debug = True, port = 8000)