
import dash_core_components as dcc
import dash_html_components as html
import dash_table

from ..utils.plot_geojson import dart_plot
from .aux import load_local_dictionnary, init_db, Column_Live_Stats_Graph
from .styles_dash import (align_style,
                          style_table,
                          style_data_conditional,
                          style_header,
                          tab_style,
                          score_style_table,
                          tab_selected_style,
                          style_data_cond,
                          style_data_conditional)

def generate_tab_1(turn_n, dart_n, score, live_stats,
                   teams, n_teams, df_score_live, df_score,
                   tab_style, legend):
    

    tab_child = []

    var = [('Dart_Counter', dart_n)]
        #    ('Turn_Counter', turn_n),
        #    ,
        #    ('Score_Storage', score),
        #    ('Y_Live-Stat', live_stats),
        #    ('Game_Players', teams),
        #    ('Team_Number', n_teams)]
    for id_, data in var:
        tab_child.append(dcc.Store(id=id_,
                                   data=data))
    
    #Maybe useless, button to update game if it has been closed
    tab_child += [html.Div([html.Button('Mise à jour',
                                        id='Refresh',
                                        n_clicks=0)])]

    tab_child += [html.Div([
            # Maybe useless, a display to indicate 
            # how many turns have been played
            html.H1(id='Joueur',
                    children=['Tour numéro: {}'.format(turn_n)]),])]
            # html.H1(children= ' "{}"'.format(df_Score_Live_New_Way['index'][Turn_Counter]),id= 'Joueur1' ),

    #  Buttons to submit the darts inputs, cancel the input, or go back to the previous player


    tab_child += [html.Button('Valider ce tour',
                              id='submit_round',
                              n_clicks=0)]
    tab_child += [html.Button('Annuler ce tour',
                              id='cancel_round',
                              n_clicks=0)]
    tab_child += [html.Button('Revenir au joueur precedent ',
                              id='precedent_round',
                              n_clicks=0)]

    first_dash_table = [{'name': ['Joueur', ''], 'id': 'index'},
                        {'name': ['Equipe', ''], 'id': 'Equipe'},
                        {'name': ['Fleche 1', 'Value'], 'id': 'Fleche 1'},
                        {'name': ['Fleche 1', 'Coef'], 'id': 'Coef 1'},
                        {'name': ['Fleche 2', 'Value'], 'id': 'Fleche 2'},
                        {'name': ['Fleche 2', 'Coef'], 'id': 'Coef 2'},
                        {'name': ['Fleche 3', 'Value'], 'id': 'Fleche 3'},
                        {'name': ['Fleche 3', 'Coef'], 'id': 'Coef 3'}]
    
    live_score_table = dash_table.DataTable(id='Score_Live_New_Way',
                                            columns=first_dash_table,
                                            data=df_score_live.to_dict('records'),
                                            style_cell=align_style,
                                            style_table=style_table,
                                            style_data_conditional=style_data_conditional(turn_n),
                                            style_header=style_header,
                                            merge_duplicate_headers=True)

    tab_child_child = [html.Div(live_score_table,
                                className="six columns")]

    current_score_table = dash_table.DataTable(
                                id='Score_Table',
                                columns=[{"name": i, "id": i} for i in df_score.columns],
                                data=df_score.to_dict('records'),
                                style_cell=align_style,
                                style_table=score_style_table,
                                # style_data_conditional=styles,
                                style_header=style_header)

    tab_child_child += [html.Div([legend,
                                  current_score_table], 
                            # Table displaying the total score
                            # (refreshes only after submission of the round)
                                 className="height columns")]
    tab_child += [html.Div(html.Div(tab_child_child, 
                                    className="row"), 
                           className="container")]
    fig = dart_plot()

    tab_child += [dcc.Graph(
                    id='basic-interactions',
                    figure=fig
                )]

#    print(tab_child)
    return tab_child
#    return dcc.Tab(label='Game',
#                   style=tab_style,
#                   selected_style=tab_selected_style, 
#                   children=tab_child)


def generate_tab_2(df_Stat_Live, fig_Stat):
    children = []

    children += [dash_table.DataTable(
                        id='Stat_Live',
                        columns=[{"name": i, "id": i} for i in df_Stat_Live.columns],
                        style_cell=align_style,
                        style_table=style_table,
                        style_data_conditional=style_data_cond,
                        style_header=style_header,
                        data=df_Stat_Live.to_dict('records')
                )]

    children += [dcc.Dropdown(
                    id='Stat_Dropdown',
                    options=[{'label': Column_Live_Stats_Graph[i], 'value': i} for i in range(len(Column_Live_Stats_Graph))],
                    value=0)]
    
    children += [dcc.Graph(
                    id='Graph_Live_Stat',
                    animate=True,
                    figure=fig_Stat
                )]
    
    children += [html.Button('Mise à jour Graphiques',
                             id='Button_Graph',
                             n_clicks=0)]


    return children    
#    return dcc.Tab(label='Live_Stats',
#                   style=tab_style,
#                   selected_style=tab_selected_style,
#                   children=children)


#def generate_tab_3(df_Score_Storage):
#    children = []
#    children += [dash_table.DataTable(
#                        id='Historique_Partie',
#                        columns = [{"name": i, "id": i} for i in df_Score_Storage.columns],
#                        style_cell={'textAlign': 'center'},
#                        style_table=style_table,
#                        style_data_conditional=style_data_cond,
#                        style_header=style_header,
#                        data = df_Score_Storage.to_dict('records'),
#                )]
#    return dcc.Tab(label='Historique',
#                   style=tab_style,
#                   selected_style=tab_selected_style,
#                   children=children)

def generate_tab_3(df_Score_Storage):
    children = []
    children += [dash_table.DataTable(
                        id='Historique_Partie',
                        columns = [{"name": i, "id": i} for i in df_Score_Storage.columns],
                        style_cell={'textAlign': 'center'},
                        style_table=style_table,
                        style_data_conditional=style_data_cond,
                        style_header=style_header,
                        data = df_Score_Storage.to_dict('records'),
                )]

    return children
#    return dcc.Tab(label='Historique',
#                   style=tab_style,
#                   selected_style=tab_selected_style,
#                   children=children)

def generate_tab_4():
    children = [html.Button('Mise à jour Graphiques',
                             id='Big_button',
                             n_clicks=0)]
    children += [html.Div("no default", id="text")]
    return children


def cricket_layout(local_path):

    game_att = load_local_dictionnary(local_path, "Cricket")
    
    init = init_db(game_att)
    Turn_Counter, Flechette_Compteur, Score_Storage, Y_Live_Stats = init[0:4]
    df_Score_Live_New_Way, df_Score, df_Stat_Live, fig_Stat = init[4:8]
    df_Score_Storage, legend = init[8:10]

    layout = html.Div([
        dcc.Tabs(
                id='tabs',
                value = 'tab-main', 
        #        children=[
        #        generate_tab_1(Turn_Counter, Flechette_Compteur, Score_Storage,
        #                       Y_Live_Stats, game_att['Team_List'], game_att['n_t'], 
        #                       df_Score_Live_New_Way,
        #                       df_Score, tab_style, legend),
        #        generate_tab_2(df_Stat_Live, fig_Stat),
        #        generate_tab_3(df_Score_Storage)
        #    ]
                children=[
                    dcc.Tab(label='Game', value='tab-main',style=tab_style ,selected_style=tab_selected_style),
                    dcc.Tab(label='Tab two', value='tab-stat',style=tab_style ,selected_style=tab_selected_style),
                    dcc.Tab(label='Tab three', value='tab-historique',style=tab_style ,selected_style=tab_selected_style),
                    dcc.Tab(label='Tab four', value='tab-example',style=tab_style ,selected_style=tab_selected_style)
                ]
            ),
            html.Div(id='tab-content')
    ])
    return layout
