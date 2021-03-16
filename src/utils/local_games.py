import os
from glob import glob
import shutil


def games_folders_and_live(path="./ressources/local_games", live_games=[]):
    output = []
    folders = glob(os.path.join(path, '*'))
    for f in folders:
        port = os.path.basename(f)
        output.append([port, "folder", f"/delete_game_folder/{port}"])
    for game in live_games:
        port = game[1]
        output.append([port, "process", f"/delete_live_game/{port}"])
    return output


def check_or_create(folder):
    if not os.path.exists(folder):
        os.mkdir(folder)


def delete_local_folder(port, path="./ressources/local_games"):
    shutil.rmtree(os.path.join(path, f"{port}"))


def kill_game(port, live_games):
    for game in live_games:
        if game[1] == port:
            break
    proc = game[3]
    proc.kill()
    live_games.remove(game)
    return live_games
