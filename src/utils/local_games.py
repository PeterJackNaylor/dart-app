import os
from glob import glob
import shutil


def live_games(path="./ressources/local_games", live_games=[]):
    output = []
    for game in live_games:
        room = game[0]
        game = game[1]
        del_game = f"/delete_live_game/{room}_{game}"
        save_game = f"/save_live_game/{room}_{game}"
        output.append([room, game, del_game, save_game])
    return output


def temp_games(path="./ressources/local_games"):
    output = []
    folders = glob(os.path.join(path, '*', '*'))
    for f in folders:
        room = f.split('/')[-1]
        game = f.split('/')[-2]
        del_game_f = f"/delete_temp_folder/{room}_{game}"
        load_game = f"/load_temp_game/{room}_{game}"
        output.append([room, game, del_game_f, load_game])
    return output


def saved_games(path="./ressources/saved_games"):
    output = []
    folders = glob(os.path.join(path, '*'))
    for f in folders:
        name = f.split('/')[-1]
        del_game_f = f"/delete_saved_folder/{name}"
        load_game = f"/load_saved_game/{name}"
        output.append([name, del_game_f, load_game])
    return output


def check_or_create(folder):
    if not os.path.exists(folder):
        os.mkdir(folder)


def delete_local_folder(name, path="./ressources/local_games"):
    shutil.rmtree(os.path.join(path, name))


def load_saved_folder(room, game, save_name_folder, path="./ressources/"):
    dest = shutil.move(os.path.join(path, "saved_games", save_name_folder),
                       os.path.join(path, "local_games", game, room))
    return dest


def save_folder(room, game, save_name_folder, path="./ressources/"):
    dest = shutil.move(os.path.join(path, "local_games", game, room),
                       os.path.join(path, "saved_games", save_name_folder))
    return dest
