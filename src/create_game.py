import os
from flask import (Blueprint,
                   session,
                   render_template,
                   abort,
                   request,
                   redirect,
                   url_for)

from .utils.sql import (player_info_for_create,
                        add_player,
                        list_players_name)
from .utils.pickle import save_dic
from .utils.local_games import check_or_create
from .global_variables import gb

# blueprint for better python file management
create_game_page = Blueprint("create_game_page",
                             __name__)


root_url_games = "/game_room/"


@create_game_page.route("/game/<room_number>/<game>")
def FUN_game_page(room_number, game):
    if session.get("current_user", None):
        dash_url = f"{root_url_games}{game}/{room_number}/"
        return render_template("dash_page.html",
                               dash_url=dash_url,
                               min_height=800)
    else:
        return abort(403)


@create_game_page.route("/start_game", methods=["POST"])
def FUN_start_game():
    if session.get("current_user", None):
        global gb
        player_info = player_info_for_create()
        players = []
        teams = []
        for player_attribute in player_info:
            if request.form.get(f"tick_{player_attribute[0]}") == "on":
                players.append(player_attribute[0])
                team = request.form.get(f"team_{player_attribute[0]}")
                teams.append(team)
        game = request.form.get('picked_game')
        # we would save all meta data of the game
        if len(gb['available_rooms'][game]):
            room_number = gb['available_rooms'][game].pop(0)
            game_local_url = f'ressources/local_games/{game}/{room_number}/'
            check_or_create(game_local_url)

            meta_data = {"teams": teams,
                         "picked_players": players,
                         "picked_game": game}
            gb["live_games"].append((room_number, game))
            save_dic(os.path.join(game_local_url, 'meta.pickle'),
                     meta_data)
            return(redirect(url_for("create_game_page.FUN_game_page",
                                    room_number=room_number,
                                    game=game)))
        else:
            return abort(406)
    else:
        return abort(403)


@create_game_page.route("/create_game/")
def FUN_create_game():
    if session.get("current_user", None) is not None:
        global gb
        player_info = player_info_for_create()

        colors = gb["teams"]
        games = gb["games"]
        return render_template("create_game.html",
                               player_info=player_info,
                               teams=colors,
                               games=games)
    else:
        return abort(403)


@create_game_page.route("/add_player", methods=["POST"])
def FUN_add_player():
    if session.get("current_user", None):
        # only Admin should be able to add user.
        # before we add the user, we need to ensure this is doesn't exist
        # in database. We also need to ensure the id is valid.
        if request.form.get('name') in list_players_name():
            return(render_template("create_game.html",
                                   id_to_add_is_duplicated=True))
        if " " in request.form.get('name') or "'" in request.form.get('name'):
            # player_info
            return(render_template("create_game.html",
                                   id_to_add_is_invalid=True))
        else:
            add_player(request.form.get('name'),
                       request.form.get('nickname'),
                       request.form.get('hand'),
                       request.form.get('height'),
                       request.form.get('genital_size'))
            return(redirect(url_for("create_game_page.FUN_create_game")))
    else:
        return abort(403)
