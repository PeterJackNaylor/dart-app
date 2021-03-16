import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import dash_table
import json
import plotly.express as px

import numpy as np

from flask import Flask, render_template
from flask_bootstrap import Bootstrap


def add_dash(server, url_base):

    external_stylesheets = [
        dbc.themes.BOOTSTRAP,
    ]

    app = dash.Dash(
        server=server,
        url_base_pathname=url_base,
        suppress_callback_exceptions=True,
        external_stylesheets=external_stylesheets
    )
    df = px.data.gapminder()
    fig = px.scatter(df.query("year==2007"),
                     x="gdpPercap",
                     y="lifeExp",
                     size="pop",
                     color="continent",
                     hover_name="country",
                     log_x=True,
                     size_max=60)

    app.layout = html.Div([dcc.Graph(figure=fig)])
    return server

# import argparse


# if __name__ == '__main__':
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--port", type=int,
#                         help="port number")
#     parser.add_argument("--url_base",
#                         help="base")
#     parser.add_argument("-v", "--verbose", action="store_true",
#                         help="to print information")
#     args = parser.parse_args()

#     URL_BASE = args.url_base
#     MIN_HEIGHT = 200
#     bootstrap = Bootstrap()
#     app = Flask(import_name="baby")
#     bootstrap.init_app(app)

#     # inject Dash
#     #app = add_dash(app, URL_BASE, 'button', login_reg=False)

#     @app.route("/")
#     def FUN_root():
#         global live_games
#         return render_template("create_game.html")

#     @app.route(URL_BASE+'debug')
#     def dash_app():
#         return render_template('create_game.html', dash_url=URL_BASE)

#     app_port = args.port
#     print(f'http://localhost:{app_port}{URL_BASE}/debug')
#     app.run(debug=False, port=app_port)
