import dash_html_components as html

import os

import pandas as pd
import numpy as np

### Function that creates the color scale in the score table

def discrete_background_color_bins(df, n_bins , columns ):


#    import colorlover
    bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
    if columns == 'all':
    
        
       # if columns != 'Score':
        
        if 'id' in df:
            df_numeric_columns = df.select_dtypes('number').drop(['id'], axis=1)
        else:
            df_numeric_columns = df.select_dtypes('number')
    else:
        df_numeric_columns = df[columns]
    df_max = 3
    df_min = 0
    ranges = [
        ((df_max - df_min) * i) + df_min
        for i in bounds
    ]
    styles = []
    legend = []
    for i in range(1, len(bounds)):
        min_bound = ranges[i - 1]
        max_bound = ranges[i]
   #     backgroundColor = colorlover.scales[str(n_bins)]['seq']['Blues'][i - 1]
        color = 'white' if i > len(bounds) / 2. else 'inherit'

        
        if i ==1:
            backgroundColor = 'white'
            
        if i == 2: 
            backgroundColor = 'rgb(158,202,225)'
            
        if i== 3:
            backgroundColor = 'rgb(49,130,189)'
            
        if i == 4:
            backgroundColor = 'rgb(50, 50, 50)'
            


        for column in df_numeric_columns:
            styles.append({
                'if': {
                    'filter_query': (
                        '{{{column}}} >= {min_bound}' +
                        (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
                    ).format(column=column, min_bound=min_bound, max_bound=max_bound),
                    'column_id': column
                },
                'backgroundColor': backgroundColor,
                'color': color
            })
        legend.append(
            html.Div(style={'display': 'inline-block', 'width': '60px'}, children=[
                html.Div(
                    style={
                        'backgroundColor': backgroundColor,
                        'borderLeft': '1px rgb(50, 50, 50) solid',
                        'height': '10px'
                    }
                ),
                html.Small(round(min_bound, 2), style={'paddingLeft': '2px'})
            ])
        )

    return (styles, html.Div(legend, style={'padding': '5px 0 5px 0'}))


def Storage_Player_Separation (data_Historique): #,data_Historique,Player_Number_Game):

    style_data_conditional=[
        {
            'if': {
                'filter_query': '{Flèche numéro} = 1',
            },
            'backgroundColor': 'RebeccaPurple',
            'color': 'white'
        },
    ]

    return style_data_conditional

#    if Turn_Counter % Darts_Total == 0 :

 #       New_Turn = {
   #         'if': {'row_index': Turn_Counter},
  #          'backgroundColor': 'RebeccaPurple',
    #        'color': 'white'     
     #   }

      #  Player_Separation.append([])
       # Player_Separation[-1] = New_Turn

#    return Player_Separation

def Which_Line (Turn_Counter_Index, data_Live_New_Way, Dart_Number):

    Player_Line = [{
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(248, 248, 248)'
            },
            {
            'if': {'row_index': Turn_Counter_Index},
             'backgroundColor': 'rgb(250, 200, 250)',
            'fontWeight': 'bold'
            },
            {
            'if': {'column_id' : list(data_Live_New_Way[Turn_Counter_Index])[2*Dart_Number + 1],
                   'row_index': Turn_Counter_Index},
            'backgroundColor': 'RebeccaPurple',
            'color': 'white'
                    },
            {
            'if': {'column_id' : list(data_Live_New_Way[Turn_Counter_Index])[2*Dart_Number + 2],
                   'row_index': Turn_Counter_Index},
            'backgroundColor': 'RebeccaPurple',
            'color': 'white'
                    }]
    
    return Player_Line


def Douze_Turn(Game,Turn) :
    Number_Open_Close = [{
                'if': {'column_id' : Game[Turn] },
                'backgroundColor': 'rgb(85, 85, 85)', # gris
                'color': 'white'
                } ]
    
    return Number_Open_Close




def Open_Or_Closed (Game,Team_Number_Game,data_Table,Turn_Counter_Index):


    


    Number_Open_Close = [None,None ,None ,None ,None ,None ,None  ] # doesn't do anything for the total Score    

    for j in range (0, len(Number_Open_Close) ):       
    
    
        Compteur_Fermer = 0
    
        
        for i in range (0, Team_Number_Game):       
            if data_Table[i][Game[j]] == 3:           
                Compteur_Fermer = Compteur_Fermer + 1           
        
        if Compteur_Fermer == Team_Number_Game: # Tout le monde a fermer
            Number_Open_Close[j] = {
                'if': {'column_id' : Game[j] },
                'backgroundColor': 'rgb(85, 85, 85)', # gris
                'color': 'white'
                }
                     
            
            
        elif Compteur_Fermer == 0 : # Personne n'a fermé
            Number_Open_Close[j] = {
                    'if': {'column_id' : Game[j] },
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'                        }
                               
        else: # au moins une personne a fermé           
            if data_Table[Turn_Counter_Index][Game[j]] == 3: # celui qui est en train de jouer a fermé, il peut donc marquer des points 
                      
                Number_Open_Close[j] = {
                        'if': {'column_id' : Game[j] },
                        'backgroundColor': 'rgb(12, 124, 27)', # vert
                        'color': 'white'
                        }
              
                                        
            else: # celui qui est en train de jouer n'a pas fermé, il peut donc se prendre des points.       
                Number_Open_Close[j] = {
                        'if': {'column_id' : Game[j] }, 
                        'backgroundColor': 'rgb(232, 45, 82)', # rouge
                        'color': 'white'
                         }

    return Number_Open_Close


def Tables_Up_to_Date(Team_List,Score_Live,Score_Init, Game):
        
    data_Live_New_Way = pd.DataFrame(np.array([Score_Live for i in range (0, len(Team_List))]), columns=['Fleche 1','Coef 1', 'Fleche 2','Coef 2', 'Fleche 3','Coef 3'], index= Player_List)
    data_Live_New_Way = data_Live_New_Way.reset_index()
    data_Live_New_Way = data_Live_New_Way.to_dict('records')
        
        
    data_Table = pd.DataFrame(np.array([Score_Init for i in range (0, len(Team_List))]), columns=Game, index= Team_List)         
    data_Table = data_Table.reset_index()
    data_Table = data_Table.to_dict('records')

    return (data_Live_New_Way, data_Table)


def Cancel_Button(data_Live_New_Way,Team_Turn):

        
    data_Live_New_Way[Team_Turn]['Fleche 1'] = None
    data_Live_New_Way[Team_Turn]['Fleche 2'] = None
    data_Live_New_Way[Team_Turn]['Fleche 3'] = None
    data_Live_New_Way[Team_Turn]['Coef 1'] = None
    data_Live_New_Way[Team_Turn]['Coef 2'] = None
    data_Live_New_Way[Team_Turn]['Coef 3'] = None
    
    return data_Live_New_Way


def Submit_Turn(data_Live_New_Way, Team_Turn, Next_Player, Dart_Number) :

    if data_Live_New_Way[Team_Turn]['Fleche 1'] is not None:
        
        coef1 = data_Live_New_Way[Team_Turn]['Coef 1']  # Save the shots 
        Dart1 = data_Live_New_Way[Team_Turn]['Fleche 1'] 
    else: # submitted with no entry
        coef1 = 1
        Dart1 = 0            
        
        
    if data_Live_New_Way[Team_Turn]['Fleche 2'] is not None:
    
        coef2 = data_Live_New_Way[Team_Turn]['Coef 2'] 
        Dart2 = data_Live_New_Way[Team_Turn]['Fleche 2'] 
    else: # submitted with no entry
        coef2 = 1
        Dart2 = 0 
        Dart_Number = 0
    
            
    if data_Live_New_Way[Team_Turn]['Fleche 3'] is not None:
    
        coef3 = data_Live_New_Way[Team_Turn]['Coef 3'] 
        Dart3 = data_Live_New_Way[Team_Turn]['Fleche 3'] 
    else: # submitted with no entry
        coef3 = 1
        Dart3 = 0 
        Dart_Number = 0
                
                
    Darts = [Dart1, Dart2, Dart3]
    Coef = [coef1,coef2,coef3]

    data_Live_New_Way[Next_Player]['Fleche 1'] = None # Erase the shots of the next player
    data_Live_New_Way[Next_Player]['Fleche 2'] = None 
    data_Live_New_Way[Next_Player]['Fleche 3'] = None
    data_Live_New_Way[Next_Player]['Coef 1'] = None
    data_Live_New_Way[Next_Player]['Coef 2'] = None
    data_Live_New_Way[Next_Player]['Coef 3'] = None
        


    return Darts, Coef , data_Live_New_Way, Dart_Number


def Score_Update_Cricket(Darts, Coef, Turn, data_Table, Team_Turn, Team_Number_Game,Dart_Number,Score_History, Cricket_Type):

    Degats = [[0 for j in range (0,Team_Number_Game)] for i in range(0,len(Darts))]

    Fleche_qui_Ferme = [0,0,0]
            
    for j in range (0, len(Darts) ): # for each dart, fill in the score table
                
        if ( Darts[j] >= 15 ):
            value = Darts[j]
            coef = Coef[j]        
            if value == 25 :
                value_string = 'Bull'        
            else : 
                value_string = str(int(value))        
            
            if data_Table[Team_Turn][value_string] + coef <= 3 : # Si celui qui joue ne ferme pas le chiffre qu'il a touché 
                data_Table[Team_Turn][value_string] = data_Table[Team_Turn][value_string] + coef
                Fleche_qui_Ferme[j] = coef
        
            elif data_Table[Team_Turn][value_string] == 3 : # si celui qui joue avait deja fermé
                
                if Cricket_Type == 'Cut_Throat':
                
                    for i in range (0, Team_Number_Game):
                    
                    
                        if i == Team_Turn:
                            continue
                        
                        if data_Table[i][value_string] < 3 : # mets des points à ceux qui n'ont pas fermé
                            data_Table[i]['Score'] = data_Table[i]['Score'] + value * coef
                            Degats[j][i] = value * coef

                else:
                    Checking_Other_Scores = 0
                    for i in range (0, Team_Number_Game):

                        if i == Team_Turn : 
                            continue

                        if data_Table[i][value_string] < 3 :
                                 
                            Checking_Other_Scores = 1
                    
                    if Checking_Other_Scores == 1:
                        data_Table[Team_Turn]['Score'] = data_Table[Team_Turn]['Score'] + value * coef
                        Degats[j][Team_Turn] = value * coef

                    
            elif data_Table[Team_Turn][value_string] + coef >= 3: # Si celui qui joue ferme ce chiffre pendant ce tour            
                
                if Cricket_Type == 'Cut_Throat':
                    
                    for i in range (0, Team_Number_Game):

                        if i == Team_Turn:
                            continue
                                
                        if data_Table[i][value_string] < 3:
                            data_Table[i]['Score'] = data_Table[i]['Score'] + value * ( data_Table[Team_Turn][value_string] + coef - 3 )
                            Degats[j][i] = value * ( data_Table[Team_Turn][value_string] + coef - 3 )
                        
                        Fleche_qui_Ferme[j] = 3 - data_Table[Team_Turn][value_string] # je crois tous les fleches qui ferme ne doivent pas etre dans le if!

                else: 
                    Checking_Other_Scores = 0
                    for i in range (0, Team_Number_Game):

                        if i == Team_Turn : 
                            continue

                        if data_Table[i][value_string] < 3 :
                                 
                            Checking_Other_Scores = 1
                    
                    if Checking_Other_Scores == 1:
                
                        data_Table[Team_Turn]['Score'] = data_Table[Team_Turn]['Score'] + value * ( data_Table[Team_Turn][value_string] + coef - 3 )
                        Degats[j][Team_Turn] = value * ( data_Table[Team_Turn][value_string] + coef - 3 )
                        
                        Fleche_qui_Ferme[j] = 3 - data_Table[Team_Turn][value_string]

                data_Table[Team_Turn][value_string] = 3  # (Needs to be after the for loop!)
            
      #  print('Degats:')
      #  print(Degats[j])

        Score_History.append([Team_Turn, Turn+1, j+1, Darts[j],Coef[j],Degats[j], Fleche_qui_Ferme[j]]) # sauvegarde info fleche i


    return data_Table, Score_History


def Score_Update_Douze(Darts, Coef, Turn_Counter_Index, data_Table, Team_Turn, Team_Number_Game,Dart_Number,Score_History, Douze):

    Degats =  [[0 for i  in range(0,Team_Number_Game)] for j in range (0,len(Darts)) ]

    Fleche_qui_Ferme = [0,0,0]

    Factor = 0.51 # stay at 0.5 if you don t hit

    if (Turn_Counter_Index % 4 == 3) :
        if Douze[Turn_Counter_Index] == 'Double':
            for j in range (0, len(Darts) ): # for each dart, fill in the score table
                if (Coef[j]==2):
                    Factor = 1
                    data_Table[Team_Turn][Douze[Turn_Counter_Index]] = data_Table[Team_Turn][Douze[Turn_Counter_Index]] + Coef[j]
                    Degats[j][Team_Turn] =  Degats[j][Team_Turn] + Darts[j] * Coef[j]
                    Fleche_qui_Ferme[j] = data_Table[Team_Turn][Douze[Turn_Counter_Index]]

        if Douze[Turn_Counter_Index] == 'Triple':
            for j in range (0, len(Darts) ): # for each dart, fill in the score table
                if (Coef[j]==3):
                    Factor = 1
                    data_Table[Team_Turn][Douze[Turn_Counter_Index]] = data_Table[Team_Turn][Douze[Turn_Counter_Index]] + Coef[j]
                    Degats[j][Team_Turn] =  Degats[j][Team_Turn] + Darts[j] * Coef[j]
                    Fleche_qui_Ferme[j] = data_Table[Team_Turn][Douze[Turn_Counter_Index]]
                    
        
        if Douze[Turn_Counter_Index] == 'Bull':
            for j in range (0, len(Darts) ): # for each dart, fill in the score table
                if (Darts[j]==25):
                    Factor = 1
                    data_Table[Team_Turn][Douze[Turn_Counter_Index]] = data_Table[Team_Turn][Douze[Turn_Counter_Index]] + Coef[j]
                    Degats[j][Team_Turn] =  Degats[j][Team_Turn] + Darts[j] * Coef[j]
                    Fleche_qui_Ferme[j] = data_Table[Team_Turn][Douze[Turn_Counter_Index]]



        
    else:
            
        for j in range (0, len(Darts) ): # for each dart, fill in the score table
            
            if ( Darts[j] == int(Douze[Turn_Counter_Index]) ):
                Factor = 1
                data_Table[Team_Turn][Douze[Turn_Counter_Index]] = data_Table[Team_Turn][Douze[Turn_Counter_Index]] + Coef[j]
                Degats[j][Team_Turn] =  Degats[j][Team_Turn] + Darts[j] * Coef[j]
                Fleche_qui_Ferme[j] = Coef[j]

        
   # print('Fleche qui ferme : ')
   # print(Fleche_qui_Ferme)

    data_Table[Team_Turn]['Score'] = round(Factor * data_Table[Team_Turn]['Score'] + Degats[0][Team_Turn]+ Degats[1][Team_Turn]+ Degats[2][Team_Turn])

    for j in range (0, len(Darts) ): # save each dart

        Score_History.append([Team_Turn,Turn_Counter_Index + 1, j+1, Darts[j],Coef[j],Degats[j], Fleche_qui_Ferme[j]]) # sauvegarde info fleche i
 
   # print(Score_History)

    return data_Table, Score_History



def Remove_Last_Round(Player_Number_Game, data_Table, Score_History, Darts_Total, Player_Precedent):
     # enlever les eventuels degats infliger par les 3 dernieres flechettes.
    for i in range (0, Player_Number_Game):
        data_Table[i]['Score'] = data_Table[i]['Score'] - Score_History[-1][5][i] # degats de la 3eme fleche du joueur precedent infligés à chaque joueur
        data_Table[i]['Score'] = data_Table[i]['Score'] - Score_History[-2][5][i] # degats de la 2eme fleche du joueur precedent infligés à chaque joueur
        data_Table[i]['Score'] = data_Table[i]['Score'] - Score_History[-3][5][i] # degats de la 1ere fleche du joueur precedent infligés à chaque joueur
                    
                
    # enlever les touches obtenus par le joueur precedent sur ses 3 dernieres flechettes.
    for i in range (0, Darts_Total ):
        if Score_History[-i-1][3] >= 15:
                        
            if Score_History[-i-1][3] == 25 :
                value_Precedent_Dart_string = 'Bull'        
            else : 
                value_Precedent_Dart_string = str(int(Score_History[-i-1][3])) 
                        
            data_Table[Player_Precedent][value_Precedent_Dart_string] = data_Table[Player_Precedent][value_Precedent_Dart_string] - Score_History[-i-1][6]
                
                
                
    # remove the last 3 darts from the storage file and the last 3 darts of the historic display
                
    del(Score_History[-1]) 
    del(Score_History[-1])
    del(Score_History[-1])
    

    return data_Table, Score_History


def Remove_Last_Round_New(Player_Number_Game, data_Table, Score_History, Darts_Total, Player_Precedent,Game,Turn_Counter,data_Historique, Stat_Live, fig_Stat_Live,Y_Live):
    # enlever les contributions au score
    
     # enlever les eventuels degats infliger par les 3 dernieres flechettes.
    for i in range (0, Player_Number_Game):
        data_Table[i]['Score'] = data_Table[i]['Score'] - Score_History[-1][5][i] # degats de la 3eme fleche du joueur precedent infligés à chaque joueur
        data_Table[i]['Score'] = data_Table[i]['Score'] - Score_History[-2][5][i] # degats de la 2eme fleche du joueur precedent infligés à chaque joueur
        data_Table[i]['Score'] = data_Table[i]['Score'] - Score_History[-3][5][i] # degats de la 1ere fleche du joueur precedent infligés à chaque joueur      
                
    # enlever les touches obtenus par le joueur precedent sur ses 3 dernieres flechettes.
    for i in range (0, Darts_Total ):
        if Score_History[-i-1][6] > 0:
                        
            if Score_History[-i-1][3] == 25 :
                value_Precedent_Dart_string = 'Bull'  
            elif Game[Turn_Counter] == 'Double' :
                value_Precedent_Dart_string = 'Double'
            elif Game[Turn_Counter] == 'Triple':
                value_Precedent_Dart_string = 'Triple'      
            else : 
                value_Precedent_Dart_string = str(int(Score_History[-i-1][3])) 
                        
            data_Table[Player_Precedent][value_Precedent_Dart_string] = data_Table[Player_Precedent][value_Precedent_Dart_string] - Score_History[-i-1][6]
                
    if Game == ['12', '13', '14','Double','15','16','17','Triple','18', '19', '20', 'Bull', 'Score'] and  Score_History[-0-1][6] == 0  and  Score_History[-1-1][6] == 0 and  Score_History[-2-1][6] == 0   :     
    
        data_Table[Player_Precedent]['Score'] = data_Table[Player_Precedent]['Score'] * 2


#enlever les contributions au stats


    fig_Stat_Live['data'][Player_Precedent]['x'].pop(-1) 
    fig_Stat_Live['data'][Player_Precedent]['y'].pop(-1)

    Y_Live.pop(-1)

    print('Turn :', Turn_Counter)
    print('Y_Live:', Y_Live)

    if Turn_Counter == 0:
        Stat_Live[Player_Precedent]['Tour'] = 0
        Stat_Live[Player_Precedent]['# Touche/ Tour'] = 0
        Stat_Live[Player_Precedent]['# de triple'] = 0
        Stat_Live[Player_Precedent]['# de double'] = 0
        Stat_Live[Player_Precedent]['# de tour à vide'] = 0
        Stat_Live[Player_Precedent]['Longest streak'] = 0
    else:
        Stat_Live[Player_Precedent]['Tour'] = Y_Live[-2][5]
        Stat_Live[Player_Precedent]['# Touche/ Tour'] = Y_Live[-2][0]
        Stat_Live[Player_Precedent]['# de triple'] = Y_Live[-2][1]
        Stat_Live[Player_Precedent]['# de double'] = Y_Live[-2][2]
        Stat_Live[Player_Precedent]['# de tour à vide'] = Y_Live[-2][3]
        Stat_Live[Player_Precedent]['Longest streak'] = Y_Live[-2][4]


    





#    Stat_Live[Player_Precedent]['Tour'] = fig_Stat_Live['data'][Player_Precedent]['x'][-1]
#    Stat_Live[Player_Precedent]['# Touche/ Tour'] = fig_Stat_Live['data'][Player_Precedent]['y'][-1]




    # remove the last 3 darts from the storage file and the last 3 darts of the historic display
                
    del(Score_History[-1]) 
    del(Score_History[-1])
    del(Score_History[-1])

    del(data_Historique[-1])
    del(data_Historique[-1])
    del(data_Historique[-1])

    return data_Table, Score_History, data_Historique, Stat_Live, fig_Stat_Live, Y_Live

def Get_Click_Data(clickData,df_darts,Dart_Number,data_Live_New_Way, Player_Turn, Darts_Total) :
    click_Location = clickData['points'][0]['location']
    touched_polygon = df_darts.loc[df_darts["id"] == click_Location].index[0]
    value = df_darts.loc[touched_polygon, 'value']
    coef  = df_darts.loc[touched_polygon, 'coef']
            
    clickData = None   # To be able to click at the same place
            
            
    if Dart_Number == 0: # Entering the score of the 1st dart
 
        data_Live_New_Way[Player_Turn]['Fleche 1'] = value 
        data_Live_New_Way[Player_Turn]['Coef 1']= coef
                    
    if Dart_Number == 1: # Entering the score of the 2nd dart
                                       
        data_Live_New_Way[Player_Turn]['Fleche 2'] = value 
        data_Live_New_Way[Player_Turn]['Coef 2'] = coef
                    
    if Dart_Number == 2: # Entering the score of the 3rd dart
                                        
        data_Live_New_Way[Player_Turn]['Fleche 3'] = value 
        data_Live_New_Way[Player_Turn]['Coef 3'] = coef
        Dart_Number = 1 # (so that the highlight changes once you validate)
                    
    Dart_Number = (Dart_Number + 1) % Darts_Total

    return clickData, Dart_Number, data_Live_New_Way


def Update_Live_Stats(Darts_Total,Score_History,Player_Turn,Team_List, Stat_Live, Turn, Y_Live):#,fig_Stat_Live,Dropdown_Value,Y_Live,Column_Live_Stats_Graph):
    Dernier_Tour = []
    Player_Number_Game = len(Team_List)
    Turn_Number = int(Turn / Player_Number_Game) + 1

    for i in range(0, Darts_Total):
        Dernier_Tour.append(Score_History[-i-1] )
        


    Touche_Total = 0

    if (Dernier_Tour[0][6] + Dernier_Tour[1][6] + Dernier_Tour[2][6] == 0) and (np.sum(Dernier_Tour[0][5]) + np.sum(Dernier_Tour[1][5]) + np.sum(Dernier_Tour[2][5]) == 0 ):
        Stat_Live[Player_Turn]['# de tour à vide'] = Stat_Live[Player_Turn]['# de tour à vide'] + 1
            

    else:
        for i in range(0, Darts_Total):
                
            if ( Dernier_Tour[i][6] != 0 ) or ( np.sum(Dernier_Tour[i][5]) != 0 ):

                if Dernier_Tour[i][4] == 3:
                    Stat_Live[Player_Turn]['# de triple'] = Stat_Live[Player_Turn]['# de triple'] + 1
                elif Dernier_Tour[i][4] == 2:
                    Stat_Live[Player_Turn]['# de double'] = Stat_Live[Player_Turn]['# de double'] + 1

                Touche_Total = Touche_Total + Dernier_Tour[i][6] + np.sum(Dernier_Tour[i][5]) / Dernier_Tour[i][3]

    Stat_Live[Player_Turn]['# Touche/ Tour'] = ( Stat_Live[Player_Turn]['# Touche/ Tour'] * ( Dernier_Tour[0][1] -1) + Touche_Total ) / (Dernier_Tour[0][1])
    Stat_Live[Player_Turn]['Tour'] = Turn_Number

    
    New_Stats = [Stat_Live[Player_Turn][i] for i in Stat_Live[Player_Turn]]
   # print('New_Stats =', New_Stats)

  #  New_Stats.remove(New_Stats[0])
    Y_Live.append(New_Stats)
   # print('Y_live =', Y_Live)


    


############    fig_Stat_Live['data'][0]['hovertemplate'] = 'color=A<br>Tour=%{x}<br># Touche/ Tour=%{y}<extra></extra>'




    return Stat_Live, Y_Live



def Update_Live_Graph(Stat_Live,Player_Turn,Team_List, Y_Live,fig_Stat_Live, Dropdown_Value, Column_Live_Stats_Graph,Score_History):

    Player_Number_Game = len(Team_List)


    print('Updating graph')
    print('Stat_Live', Stat_Live[Player_Turn])
    X = [[] for i in range (0, Player_Number_Game)]
    Y = [[] for i in range (0, Player_Number_Game)]

    for j in range (0, len(Y_Live)):

 #       if Y_Live[j][5] == 0:
  #          Y_Live.remove(Y_Live[j])
   #         continue
#   ###         Y[i].remove(Y[i][0])

        print('Y_Live =', Y_Live)
        X[(j+1) % Player_Number_Game].append(Y_Live[j][5])
        Y[(j+1) % Player_Number_Game].append(Y_Live[j][Dropdown_Value])

        
    for i in range (0, Player_Number_Game):
        if X[i][0] == '0':
            X[i].remove(X[i][0])
            Y[i].remove(Y[i][0])


        print('Player:', Team_List[i])
        fig_Stat_Live['data'][i]['x'] = X[i]
        fig_Stat_Live['data'][i]['y'] = Y[i]
    

#    print(fig_Stat_Live)
   # print('Y_Live =', Y_Live)
    X_Max =   float(max(max( x) for x in X ))
    Y_Max =   float(max(max( x) for x in Y ))
    fig_Stat_Live['layout']['yaxis']['title']['text'] = Column_Live_Stats_Graph[Dropdown_Value]
    fig_Stat_Live['layout']['xaxis']['domain'] = [0.0, X_Max + 1]
    
    fig_Stat_Live['layout']['yaxis']['domain'] = [0.0, Y_Max + 0.5]     
 #   print('X:', X)
 #   print('Y:', Y)

    for i in range (0, Player_Number_Game):
        fig_Stat_Live['data'][i].update(mode='markers+lines', hovertemplate =f'<b>Fleche 1:{Score_History[-3][3]:.0f}</b><br>Fleche 2:{Score_History[-2][3]:.3f} <br>Fleche3:{Score_History[-1][3]:.3f} ')
        #fig_Stat_Live['data'][i].update_traces(mode="markers+lines", hovertemplate=None)

        print('Score History:', Score_History[-1])


    return fig_Stat_Live






def Update_Live_Player(data_Live_New_Way, Turn, Team_Number_Game, Team_List):

    Number_Of_Players = len(Team_List[ list(Team_List.keys())[Turn % Team_Number_Game] ])
    Team_Turn = list(Team_List.keys())[Turn % Team_Number_Game]
  #  Player_Turn = Team_List[Turn % Team_Number_Game][1][ int(Turn / Team_Number_Game) %  Number_Of_Players ]
    Player_Turn = Team_List[Team_Turn][int(Turn / Team_Number_Game) %  Number_Of_Players]
    print(list(Team_List.keys())[Turn % Team_Number_Game])
    print(int(Turn / Team_Number_Game))
    print(Number_Of_Players)
    print(int(Turn / Team_Number_Game) %  Number_Of_Players)
    data_Live_New_Way[Turn % Team_Number_Game ]['index'] = Player_Turn

    return data_Live_New_Way

def Save_Everyone(local_path,Turn,Score_History,data_Historique,data_Table,Y_Live,Stat_Live):

    f1 = open(os.path.join(local_path, "Turn_Counter.txt"), "w")
    f1.write(str(Turn))
    f1.close()
            
    np.save(os.path.join(local_path, 'Partie_Live.npy'),Score_History)
    np.save(os.path.join(local_path, 'Partie_Historique.npy'),data_Historique)
    np.save(os.path.join(local_path, 'Score.npy'),data_Table)
    np.save(os.path.join(local_path, 'Graph_Partie.npy'),Y_Live)
    np.save(os.path.join(local_path, 'Stats_Partie.npy'),Stat_Live)



            