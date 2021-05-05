



align_style = {'textAlign': 'center'}

style_table = {'maxHeight': '50ex',
               'width': '100%',
               'minWidth': '100%',
               'horizontalAlign': 'bottom'}

tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}


def style_data_conditional(turn):
    return [{'if': {'row_index': 'odd'},
             'backgroundColor': 'rgb(248, 248, 248)'},
            {'if': {'row_index': turn},
             'backgroundColor': 'rgb(250, 200, 250)',
             'fontWeight': 'bold'}]


style_header = {'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'}

style_data_cond = [{'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(243, 243, 243)'}]

score_style_table = style_table.copy()

score_style_table["margin-left"] = "15px"
