from flask import (Blueprint,
                   session,
                   render_template,
                   request,
                   redirect,
                   url_for)

from .utils.sql import (list_users_name,
                        verify,
                        check_admin)
from .global_variables import gb
# blueprint for better python file management
home_page = Blueprint("home_page",
                      __name__)


@home_page.route("/")
def FUN_root():
    global gb
    is_user = True if session.get("current_user", None) else False
    return render_template("index.html",
                           live_games=gb['live_games'],
                           is_user=is_user)


@home_page.route("/login", methods=["POST"])
def FUN_login():
    id_submitted = request.form.get("id")
    check_id = verify(id_submitted, request.form.get("pw"))
    if (id_submitted in list_users_name()) and check_id:
        session['current_user'] = id_submitted
        session['is_admin'] = check_admin(id_submitted)
    return(redirect(url_for("home_page.FUN_root")))


@home_page.route("/logout/")
def FUN_logout():
    session.pop("current_user", None)
    session.pop("is_admin", None)
    return(redirect(url_for("home_page.FUN_root")))
