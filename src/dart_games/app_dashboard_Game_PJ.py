import os
from dash_core_components import Dropdown

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
                                      #Update_Live_Graph,
                                      Update_Live_Player,
                                      Number_Open_Close_f,
                                      submit_score,
                                      Get_Stats,
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

    game_att = load_local_dictionnary(local_path, "Cricket")
    layout = cricket_layout(local_path)
 
   
    
    @app.callback(
        Output('tab-content', 'children'),
        
        Input('tabs', 'value')


        )


    def render_content(tab):
       

        print('i m in render content')

        game_att = load_local_dictionnary(local_path, "Cricket")

        init = init_db(game_att)
        Turn_Counter, Flechette_Compteur, Score_Storage, Y_Live_Stats = init[0:4]
        df_Score_Live_New_Way, df_Score, Stats_Table, Stats_Graph = init[4:8]
        data_Historique, legend = init[8:10]

        var_to_load = ["Turn_Counter", 'data_Historique',
                        'data_Table']
            
        Turn, data_Historique,  data_Table = load_var(local_path, var_to_load, game_att)

        
        if tab == 'tab-main':

            return generate_tab_1(Turn_Counter,Flechette_Compteur,df_Score_Live_New_Way,df_Score, legend)


        elif tab == 'tab-stat':
            
            Dropdown_Value = '# Touche/ Tour'
            Stats_Table, Stats_Graph = Get_Stats(data_Historique, Stats_Table, game_att['Team_List'],Stats_Graph,Dropdown_Value)


            return generate_tab_2(Stats_Table, Stats_Graph)
            
        elif tab == 'tab-historique':           

            return generate_tab_3(data_Historique, game_att['Team_List'])


    @app.callback(
        Output('Graph_Live_Stat', 'figure'),  
        Output('Stat_Dropdown', 'value'),
     
        Input('Stat_Dropdown', 'value')

        )


    def Update_DropdownValue(Dropdown_Value):

        print('Dropdown triggered this')

        game_att = load_local_dictionnary(local_path, "Cricket")
        var_to_load = ['data_Historique']
        init = init_db(game_att)
        data_Historique, legend = init[8:10]

            
        data_Historique = load_var(local_path, var_to_load, game_att)[0]

            


        init = init_db(game_att)
        Stats_Table, Stats_Graph = init[6:8]


        
        Stats_Table, Stats_Graph = Get_Stats(data_Historique, Stats_Table, game_att['Team_List'],Stats_Graph,Dropdown_Value)

        print('Stats Graph:', Stats_Graph)

        return Stats_Graph, Dropdown_Value



    # Callback called upon whenever you change player or you change the dartnumber. 
    # Puts up to date the display of the score tables
    @app.callback( 
        Output('Score_Table', 'style_header_conditional'),
        Output('Score_Table', 'style_data_conditional'),
        Output('Score_Live_New_Way', 'style_data_conditional'),

        Input('Dart_Counter', 'data'),

        State('Score_Table', 'data'),
        State('Score_Live_New_Way', 'data'),

    )
    def Update_PlayerTurn_Display(Dart_Number,# Turn_Counter, 
                                  data_Table, data_Live_New_Way, 
                                  # Team_Number_Game, 
                                  ##data_Historique
                                  ):
                    # 'Partie_Historique.npy', 'Partie_Live.npy', 'Score.npy', 'Graph_Partie.npy', 'Stats_Partie.npy'

        print('i m in ipdate playerturn display')
        game_att = load_local_dictionnary(local_path, "Cricket")
        var_to_load = ["Turn_Counter"]# , 'Partie_Historique', 'Stats_Partie']
        Turn_Counter = load_var(local_path, var_to_load, game_att)[0]
        Turn_Counter_Index = Turn_Counter % game_att['n_t']
        
        Player_Line_Dart_Column = Which_Line(Turn_Counter_Index,
                                             data_Live_New_Way,
                                             Dart_Number)

##        Player_Separation = Storage_Player_Separation(Turn_Counter)

        (styles, _) = discrete_background_color_bins(pd.DataFrame(data_Table), 4, game_att['Game'][:-2])
        # Shouldn't it be data_Table instead of df_Score?

        Number_Open_Close = Number_Open_Close_f("Cricket", game_att['n_t'], data_Table,
                                                Turn_Counter_Index, Turn_Counter)

                  
        
        return Number_Open_Close, styles, Player_Line_Dart_Column
        ##, Player_Separation


    ### Callback called upon whenever you click on the dart board, on a button (cancel, submit, previous)
    ### , or when the list of players is changed. It then updates the score accordingly.

    @app.callback(

        Output('Joueur','children'),

        Output('Refresh','n_clicks'),
        Output('cancel_round','n_clicks'),
        Output('submit_round','n_clicks'),
        Output('precedent_round', 'n_clicks'),


        Output('basic-interactions', 'clickData'),
        Output('Dart_Counter','data'),


        Output('Score_Live_New_Way', 'data'),
        Output('Score_Table', 'data'),
    


        Input('Refresh','n_clicks'),
        Input('cancel_round','n_clicks'),
        Input('submit_round','n_clicks'),
        Input('precedent_round', 'n_clicks'),

        Input('basic-interactions', 'clickData'),

        State('Dart_Counter','data'),
        State('Score_Live_New_Way', 'data'),
        State('Score_Table', 'data'),

 




        )
    def Tab_Game_Callback(n_clicks_Refresh, n_clicks_Cancel, n_clicks_Submit, n_clicks_precedent, clickData,
                            Dart_Number, data_Live_New_Way, data_Table):


        game_att = load_local_dictionnary(local_path, "Cricket")

        var_to_load = ["Turn_Counter", 'data_Historique',
                        'data_Table']

        Turn, data_Historique, data_Table = load_var(local_path, var_to_load, game_att)


        # which click
        clicked_on_refresh = n_clicks_Refresh == 1
        clicked_on_dartboard = clickData is not None
        clicked_on_canceled = n_clicks_Cancel == 1
        clicked_on_submit = n_clicks_Submit == 1
        clicked_on_precedent = n_clicks_precedent == 1

        if check_if_init(data_Live_New_Way, game_att):
            data_Live_New_Way = init_df_live(game_att).to_dict('records')


        if clicked_on_refresh: # You clicked the refresh button
            n_clicks_Refresh = 0
            print('The refresh button has been pushed whuile having dynamic tabs')

            Turn, data_Historique,  data_Table= load_var(local_path, var_to_load, game_att)


        Team_Number_Game = game_att['n_t']

        Turn_Number = int(Turn / Team_Number_Game) + 1
        Team_Turn = Turn % Team_Number_Game
        Next_Player = (Turn + 1) % Team_Number_Game

        
        if (clicked_on_dartboard or # Something got clicked
            clicked_on_canceled or 
            clicked_on_submit or 
            clicked_on_precedent):



            if (clicked_on_dartboard and # We enter here as soon as you click on the dart board
                not clicked_on_canceled and 
                not clicked_on_submit and
                not clicked_on_precedent):

                print('I can click on dart board')


                clickData, Dart_Number, data_Live_New_Way = Get_Click_Data(clickData,
                                                                           df_darts,
                                                                           Dart_Number,
                                                                           data_Live_New_Way,
                                                                           Team_Turn,
                                                                           game_att["Darts_Total"])
            
            
            if clicked_on_refresh: # You clicked the refresh button
                n_clicks_Refresh = 0
                print('The refresh button has been pushed whuile having dynamic tabs')
                Turn, data_Historique, data_Table = load_var(local_path, var_to_load, game_att)


            elif (not clicked_on_dartboard and
                clicked_on_canceled and 
                not clicked_on_submit and 
                not clicked_on_precedent):                 # the cancel button has been pressed

                print('I can click on cancel button')
                Dart_Number = 0 # reinitializing n_clicks and the dart number
                n_clicks_Cancel = 0

                data_Live_New_Way = Cancel_Button(data_Live_New_Way, Team_Turn)

            elif (not clicked_on_dartboard and
                  not clicked_on_canceled and 
                  clicked_on_submit and 
                  not clicked_on_precedent):                 # The submit button has been pressed
                print('I can click on submit button')

                data_Live_New_Way = Update_Live_Player(data_Live_New_Way,Turn, Team_Number_Game, game_att['Team_List'])
                
                Dart_Number = 0 # reinitialize the dart number
                n_clicks_Submit = 0 # reinitializing n_clicks

                outputs = submit_score("Cricket", game_att['Cricket_Type'], data_Live_New_Way, Team_Turn, 
                                    Next_Player, Dart_Number, Turn, Team_Number_Game, data_Table, 
                                    game_att['Darts_Total'], data_Historique, Column_Storage, 
                                    game_att['Team_List'], local_path)
                                
                data_Live_New_Way, Turn, data_Historique, data_Table = outputs
            
            
            elif (not clicked_on_dartboard and
                  not clicked_on_canceled and 
                  not clicked_on_submit and 
                  clicked_on_precedent): # The come back a player button has been pressed 
                print('I can click on precedent button')
                n_clicks_precedent = 0
                if Turn: # if it is pressed right at the beginning
                    Player_Precedent = (Turn - 1) % Team_Number_Game
                    Turn = Turn - 1 # think about this, maybe not true?
                    data_Live_New_Way = Update_Live_Player(data_Live_New_Way,Turn, Team_Number_Game, game_att['Team_List'])
                    outputs = Remove_Last_Round_New(Team_Number_Game, data_Table, 
                                                    game_att['Darts_Total'], Player_Precedent,
                                                    game_att['Game'], Turn, data_Historique)
                    data_Table, data_Historique = outputs

            Save_Everyone(local_path, Turn, 
                          data_Historique, data_Table)


        Affichage = ['Tour numéro: {}'.format(Turn_Number) ] 

        return (Affichage,
        n_clicks_Refresh, n_clicks_Cancel, n_clicks_Submit, n_clicks_precedent, 
        clickData, Dart_Number,
         data_Live_New_Way, data_Table)




  

    return app, layout


if __name__ == '__main__':
    app.run_server(debug = True, port = 8000)