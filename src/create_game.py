import os
import subprocess
import shlex
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
from .utils.pickle import save_dic, open_dic
from .global_variables import gb

# blueprint for better python file management
create_game_page = Blueprint("create_game_page",
                             __name__)


@create_game_page.route("/game/<port>")
def FUN_game_page(port):
    if session.get("current_user", None):
        global gb
        taken_ports = [el[1] for el in gb['live_games']]
        url_base = "/game_room/"
        if port not in taken_ports:
            # we would load all meta data of the game
            dic = open_dic(f'ressources/local_games/{port}/meta.pickle')
            import os; print(os.getcwd())
            py_f = "src/dart_games/bruno_table.py"
            command = f'python {py_f} --port={port} --url_base={url_base} --param={dic["param"]}'
            logfile = open(f'ressources/local_games/{port}/output.log', 'w', 1)
            proc = subprocess.Popen(shlex.split(command), stdout=logfile)
            game_info = tuple([proc.pid, port, url_base, proc, logfile])
            gb['live_games'].append(game_info)
        return render_template("dash_page.html",
                               dash_url=f"http://127.0.0.1:{port}{url_base}",
                               min_height=800)
    else:
        return abort(401)


@create_game_page.route("/start_game", methods=["POST"])
def FUN_start_game():
    if session.get("current_user", None):
        player_info = player_info_for_create()
        picked_players = []
        for player_attribute in player_info:
            if request.form.get(f"tick_{player_attribute[0]}") == "on":
                picked_players.append((player_attribute[0],
                                       request.form.get(f"team_{player_attribute[0]}")))
        name = picked_players[0][0] + picked_players[1][0]
        # we would save all meta data of the game
        global gb
        port = gb['available_ports'].pop()
        os.mkdir(f'ressources/local_games/{port}')
        save_dic(f'ressources/local_games/{port}/meta.pickle', {'param': name})
        return(redirect(url_for("create_game_page.FUN_game_page", port=port)))
    else:
        return abort(401)


@create_game_page.route("/create_game/")
def FUN_create_game():
    if session.get("current_user", None) is not None:
        player_info = player_info_for_create()
        colors = ["Blue", "Pink", "Red", "Green", "White"]
        games = ["Cricket", "The pit"]
        return render_template("create_game.html",
                               player_info=player_info,
                               teams=colors,
                               games=games)
    else:
        return abort(401)


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
        return abort(401)
