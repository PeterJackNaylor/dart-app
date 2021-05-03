import os
import numpy as np

from numpy import savetxt
from numpy import loadtxt

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table

import pandas as pd
import plotly.express as px

from ..utils.pickle import open_dic
from ..utils.plot_geojson import dart_plot

from .app_dashboard_functions import (discrete_background_color_bins,
                                      Which_Line,
                                      Open_Or_Closed,
                                      # Tables_Up_to_Date,
                                      Cancel_Button,
                                      Submit_Turn,
                                      Remove_Last_Round_New,
                                      Get_Click_Data,
                                      Score_Update_Cricket,
                                      Score_Update_Douze,
                                      Douze_Turn,
                                      Storage_Player_Separation,
                                      Update_Live_Stats,
                                      Update_Live_Graph,
                                      Update_Live_Player,
                                      Save_Everyone)


# mise a jour du tableau df_players

# the end of game criteria takes the data of the next player.

GAME_NAME = "Bruno"


def create_ap(app, room_number):
    local_path = f"ressources/local_games/{GAME_NAME}/{room_number}"

    styles = {
        'pre': {
            'border': 'thin lightgrey solid',
            'overflowX': 'scroll'
        }
    }

    tab_style = {
        'borderBottom': '1px solid #d6d6d6',
        'padding': '6px',
        'fontWeight': 'bold'
    }

    tab_selected_style = {
        'borderTop': '1px solid #d6d6d6',
        'borderBottom': '1px solid #d6d6d6',
        'backgroundColor': '#119DFF',
        'color': 'white',
        'padding': '6px'
    }

    Score_Storage = []

    fig = dart_plot()

  

    if os.path.isdir(local_path):
        print("loading local files")
        dic = open_dic(os.path.join(local_path, "meta.pickle"))
        print(dic)



            

    #    if len(os.listdir(local_path)) == 1 : # This means we have just created the folder, we therefore need to initialize everybody
    #        Turn_Counter = 0
    #        Flechette_Compteur = 0
    #        f1 = open(os.path.join(local_path, "Turn_Counter.txt"), "x")
    #        f1.write(str(Turn_Counter))
    #        f1.close()

    #        f2 = open(os.path.join(local_path, "Flechette_Compteur.txt"), "x")
    #        f2.write(str(Flechette_Compteur))
    #        f2.close()






#        else : # This means the game has already started and we need to load existing files.
    else:
        print("taking default dic")
        dic = {"teams": ["Blue", "Red"],
               "picked_players": ["Peter", "Bruno"],
               "picked_game": "Just a template"}

        Turn_Counter = 0
        Flechette_Compteur = 0

        # f1 = open(os.path.join(local_path, "Turn_Counter.txt"), "x")
        # f1.write(str(Turn_Counter))
        # f1.close()

        # f2 = open(os.path.join(local_path, "Flechette_Compteur.txt"), "x")
        # f2.write(str(Flechette_Compteur))
        # f2.close()

    Team_List = {}
    for i, t in enumerate(dic["teams"]):
        player = dic["picked_players"][i]
        if t in Team_List.keys():
            Team_List[t].append(player)
        else:
            Team_List[t] = [player]

    n_t = len(Team_List)

    Cricket = ['20', '19', '18', '17', '16', '15', 'Bull', 'Score']
    Douze = ['12', '13', '14', 'Double', '15', '16', '17', 'Triple',
             '18', '19', '20', 'Bull', 'Score']
    Cricket_Type = 'Cut_Throat'  # other mode is 'Cut_Throat'

    # Game = Douze
    Game = Cricket


    Score_Live = [[t] + [None]*6 for t in Team_List]

#    Turn_Counter = 0
#    Flechette_Compteur = 0
    Darts_Total = 3  # Maybe some games use a different number of darts....

    df_darts = pd.read_csv('ressources/mapping_dart_geojson.csv')

    df_Score = pd.DataFrame(np.zeros((n_t, len(Game)), dtype=int),
                            columns=Game, index=list(Team_List.keys()))

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

    Column_Live_Stats_Graph = ['# Touche/ Tour',
                               '# de triple',
                               '# de double',
                               '# de tour à vide',
                               'Longest streak',
                               'Tour',
                               'Player']

    init_graph_live = np.zeros((n_t, len(Column_Live_Stats_Graph)), dtype=int)

    df_Graph_Live = pd.DataFrame(init_graph_live,
                                 columns=Column_Live_Stats_Graph)
    df_Graph_Live["index"] = list(Team_List.keys())

    fig_Stat = px.scatter(df_Graph_Live,
                          x="Tour",
                          y="# Touche/ Tour",
                          color=list(Team_List.keys()),
                          hover_data=[]) #,size='petal_length', hover_data=['Dernier_Tour'])
    Y_Live_Stats = [[0] * len(Column_Live_Stats_Graph)]

    for i in range(0, n_t):
        fig_Stat.data[i].update(mode='markers+lines')



    (styles, legend) = discrete_background_color_bins(df_Score, 4, Game[:-1])

    first_dash_table =[{'name': ['Joueur', ''], 'id': 'index'},{'name': ['Equipe', ''], 'id': 'Equipe'},
            {'name': ['Fleche 1', 'Value'], 'id': 'Fleche 1'},
            {'name': ['Fleche 1', 'Coef'], 'id': 'Coef 1'},
            {'name': ['Fleche 2', 'Value'], 'id': 'Fleche 2'},
            {'name': ['Fleche 2', 'Coef'], 'id': 'Coef 2'},
            {'name': ['Fleche 3', 'Value'], 'id': 'Fleche 3'},
            {'name': ['Fleche 3', 'Coef'], 'id': 'Coef 3'}]

    layout = html.Div([
        
        dcc.Tabs(children = [
                dcc.Tab(label='Game',
                        style=tab_style,
                        selected_style=tab_selected_style, 
                        children = [    
                            
                            dcc.Store(id='Dart_Counter',
                                      data=Flechette_Compteur),#, storage_type = 'session'),
                      
                            html.Div([
                                #Maybe useless, button to update game if it has been closed
                                html.Button('Mise à jour',
                                    id='Refresh',
                                    n_clicks=0),
                                
                                ### Maybe useless, a display to indicate how many turns have been played
                                html.H1(id='Joueur',
                                        children=['Tour numéro: {}'.format(Turn_Counter)]),
                                # html.H1(children= ' "{}"'.format(df_Score_Live_New_Way['index'][Turn_Counter]),id= 'Joueur1' ),
                            ]), 
                            ### Buttons to submit the darts inputs, cancel the input, or go back to the previous player
                            html.Button('Valider ce tour',
                                        id='submit_round',
                                        n_clicks=0),
                            html.Button('Annuler ce tour',
                                        id='cancel_round',
                                        n_clicks=0),
                            html.Button('Revenir au joueur precedent ',
                                        id='precedent_round', 
                                        n_clicks=0),
                            html.Div([
                                html.Div([
                                    # Table that shows what each player did on his/her last round. 
                                    dash_table.DataTable(
                                                id='Score_Live_New_Way',
                                                columns=first_dash_table,
                    
                            data = df_Score_Live_New_Way.to_dict('records'),
                            style_cell={'textAlign': 'center'},
                            style_table={
                            'maxHeight': '50ex',
                            'width': '100%',
                            'minWidth': '100%',
                            "horizontalAlign": "bottom"
                            },
                            style_data_conditional=[
                        
                                {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgb(248, 248, 248)'
                                },
                                {
                                'if': {'row_index': Turn_Counter},
                                'backgroundColor': 'rgb(250, 200, 250)',
                                'fontWeight': 'bold'
                                }
                            ],
                            style_header={
                                'backgroundColor': 'rgb(230, 230, 230)',
                                'fontWeight': 'bold'
                            },
                            
                            merge_duplicate_headers=True
                    
                            ) 
                        ], className="six columns"),
                    
                    html.Div([


                        ### Table displaying the total score (refreshes only after submission of the round)
                        dash_table.DataTable(
                            id='Score_Table',
                            columns = [{"name": i, "id": i} for i in df_Score.columns],
                            data = df_Score.to_dict('records'),
                            style_cell={'textAlign': 'center'},
                            style_table={
                                'maxHeight': '50ex',
                                'width': '100%',
                                'minWidth': '100%',
                                "horizontalAlign": "bottom"
                            },
                            style_data_conditional= styles 
                                ,
                            style_header={
                                'backgroundColor': 'rgb(230, 230, 230)',
                                'fontWeight': 'bold'
                                },
                                        
                            editable=True,
                            ),
                        html.Div(legend, style={'float': 'right'}),

                        
            ], className="six columns"),
                    
                    ], className="row"),
                
    

                # Display the dartboard



                dcc.Graph(
                    id='basic-interactions',
                    figure=fig
                )
            ]),

            dcc.Tab(label = 'Live_Stats', style = tab_style, selected_style= tab_selected_style, children = [
        
        
                dash_table.DataTable(
                        id='Stat_Live',
                        columns = [{"name": i, "id": i} for i in df_Stat_Live.columns],
                        style_cell={'textAlign': 'center'},
                        style_table={
                            'maxHeight': '50ex',
                            'width': '100%',
                            'minWidth': '100%',
                            },
                        style_data_conditional=[
                
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgb(243, 243, 243)'
                                }
                            ],
                        style_header={
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'fontWeight': 'bold'
                            },
                
                
                        data = df_Stat_Live.to_dict('records'),

                ),
                

                dcc.Dropdown(
                    id='Stat_Dropdown',
                    options=[ {'label': Column_Live_Stats_Graph[i], 'value': i} for i in range (0, len(Column_Live_Stats_Graph)) 
    #                options=[ {'label': Column_Live_Stats_Graph[i], 'value': Column_Live_Stats_Graph[i]} for i in range (0, len(Column_Live_Stats_Graph)) 
                    ],
                    value= 0
    #                value= Column_Live_Stats_Graph[0]

                ),
                
                dcc.Graph(
                    id='Graph_Live_Stat',
                    animate = True,
                    figure=fig_Stat
                ),
                
                html.Button('Mise à jour Graphiques', id='Button_Graph', n_clicks=0),


            ]),
            dcc.Tab(label = 'Historique', style = tab_style, selected_style= tab_selected_style, children = [
        
        
                dash_table.DataTable(
                        id='Historique_Partie',
                        columns = [{"name": i, "id": i} for i in df_Score_Storage.columns],
                        style_cell={'textAlign': 'center'},
                        style_table={
                            'maxHeight': '50ex',
                            'width': '100%',
                            'minWidth': '100%',
                            },
                        style_data_conditional=[
                
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgb(248, 248, 248)'
                                }
                    
                            ],
                        style_header={
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'fontWeight': 'bold'
                            },
                
                
                        data = df_Score_Storage.to_dict('records'),

                ),
                
                    
            ]),
        ]),
        
        
    ])


    

    ### Callback called upon whenever you change player or you change the dartnumber. Puts up to date the display of the score tables
    @app.callback( 
        Output( 'Score_Table','style_header_conditional'),
        Output( 'Score_Table','style_data_conditional'),
        Output( 'Score_Live_New_Way','style_data_conditional'),
        Output( 'Historique_Partie','style_data_conditional'),

        
        Input( 'Dart_Counter','data'),
    #    Input( 'Turn_Counter','data'),
        State('Score_Table', 'data'),
        State('Score_Live_New_Way', 'data')   ,
    #    State('Team_Number', 'data'),
        State( 'Historique_Partie','data'),

        
        
    )

    def Update_PlayerTurn_Display(Dart_Number, data_Table, data_Live_New_Way, data_Historique):
        
        f1 = open(os.path.join(local_path, "Turn_Counter.txt"), "r")
        f2 = open(os.path.join(local_path, "Flechette_Compteur.txt"), "r")
        Turn_Counter = int(f1.read())
        Dart_number = int(f2.read())

        Team_Number_Game = n_t
        Turn_Counter_Index = Turn_Counter % Team_Number_Game
        
        Player_Line_Dart_Column = Which_Line(Turn_Counter_Index, data_Live_New_Way, Dart_Number)


        if Turn_Counter > 1 :
            Player_Separation = Storage_Player_Separation(data_Historique)
        else:
            Player_Separation = [
                
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgb(248, 248, 248)'
                                }
                    
                            ]

        (styles, legend) = discrete_background_color_bins(df_Score, 4, Game[:-1]) # Shouldn't it be data_Table instead of df_Score?
        

        if Game == Cricket:
        
            Number_Open_Close = Open_Or_Closed(Game,
                                               Team_Number_Game,
                                               data_Table,
                                               Turn_Counter_Index)
        
        elif Game == Douze:

            Number_Open_Close = Douze_Turn(Game, int( Turn_Counter / Team_Number_Game ) ) 

        ### Borders is something I'm working on, to color the border lines, doesn't work yet    
        Borders ={
                'if': {'row_index': Turn_Counter % Team_Number_Game},
                'border': '1px solid blue'
                #'backgroundColor': 'rgb(250, 200, 250)',
                #'fontWeight': 'bold'
                },
    #   { 'border': '1px solid blue' }
        
    #    styles.append(Borders)            
        
        return Number_Open_Close , styles , Player_Line_Dart_Column, Player_Separation
                            
                    
        

    ### Callback called upon whenever you click on the dart board, on a button (cancel, submit, previous)
    ### , or when the list of players is changed. It then updates the score accordingly.

    @app.callback(
        Output( 'Dart_Counter','data'),
        Output( 'cancel_round','n_clicks'),
        Output('Score_Table', 'data'),
        Output( 'submit_round','n_clicks'),
        Output('basic-interactions', 'clickData'),
        Output('precedent_round', 'n_clicks'),
        Output( 'Joueur','children'),
        Output('Score_Live_New_Way', 'data'),    
        Output('Stat_Live', 'data'),
        Output('Historique_Partie','data'),
        Output( 'Refresh','n_clicks'),



        
        Input('basic-interactions', 'clickData'),
        Input( 'Refresh','n_clicks'),
        Input( 'cancel_round','n_clicks'),
        Input( 'submit_round','n_clicks'),
        Input( 'precedent_round','n_clicks'),
        Input( 'Stat_Dropdown', 'value'),


        

        State( 'Dart_Counter','data'),
        State('Score_Table', 'data'),
        State('Score_Live_New_Way', 'data'), 
        State('Stat_Live', 'data'),
        State('Historique_Partie','data'),
        State('Graph_Live_Stat', 'figure'),


        
        )

    def Score_All_In_One(clickData, n_clicks_Refresh, n_clicks_Cancel, n_clicks_Submit, n_clicks_precedent, Dropdown_Value,  Dart_Number, data_Table, data_Live_New_Way, Stat_Live, data_Historique, fig_Stat_Live):
        
        Team_List = {}
        dic = open_dic(os.path.join(local_path, "meta.pickle"))
        print(dic)
        
        for i, t in enumerate(dic["teams"]):
            player = dic["picked_players"][i]
            

            if t in Team_List.keys():
                Team_List[t].append(player)
            else:
                Team_List[t] = [player]

        n_t = len(Team_List)

        
        index_3 = [Team_List[list(Team_List.keys())[i]][0] for i in range(n_t)]


        for i in range (0 ,len(data_Live_New_Way) ):
            data_Live_New_Way[ i ]['Equipe'] = list(Team_List.keys())[i]

                
        
        if os.path.isfile(os.path.join(local_path, "Turn_Counter.txt")):
            print('The file was already there')
            f1 = open(os.path.join(local_path, "Turn_Counter.txt"), "r")
            f2 = open(os.path.join(local_path, "Flechette_Compteur.txt"), "r")
            Turn = int(f1.read())
            Dart_number = int(f2.read())

            

            Score_History = np.load(os.path.join(local_path, 'Partie_Live.npy'),allow_pickle=True)
            Score_History = Score_History.tolist()

            data_Historique = np.load(os.path.join(local_path, 'Partie_Historique.npy'),allow_pickle=True)
            data_Historique = data_Historique.tolist()

            data_Table = np.load(os.path.join(local_path, 'Score.npy'),allow_pickle=True)
            data_Table = data_Table.tolist()

            Y_Live = np.load(os.path.join(local_path, 'Graph_Partie.npy'), allow_pickle=True)
            Y_Live = Y_Live.tolist()

            Stat_Live = np.load(os.path.join(local_path, 'Stats_Partie.npy'), allow_pickle=True)
            Stat_Live = Stat_Live.tolist()


            
        else:
            print('the file needs to be created')
            Turn = 0
            Dart_Number = 0
            Score_History= []
            f1 = open(os.path.join(local_path, "Turn_Counter.txt"), "x")
            f1.write(str(Turn))
            f1.close()

            f2 = open(os.path.join(local_path, "Flechette_Compteur.txt"), "x")
            f2.write(str(Dart_Number))
            f2.close()
            
            np.save(os.path.join(local_path, 'Partie_Live.npy'),Score_History)
            np.save(os.path.join(local_path, 'Partie_Historique.npy'),data_Historique)
            np.save(os.path.join(local_path, 'Score.npy'),data_Table)
            np.save(os.path.join(local_path, 'Graph_Partie.npy'),Y_Live_Stats)
            np.save(os.path.join(local_path, 'Stats_Partie.npy'),Stat_Live)

        
        if n_clicks_Refresh == 1: # You clicked the refresh button

            n_clicks_Refresh = 0
            
            
            
            
            f1 = open(os.path.join(local_path, "Turn_Counter.txt"), "r")
            f2 = open(os.path.join(local_path, "Flechette_Compteur.txt"), "r")
            Turn = int(f1.read())
            Dart_number = int(f2.read())

            Score_History = np.load(os.path.join(local_path, 'Partie_Live.npy'),allow_pickle=True)
            Score_History = Score_History.tolist()

            data_Table = np.load(os.path.join(local_path, 'Score.npy'),allow_pickle=True)
            data_Table = data_Table.tolist()

            Y_Live = np.load(os.path.join(local_path, 'Graph_Partie.npy'),allow_pickle=True)
            Y_Live = Y_Live.tolist()

            Stat_Live= np.load(os.path.join(local_path, 'Stats_Partie.npy'),allow_pickle=True)
            Stat_Live = Stat_Live.tolist()

            data_Historique = np.load(os.path.join(local_path, 'Partie_Historique.npy'),allow_pickle=True)
            data_Historique = data_Historique.tolist()


            
        



     #   else : # This means the game has already started and we want to extract data from the files



        Team_Number_Game = len( list(Team_List.keys()))
        Turn_Number = int( Turn / Team_Number_Game ) + 1
        Team_Turn = Turn % Team_Number_Game    
        Next_Player = (Turn + 1) % Team_Number_Game

        data_Live_New_Way = Update_Live_Player(data_Live_New_Way,Turn, Team_Number_Game , Team_List)


        




        
        if clickData is not None: # We enter here as soon as you click on the dart board
            #
            # print(data_Live_New_Way)
            
            if n_clicks_Cancel == 0 and n_clicks_Submit == 0 and n_clicks_precedent == 0 :# We have not pressed cancel nor submit. We are therfore filling in the livetable
                
                clickData, Dart_Number, data_Live_New_Way = Get_Click_Data(clickData,df_darts,Dart_Number,data_Live_New_Way, Team_Turn, Darts_Total)
                    
                    
        if n_clicks_Cancel != 0 and n_clicks_Submit == 0 and n_clicks_precedent == 0 : # the cancel button has been pressed

            Dart_Number = 0 # reinitializing n_clicks and the dart number
            n_clicks_Cancel = 0
            
            data_Live_New_Way = Cancel_Button(data_Live_New_Way,Team_Turn)
                
                
                
        elif n_clicks_Submit != 0 and n_clicks_precedent == 0:  # The submit button has been pressed
            
            Dart_Number = 0 # reinitialize the dart number
            n_clicks_Submit = 0 # reinitializing n_clicks
                            
        #  Dart_Number, data_Table, data_Live_New_Way, Score_History = Submit_Turn(Turn, data_Live_New_Way, data_Table, Player_Turn, Next_Player, Player_Number_Game,Dart_Number, Score_History)
        
            Darts, Coef , data_Live_New_Way, Dart_Number = Submit_Turn(data_Live_New_Way, Team_Turn, Next_Player, Dart_Number)

            if Game == Cricket:
                data_Table, Score_History = Score_Update_Cricket(Darts, Coef,  int(Turn/Team_Number_Game), data_Table, Team_Turn, Team_Number_Game,Dart_Number,Score_History, Cricket_Type)

            elif Game == Douze:
                data_Table, Score_History = Score_Update_Douze(Darts, Coef, int(Turn/Team_Number_Game), data_Table, Team_Turn, Team_Number_Game,Dart_Number,Score_History, Douze)

            
            for i in range(0, Darts_Total):
                data_Historique.append( {Column_Storage[j]:Score_History[-3+i][j] for j in range (0,len(Column_Storage))})
                data_Historique[-1][Column_Storage[5]] = np.sum(Score_History[-3+i][5])  
        #     data_Historique[-1][Column_Storage[0]] = Team_List[Score_History[-3+i][0]]  
                data_Historique[-1][Column_Storage[0]] = list(Team_List.keys())[Score_History[-3+i][0]]  


            #print(fig_Stat_Live)

    #        Stat_Live, fig_Stat_Live, Y_Live = Update_Live_Stats(Darts_Total,Score_History,Player_Turn, Player_List,Stat_Live, Turn,fig_Stat_Live, Dropdown_Value, Y_Live, Column_Live_Stats_Graph)
            Stat_Live, Y_Live= Update_Live_Stats(Darts_Total,Score_History,Team_Turn, list(Team_List.keys()),Stat_Live, Turn, Y_Live)



            
            Turn = Turn + 1 # change index for next player
            Turn_Number = int( Turn / Team_Number_Game ) + 1


            data_Live_New_Way = Update_Live_Player(data_Live_New_Way,Turn, Team_Number_Game , Team_List)

            Save_Everyone(local_path,Turn,Score_History,data_Historique,data_Table,Y_Live,Stat_Live)




                            
            
                
        
        
        
        elif n_clicks_Submit == 0 and n_clicks_precedent == 1:  # The come back a player button has been pressed
                
            n_clicks_precedent = 0
                
            if Turn == 0: # if it is pressed right at the beginning
                pass
            else:
                Player_Precedent = (Turn - 1) % Team_Number_Game
        
                Turn = Turn - 1 # think about this, maybe not true?

                data_Table, Score_History, data_Historique, Stat_Live, fig_Stat_Live, Y_Live = Remove_Last_Round_New(Team_Number_Game, data_Table, Score_History, Darts_Total, Player_Precedent,Game,Turn,data_Historique, Stat_Live, fig_Stat_Live, Y_Live)
                
            
            Save_Everyone(local_path,Turn,Score_History,data_Historique,data_Table,Y_Live,Stat_Live)
            
        
        
        # Game ending criteria. Saves all the data.   
        
        Score_min = min( data_Table[i]['Score'] for i in range (0,Team_Number_Game) )  

        if (data_Table[Team_Turn]['Bull'] == 3) and (data_Table[Team_Turn]['20'] == 3) and (data_Table[Team_Turn]['19'] == 3) and (data_Table[Team_Turn]['18'] == 3) and (data_Table[Team_Turn]['17'] == 3) and (data_Table[Team_Turn]['16'] == 3) and (data_Table[Team_Turn]['15'] == 3)  and   (data_Table[Team_Turn]['Score'] == Score_min): # end game criteria    
            


            Deroulement_de_Partie = pd.DataFrame(Score_History)
            Deroulement_de_Partie.to_csv('Partie.csv')  # sauvegarde le derouler de partie
            
            Player_Game_Info= [[] for i in range (0,len(list(Team_List.keys())))]
            
            for i in range(0, len(Score_History)):
                
                Player_Game_Info[int(i/Darts_Total)%len(list(Team_List.keys()))].append(Score_History[i])

                    
            for i in range(0, len(Team_List)):   
                #print('Score_History:')
                #print(Score_History[i]) 
                # print('Historic_Joueur:')
                Historic_Joueur = pd.read_csv('ressources/Player_Info/{}.csv'.format(list(Team_List.keys())[i]))
                #print(Historic_Joueur)
                Partie_Joueur = Player_Game_Info[i]
                #print('Player_Game_Info')
                #print(Player_Game_Info[i])
                
                
                Partie_Joueur = pd.DataFrame(Partie_Joueur,columns = Column_Storage)
                print('Partie_Joueur')
                print(Partie_Joueur)
                
                Partie_Joueur.to_csv('{}.csv'.format(list(Team_List.keys())[i]),index = False)
                
                
        Affichage = ['Tour numéro: {}'.format(Turn_Number) ]  

        # Save info to files

  #      f1 = open(os.path.join(local_path, "Turn_Counter.txt"), "w")
  #      f1.write(str(Turn))
  #      f1.close()

        f2 = open(os.path.join(local_path, "Flechette_Compteur.txt"), "w")
        f2.write(str(Dart_Number))
        f2.close()

        
        return   Dart_Number, n_clicks_Cancel, data_Table, n_clicks_Submit, clickData, n_clicks_precedent, Affichage, data_Live_New_Way, Stat_Live, data_Historique, n_clicks_Refresh#, fig_Stat_Live, Y_Live #Stat_Graph_Live
                

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

    )

    def Update_Graphs(n_click_Graph,Dropdown_Value,Stat_Live,fig_Stat_Live):

        if n_click_Graph != 0:
            
            n_click_Graph = 0
            f1 = open(os.path.join(local_path, "Turn_Counter.txt"), "r")
            Turn = int(f1.read())

            Score_History = np.load(os.path.join(local_path, 'Partie_Live.npy'),allow_pickle=True)
            Score_History = Score_History.tolist()

            Y_Live = np.load(os.path.join(local_path, 'Graph_Partie.npy'), allow_pickle=True)
            Y_Live = Y_Live.tolist()

            Team_Number_Game = len(list(Team_List.keys()))
            Team_Turn = Turn % Team_Number_Game          

            fig_Stat_Live = Update_Live_Graph(Stat_Live,Team_Turn,list(Team_List.keys()), Y_Live,fig_Stat_Live, Dropdown_Value, Column_Live_Stats_Graph,Score_History)


        return fig_Stat_Live, n_click_Graph


    return app, layout

        


 
        

if __name__ == '__main__':
    app.run_server(debug = True, port = 8000)