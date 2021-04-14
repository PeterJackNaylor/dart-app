
"""Initialize Flask app."""
from flask import Flask
from flask_bootstrap import Bootstrap
from flaskext.markdown import Markdown

# for the flask page


def create_app():
    """Create Flask application."""
    app = Flask(__name__,
                instance_relative_config=False)
    from .error_pages import add_error_pages
    app = add_error_pages(app)
    app.config.from_object('config')

    with app.app_context():
        from .global_variables import init_global
        init_global()
        # Import parts of our application
        from .home import home_page
        from .rules import rule_page
        from .create_game import create_game_page, root_url_games
        from .global_stats import global_stats_page, page_url
        from .utils.add_dash_table import add_dash as add_dash_table
        from .utils.add_dash_games import add_dash_games
        from .admin import admin_page

        bootstrap = Bootstrap()
        app.register_blueprint(home_page)

        Markdown(app)
        app.register_blueprint(rule_page)

        app.register_blueprint(create_game_page)

        app.register_blueprint(global_stats_page)
        bootstrap.init_app(app)
        app = add_dash_table(app, page_url)
        app = add_dash_games(app, root_url_games)

        app.register_blueprint(admin_page)

        return app
