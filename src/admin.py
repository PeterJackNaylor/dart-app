
import os
from flask import (Blueprint,
                   session,
                   render_template,
                   abort,
                   request,
                   redirect,
                   url_for)
from .utils.sql import (add_user,
                        user_info_with_delete,
                        player_info_with_delete,
                        delete_player_from_db,
                        delete_user_from_db,
                        list_users_name,
                        list_users_id,
                        check_admin)
from .utils.local_games import (games_folders_and_live,
                                kill_game,
                                delete_local_folder)
from .global_variables import gb

admin_page = Blueprint("admin_page",
                      __name__)


@admin_page.route("/admin/")
def FUN_admin():
    if session.get("is_admin", None):
        global gb
        user_info = user_info_with_delete()
        player_info = player_info_with_delete()
        game_info = games_folders_and_live(live_games=gb['live_games'])
        return render_template("admin.html",
                               users=user_info,
                               players=player_info,
                               games=game_info)
    else:
        return abort(401)


@admin_page.route("/add_user", methods=["POST"])
def FUN_add_user():
    if session.get("is_admin", None):
        # only Admin should be able to add user.
        # before we add the user, we need to ensure
        # this is doesn't exist in data base. We also
        # need to ensure the id is valid.
        if request.form.get('id') in list_users_name():
            user_info = user_info_with_delete()
            player_info = player_info_with_delete()
            return(render_template("admin.html", id_to_add_is_duplicated=True,
                                   users=user_info, players=player_info))
        if " " in request.form.get('id') or "'" in request.form.get('id'):
            user_info = user_info_with_delete()
            player_info = player_info_with_delete()
            return(render_template("admin.html", id_to_add_is_invalid=True,
                                   users=user_info, players=player_info))
        else:
            id = max(list_users_id()) + 1
            is_admin = 1 if request.form.get('is_admin') == "on" else 0
            add_user(id,
                     request.form.get('id'),
                     request.form.get('pw'),
                     is_admin)
            return(redirect(url_for("admin_page.FUN_admin")))
    else:
        return abort(401)


@admin_page.route("/delete_player/<name>/", methods=['GET'])
def FUN_delete_player(name):
    if session.get("is_admin", None):
        delete_player_from_db(name)
        return(redirect(url_for("admin_page.FUN_admin")))
    else:
        return abort(401)


@admin_page.route("/delete_game_folder/<port>")
def FUN_delete_folder(port):
    if session.get("is_admin", None):
        if os.path.exists(f"./ressources/local_games/{port}"):
            delete_local_folder(port)
            return(redirect(url_for("admin_page.FUN_admin")))
        else:
            return abort(401)
    else:
        return abort(401)


@admin_page.route("/delete_live_game/<port>")
def FUN_live_game(port):
    if session.get("is_admin", None):
        global gb
        taken_ports = [el[1] for el in gb['live_games']]
        if port in taken_ports:
            kill_game(port, gb['live_games'])
            return(redirect(url_for("admin_page.FUN_admin")))
        else:
            abort(401)
    else:
        return abort(401)


@admin_page.route("/delete_user/<name>/", methods=['GET'])
def FUN_delete_user(name):
    if session.get("is_admin", None):
        if check_admin(name):
            # ADMIN account can't be deleted.
            return abort(401)

        delete_user_from_db(name)
        return(redirect(url_for("admin_page.FUN_admin")))
    else:
        return abort(401)
