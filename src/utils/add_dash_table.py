import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px


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
