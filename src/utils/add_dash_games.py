import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from flask import session

from ..global_variables import gb


layouts = []


def generate_games(app):
    global gb
    global layouts
    # All game should be defined with an if statement
    for game in gb["games"]:
        if game == "Cricket":
            from ..dart_games.app_dashboard_Game import create_ap
        elif game == "Template":
            from ..dart_games.app_template import create_ap

        for i in range(gb["MAX_ROOMS"]):
            app, layout = create_ap(app, i)
            layouts.append(layout)


def load_game(room_number, game_name):
    global layouts
    global gb
    game_index = gb['games'].index(game_name)
    return layouts[int(room_number) + gb["MAX_ROOMS"] * game_index]


def add_dash_games(server, url_base):

    external_stylesheets = [
        dbc.themes.BOOTSTRAP,
    ]

    app = dash.Dash(
        server=server,
        url_base_pathname=url_base,
        suppress_callback_exceptions=True,
        external_stylesheets=external_stylesheets
    )
    def def_layout():
        url_bar_and_content_div = html.Div([
            dcc.Location(id='url', refresh=True),
            html.Div(id='page-content')
        ])
        return url_bar_and_content_div

    # url_bar_and_content_div = html.Div([
    #     dcc.Location(id='url', refresh=False),
    #     html.Div(id='page-content')
    # ])
    app.layout = def_layout
    generate_games(app)

    # Index callbacks
    @app.callback(Output('page-content', 'children'),
                  Input('url', 'pathname'))
    def display_page(pathname):
        print("Don't forget to disable this")
        if True: #session.get("current_user", None):
            global gb
            game_name = pathname.split('/')[2]
            room_number = pathname.split('/')[3]
            if True:#(room_number, game_name) in gb['live_games']:
                layout = load_game(f"{room_number}", game_name)
                return layout
            else:
                return "401"
        else:
            return "Forbidden"

    return server
