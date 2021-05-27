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
        s_dic = {'backgroundColor': backgroundColor,
                 'borderLeft': '1px rgb(50, 50, 50) solid',
                 'textAlign': 'center',
                 'height': '25px'}

        if min_bound == 2.25:
            s_dic['color'] = 'white'

        legend.append(
            html.Div(style={'display': 'inline-block', 'width': '60px'}, children=[
                html.Div(map_min_bound(min_bound),
                    style=s_dic
                )
            ])
        )

    return (styles, 
            html.Div(legend, 
                     style={'padding': '5px 0px 0px 0px',
                            'margin-left' : "15px"}))


def Storage_Player_Separation(turn): 
    if turn > 1:
        style_data_conditional = [
            {
                'if': {
                    'filter_query': '{Flèche numéro} = 1',
                },
                'backgroundColor': 'RebeccaPurple',
                'color': 'white'
            },
        ]
    else:
        style_data_conditional = [
                
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgb(248, 248, 248)'
                                }
        ]
    return style_data_conditional




def Which_Line (Turn_Counter_Index, data_Live_New_Way, Dart_Number):

    Player_Line = [{
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(248, 248, 248)'
            },
            {
            'if': {'row_index': Turn_Counter_Index},
             'backgroundColor': color_mapping[data_Live_New_Way[Turn_Counter_Index]['Equipe']+'Light'],
            'fontWeight': 'bold'
            },
            {
            'if': {'column_id' : list(data_Live_New_Way[Turn_Counter_Index])[2*Dart_Number + 1],
                   'row_index': Turn_Counter_Index},
            'backgroundColor': color_mapping[data_Live_New_Way[Turn_Counter_Index]['Equipe']],
            'color': 'white'
                    },
            {
            'if': {'column_id' : list(data_Live_New_Way[Turn_Counter_Index])[2*Dart_Number + 2],
                   'row_index': Turn_Counter_Index},
            'backgroundColor': color_mapping[data_Live_New_Way[Turn_Counter_Index]['Equipe']],
            'color': 'white'
                    }]
    
    return Player_Line


def Douze_Turn(Game,Turn) :

    if name == "Douze":
        Game = ['12', '13', '14','Double','15','16','17','Triple','18', '19', '20', 'Bull', 'Score']
    Number_Open_Close = [{
                'if': {'column_id' : Game[Turn] },
                'backgroundColor': 'rgb(85, 85, 85)', # gris
                'color': 'white'
                } ]
    
    return Number_Open_Close




def Open_Or_Closed (name, Team_Number_Game,
                    data_Table, Turn_Counter_Index):
    if name == "Cricket":
        Game = ['20', '19', '18', '17', '16', '15', 'Bull']#, 'Score', 'Delta']
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


def Cancel_Button(data_Live_New_Way, Team_Turn):

        
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


def Score_Update_Cricket(Darts, Coef, Turn, data_Table, Team_Turn, Team_Number_Game,Dart_Number,
#                Score_History,
                 Cricket_Type):

    DartRound_Data = []

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
            
        
        ### Calculate the distance in score to the leading score
     
        #Score_min = min(data_Table[i]['Score'] for i in range(Team_Number_Game))
        for i in range(Team_Number_Game):
            data_Table[i]['Delta'] = data_Table[i]['Score'] - data_Table[Team_Turn]['Score']

        DartRound_Data.append([Team_Turn, Turn+1, j+1, Darts[j],Coef[j],Degats[j], Fleche_qui_Ferme[j]]) # sauvegarde info fleche i
        

    return data_Table, DartRound_Data


def Score_Update_Douze(Darts, Coef, Turn_Counter_Index, data_Table, Team_Turn, Team_Number_Game,Dart_Number, Douze):

    DartRound_Data= []

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


    data_Table[Team_Turn]['Score'] = round(Factor * data_Table[Team_Turn]['Score'] + Degats[0][Team_Turn]+ Degats[1][Team_Turn]+ Degats[2][Team_Turn])

    for j in range (0, len(Darts) ): # save each dart

        DartRound_Data.append([Team_Turn,Turn_Counter_Index + 1, j+1, Darts[j],Coef[j],Degats[j], Fleche_qui_Ferme[j]]) # sauvegarde info fleche i
 

    return data_Table, DartRound_Data




def Remove_Last_Round_New(Player_Number_Game, data_Table,
                          Darts_Total,
                          Player_Precedent, Game, Turn_Counter,
                          data_Historique  
                         ):
    # enlever les contributions au score

    
     # enlever les eventuels degats infliger par les 3 dernieres flechettes.
    for i in range (0, Player_Number_Game):
        data_Table[i]['Score'] = data_Table[i]['Score'] - data_Historique[-1]['Dégats'][i] # degats de la 3eme fleche du joueur precedent infligés à chaque joueur
        data_Table[i]['Score'] = data_Table[i]['Score'] - data_Historique[-2]['Dégats'][i] # degats de la 2eme fleche du joueur precedent infligés à chaque joueur
        data_Table[i]['Score'] = data_Table[i]['Score'] - data_Historique[-3]['Dégats'][i] # degats de la 1ere fleche du joueur precedent infligés à chaque joueur      
                
    # enlever les touches obtenus par le joueur precedent sur ses 3 dernieres flechettes.
    for i in range (0, Darts_Total ):
        if data_Historique[-i-1]['Ferme le chiffre'] > 0:
                        
            if data_Historique[-i-1]['Valeur'] == 25 :
                value_Precedent_Dart_string = 'Bull'  
            elif Game[Turn_Counter] == 'Double' :
                value_Precedent_Dart_string = 'Double'
            elif Game[Turn_Counter] == 'Triple':
                value_Precedent_Dart_string = 'Triple'      
            else : 
                value_Precedent_Dart_string = str(int(data_Historique[-i-1]['Valeur'])) 
                        
            data_Table[Player_Precedent][value_Precedent_Dart_string] = data_Table[Player_Precedent][value_Precedent_Dart_string] - data_Historique[-i-1]['Ferme le chiffre']
                
    if Game == ['12', '13', '14','Double','15','16','17','Triple','18', '19', '20', 'Bull', 'Score'] and  data_Historique[-0-1]['Ferme le chiffre'] == 0  and  data_Historique[-1-1]['Ferme le chiffre'] == 0 and  data_Historique[-2-1]['Ferme le chiffre'] == 0   :     
    
        data_Table[Player_Precedent]['Score'] = data_Table[Player_Precedent]['Score'] * 2


    del(data_Historique[-1])
    del(data_Historique[-1])
    del(data_Historique[-1])

    return (data_Table, data_Historique)
  

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

def Get_Stats(data_Historique,Stats_Table,Team_List,Stats_Graph,Dropdown_Value):

 

    X = [ [j+1  for j in range (0, data_Historique[-1]['Tour']  )] for i in range (0,len(list(Team_List.keys()))) ]
    Y = [ [None  for j in range (0, data_Historique[-1]['Tour']  )] for i in range (0,len(list(Team_List.keys()))) ]

    N_Touche = [ [0  for j in range (0, data_Historique[-1]['Tour']  )] for i in range (0,len(list(Team_List.keys()))) ]
    Hover_Data_Fleche1 = [ [0  for j in range (0, data_Historique[-1]['Tour']  )] for i in range (0,len(list(Team_List.keys()))) ]
    Hover_Data_Fleche2 = [ [0  for j in range (0, data_Historique[-1]['Tour']  )] for i in range (0,len(list(Team_List.keys()))) ]
    Hover_Data_Fleche3 = [ [0  for j in range (0, data_Historique[-1]['Tour']  )] for i in range (0,len(list(Team_List.keys()))) ]



    for i in range (0, int( len(data_Historique) / 3) ): # Analysing the 3 darts of the turn in one go

        Player_Turn = list(Team_List.keys()).index(data_Historique[ 3*i ]['Player'])


        if ( (data_Historique[ 3*i + 0 ]['Ferme le chiffre'] 
            + data_Historique[ 3*i + 1 ]['Ferme le chiffre']
            + data_Historique[ 3*i + 2 ]['Ferme le chiffre'] == 0) 
            and
             (np.sum(data_Historique[ 3*i + 0 ]['Dégats']) 
            + np.sum(data_Historique[ 3*i + 1 ]['Dégats'])
            + np.sum(data_Historique[ 3*i + 2 ]['Dégats']) == 0) ): # si tour à vide

            Stats_Table[Player_Turn]['# de tour à vide'] = Stats_Table[Player_Turn]['# de tour à vide'] + 1

        else :
                for j in range (0, 3):
                    
                    if j == 0:
                        Hover_Data_Fleche1[Player_Turn][data_Historique[ 3*i ]['Tour'] - 1 ] = data_Historique[ 3*i + j ]['Valeur']
                    elif j ==1:
                        Hover_Data_Fleche2[Player_Turn][data_Historique[ 3*i ]['Tour'] - 1 ] = data_Historique[ 3*i + j ]['Valeur']
                    elif j ==2:
                        Hover_Data_Fleche3[Player_Turn][data_Historique[ 3*i ]['Tour'] - 1 ] = data_Historique[ 3*i + j ]['Valeur']




                    if ( (data_Historique[ 3*i + j ]['Coef'] == 3) and 
                        (data_Historique[ 3*i + j ]['Dégats'] != 0 or data_Historique[ 3*i + j ]['Ferme le chiffre'] != 0) ):
                    # la flechette est un triple et il a compté (meme partiellement)
                        Stats_Table[Player_Turn]['# de triple'] = Stats_Table[Player_Turn]['# de triple'] + 1

                    if ( (data_Historique[ 3*i + j ]['Coef'] == 2) and 
                        (data_Historique[ 3*i + j ]['Dégats'] != 0 or data_Historique[ 3*i + j ]['Ferme le chiffre'] != 0)
                        and data_Historique[ 3*i + j ]['Valeur'] != 25 ):
                    # la flechette est un double (mais pas un bull) et il a compté (meme partiellement)
                        Stats_Table[Player_Turn]['# de double'] = Stats_Table[Player_Turn]['# de double'] + 1

                    if( data_Historique[ 3*i + j ]['Valeur'] != 0):
                        
#                        N_Touche = N_Touche + data_Historique[ 3*i + j ]['Ferme le chiffre']  + np.max(data_Historique[ 3*i + j ]['Dégats']) / data_Historique[ 3*i + j ]['Valeur']
                        N_Touche[Player_Turn][data_Historique[ 3*i + j ]['Tour'] - 1 ] = N_Touche[Player_Turn][data_Historique[ 3*i + j ]['Tour'] - 1] + data_Historique[ 3*i + j ]['Ferme le chiffre']  + np.max(data_Historique[ 3*i + j ]['Dégats']) / data_Historique[ 3*i + j ]['Valeur']
                
        N_Touche_Tot= np.sum(N_Touche[Player_Turn]) # = au nombre de touche total pour cette equipe
        
#        Stats_Table[Player_Turn]['# Touche/ Tour'] = ( Stats_Table[Player_Turn]['# Touche/ Tour'] * ( data_Historique[ 3*i ]['Tour'] -1) + N_Touche ) / (data_Historique[ 3*i ]['Tour'])
        Stats_Table[Player_Turn]['# Touche/ Tour'] =  N_Touche_Tot  / (data_Historique[ 3*i ]['Tour'])

        
        Y[Player_Turn][ data_Historique[ 3*i  ]['Tour'] -1  ] = Stats_Table[Player_Turn][Dropdown_Value]

    
    Stats_Graph['layout']['yaxis']['title']['text'] = Dropdown_Value


    for i in range (0,len(list(Team_List.keys()))):

        Stats_Graph['data'][i]['x'] = X[i]  
        Stats_Graph['data'][i]['y'] = Y[i]

        N_Touche_array = np.array(N_Touche[i])
        N_Touche_array_Rescaled = (N_Touche_array+1) *10
        Stats_Graph.data[i].update(marker={'color': color_mapping[list(Team_List.keys())[i]], 'symbol':'circle', 'size':N_Touche_array_Rescaled})

#        print('data historique i:',data_Historique[i])
#        Stats_Graph.data[i].update( hovertemplate =f'<b>Fleche 1:{data_Historique[i][3]:.0f}</b><br>Fleche 2:{Score_History[-2][3]:.3f} <br>Fleche3:{Score_History[-1][3]:.3f} ')
        
        print('Hover Data :',Hover_Data_Fleche1)
     #   Stats_Graph.data[i].update( hovertemplate = "Col1: %{Hover_Data_Fleche1[i]}") #, "Col2: %{customdata[1]}", "Col3: %{customdata[2]}")

        Stats_Graph.data[i].update( hovertemplate =f'<b>Fleche 1:{Hover_Data_Fleche1[i][0]:.0f} ')

    print('data historique :',data_Historique)

    return Stats_Table, Stats_Graph



def Update_Live_Player(data_Live_New_Way, Turn, Team_Number_Game, Team_List):

    Number_Of_Players = len(Team_List[ list(Team_List.keys())[Turn % Team_Number_Game] ])
    Team_Turn = list(Team_List.keys())[Turn % Team_Number_Game]
    Player_Turn = Team_List[Team_Turn][int(Turn / Team_Number_Game) %  Number_Of_Players]
    
    data_Live_New_Way[Turn % Team_Number_Game]['index'] = Player_Turn

    return data_Live_New_Way


def Number_Open_Close_f(name, Team_Number_Game, data_Table, Turn_Counter_Index, Turn_Counter):
    if name == "Cricket":
        Number_Open_Close = Open_Or_Closed(name,
                                           Team_Number_Game,
                                           data_Table,
                                           Turn_Counter_Index)
    elif name == "Douze":
        Number_Open_Close = Douze_Turn(Game, 
                                       int(Turn_Counter / Team_Number_Game))
    return Number_Open_Close

def submit_score(name, Cricket_Type, data_Live_New_Way, Team_Turn, Next_Player, Dart_Number,
                 Turn, Team_Number_Game, data_Table, Darts_Total, data_Historique,
                 Column_Storage, Team_List, local_path):

    Turn_Number = int(Turn / Team_Number_Game) + 1
    Darts, Coef, data_Live_New_Way, Dart_Number = Submit_Turn(data_Live_New_Way, Team_Turn, Next_Player, Dart_Number)



    if name == "Cricket":
        data_Table, DartRound_Data = Score_Update_Cricket(Darts, Coef, Turn_Number-1, data_Table, Team_Turn, Team_Number_Game, Dart_Number , Cricket_Type)

    elif name == "Douze":
        Douze = ['12', '13', '14','Double','15','16','17','Triple','18', '19', '20', 'Bull', 'Score']
        data_Table, DartRound_Data = Score_Update_Douze(Darts, Coef, Turn_Number-1, data_Table, Team_Turn, Team_Number_Game, Dart_Number,  Douze)

    
    for i in range(Darts_Total):
        data_Historique.append( {Column_Storage[j]:DartRound_Data[i][j] for j in range(len(Column_Storage))})
    #########    data_Historique[-1][Column_Storage[5]] = np.sum(DartRound_Data[i][5])  
#     data_Historique[-1][Column_Storage[0]] = Team_List[Score_History[-3+i][0]]  
        data_Historique[-1][Column_Storage[0]] = list(Team_List.keys())[DartRound_Data[i][0]]  

    
    Turn = Turn + 1 # change index for next player
    
    data_Live_New_Way = Update_Live_Player(data_Live_New_Way, Turn, 
                                           Team_Number_Game , Team_List)

    Save_Everyone(local_path,Turn,data_Historique,data_Table)

    return data_Live_New_Way, Turn, data_Historique, data_Table, 
    
                
        
                
def End_Game(data_Table,
             Team_Number_Game,
             Team_Turn,
             Score_History,
             Team_List,
             Darts_Total,
             Cricket):

    small_victory = all([data_Table[Team_Turn][el] == 3 for el in Cricket[:-1]])
    if small_victory: # end game criteria    
        print("small victory")
        Score_min = min(data_Table[i]['Score'] for i in range(Team_Number_Game))
        
        print("data_Table:", data_Table)
        print("Team_Number_Game:", Team_Number_Game)
        print("Team_Turn:", Team_Turn)
        print("Score_History:", Score_History)
        print("Team_List:", Team_List)        
        if data_Table[Team_Turn]['Score'] == Score_min:
            Deroulement_de_Partie = pd.DataFrame(Score_History)
            Deroulement_de_Partie.to_csv('Partie.csv')  # sauvegarde le derouler de partie
            
            Player_Game_Info= [[] for i in range(len(list(Team_List.keys())))]
            
            for i in range(len(Score_History)):
                
                Player_Game_Info[int(i/Darts_Total)%len(list(Team_List.keys()))].append(Score_History[i])

                    
            for i in range(len(Team_List)):   
                Historic_Joueur = pd.read_csv('ressources/Player_Info/{}.csv'.format(list(Team_List.keys())[i]))
                Partie_Joueur = Player_Game_Info[i]
                
                
                Partie_Joueur = pd.DataFrame(Partie_Joueur,
                                             columns=Column_Storage)


                Partie_Joueur.to_csv('{}.csv'.format(list(Team_List.keys())[i]),index = False)


def Save_Everyone(local_path,Turn,data_Historique,data_Table):

    f1 = open(os.path.join(local_path, "Turn_Counter.txt"), "w")
    f1.write(str(Turn))
    f1.close()


    np.save(os.path.join(local_path, 'data_Historique.npy'), data_Historique)

    np.save(os.path.join(local_path, 'data_Table.npy'), data_Table)
