
import os
from flask import (Blueprint,
                   session,
                   render_template,
                   abort,
                   request,
                   redirect,
                   url_for,
                   flash)
from .utils.sql import (add_user,
                        user_info_with_delete,
                        player_info_with_delete,
                        delete_player_from_db,
                        delete_user_from_db,
                        list_users_name,
                        list_users_id,
                        check_admin)
from .utils.local_games import (live_games,
                                saved_games,
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
        games_saved = saved_games()
        games_live = live_games(live_games=gb['live_games'])
        return render_template("admin.html",
                               users=user_info,
                               players=player_info,
                               live_games=games_live,
                               saved_games=games_saved)
    else:
        return abort(403)


@admin_page.route("/add_user", methods=["POST"])
def FUN_add_user():
    if session.get("is_admin", None):
        global gb
        # only Admin should be able to add user.
        # before we add the user, we need to ensure
        # this is doesn't exist in data base. We also
        # need to ensure the id is valid.
        if request.form.get('id') in list_users_name():
            user_info = user_info_with_delete()
            player_info = player_info_with_delete()
            games_saved = saved_games()
            games_live = live_games(live_games=gb['live_games'])

            flash('User account already exists', 'danger')
            return(render_template("admin.html",
                                   id_to_add_is_duplicated=True,
                                   users=user_info,
                                   players=player_info,
                                   live_games=games_live,
                                   saved_games=games_saved))
        elif " " in request.form.get('id') or "'" in request.form.get('id'):
            user_info = user_info_with_delete()
            player_info = player_info_with_delete()
            games_saved = saved_games()
            games_live = live_games(live_games=gb['live_games'])
            flash('User account should not be spaces', 'danger')
            return(render_template("admin.html",
                                   id_to_add_is_invalid=True,
                                   users=user_info,
                                   players=player_info,
                                   live_games=games_live,
                                   saved_games=games_saved))
        else:
            id = max(list_users_id()) + 1
            is_admin = 1 if request.form.get('is_admin') == "on" else 0
            add_user(id,
                     request.form.get('id'),
                     request.form.get('pw'),
                     is_admin)
            flash('User account created', 'info')
            return(redirect(url_for("admin_page.FUN_admin")))
    else:
        return abort(403)


@admin_page.route("/delete_player/<name>/", methods=['GET'])
def FUN_delete_player(name):
    if session.get("is_admin", None):
        delete_player_from_db(name)
        flash('Player successfully deleted.', 'info')
        return(redirect(url_for("admin_page.FUN_admin")))
    else:
        return abort(403)


@admin_page.route("/delete_saved_folder/<room_game>")
def FUN_delete_folder(room_game):
    if session.get("is_admin", None):
        room, game = room_game.split('_')
        if os.path.exists(f"./ressources/local_games/{game}/{room}"):
            delete_local_folder(game, room)
            flash('Saved game successfully deleted.', 'info')
            return(redirect(url_for("admin_page.FUN_admin")))
        else:
            return abort(403)
    else:
        return abort(403)


@admin_page.route("/load_saved_game/<room_game>")
def FUN_load_folder(room_game):
    if session.get("is_admin", None):
        room, game = room_game.split('_')
        global gb
        gb["live_games"].append((room, game))
        flash('Game loaded.', 'info')
        return(redirect(f"/game/{room}/{game}"))
    else:
        return abort(403)


@admin_page.route("/delete_live_game/<room_game>")
def FUN_live_game(room_game):
    if session.get("is_admin", None):
        room, game = room_game.split('_')
        global gb
        gb['available_rooms'][game].append(room)
        gb['live_games'].remove((room, game))
        flash('Live game deleted.', 'info')
        return(redirect(url_for("admin_page.FUN_admin")))
    else:
        return abort(403)


@admin_page.route("/delete_user/<name>/", methods=['GET'])
def FUN_delete_user(name):
    if session.get("is_admin", None):
        if check_admin(name):
            flash('Can not delete admin account.', 'danger')
            # ADMIN account can't be deleted.
        else:
            delete_user_from_db(name)
            flash('User deleted.', 'info')
        return(redirect(url_for("admin_page.FUN_admin")))
    else:
        return abort(403)
