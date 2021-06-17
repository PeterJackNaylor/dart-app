align_style = {"textAlign": "center"}

style_table = {
    "maxHeight": "50ex",
    "width": "100%",
    "minWidth": "100%",
    "horizontalAlign": "bottom",
}

tab_style = {"borderBottom": "1px solid #d6d6d6", "fontWeight": "bold"}

tab_selected_style = {
    "borderTop": "1px solid #d6d6d6",
    "borderBottom": "1px solid #d6d6d6",
    "backgroundColor": "#119DFF",
    "color": "white",
    "padding": "6px",
}

styles = {"pre": {"border": "thin lightgrey solid", "overflowX": "scroll"}}


def style_data_conditional(turn):
    return [
        {"if": {"row_index": "odd"}, "backgroundColor": "rgb(248, 248, 248)"},
        {
            "if": {"row_index": turn},
            "backgroundColor": "rgb(250, 200, 250)",
            "fontWeight": "bold",
        },
    ]


style_header = {"backgroundColor": "rgb(230, 230, 230)", "fontWeight": "bold"}


color_mapping = {
    "Blue": "rgb(31,120,180)",
    "BlueLight": "rgb(166,206,227)",
    "Pink": "rgb(222,119,174)",
    "PinkLight": "rgb(241,182,218)",
    "Green": "rgb(51,160,44)",
    "GreenLight": "rgb(178,223,138)",
    "Red": "rgb(227,26,28)",
    "RedLight": "rgb(251,154,153)",
    "Orange": "rgb(253,191,111)",
    "OrangeLight": "rgb(255,127,0)",
    "Purple": "rgb(202,178,214)",
    "PurpleLight": "rgb(106,61,154)",
    "Brown": "rgb(255,255,153)",
    "BrownLight": "rgb(177,89,40)",
}


def style_data_cond_historic(Team_List):

    style_data_cond = [
        {
            "if": {
                "filter_query": "{{Equipe}} = {} && {{Fleche numero}} = 1".format(
                    team_color
                )
            },
            "backgroundColor": color_mapping[team_color],
            "color": "white",
        }
        for team_color in list(Team_List.keys())
    ]

    style_data_cond += [
        {
            "if": {
                "filter_query": "{{Equipe}} = {} && {{Fleche numero}} != 1".format(
                    team_color
                )
            },
            "backgroundColor": color_mapping[team_color + "Light"],
            "color": "white",
        }
        for team_color in list(Team_List.keys())
    ]

    return style_data_cond


style_data_basic = [
    {"if": {"row_index": "odd"}, "backgroundColor": "rgb(243, 243, 243)"}
]

score_style_table = style_table.copy()

score_style_table["margin-left"] = "15px"
