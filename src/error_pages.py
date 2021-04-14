
from flask import render_template


def wrong_log_in(e):
    return render_template('403.html'), 403


def no_more_room(e):
    return render_template('406.html'), 406


def add_error_pages(app):
    app.register_error_handler(403, wrong_log_in)
    app.register_error_handler(406, no_more_room)
    return app
