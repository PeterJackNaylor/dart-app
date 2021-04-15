
import datetime
import sqlite3
import hashlib

user_db_file_location = "ressources/users.db"
player_db_file_location = "ressources/players.db"


def player_info_with_delete():
    user_info = list_player_info()
    user_info = list(zip(*user_info))
    delete_list = zip(["/delete_player/"] * len(user_info[0]), user_info[0])
    delete_buttons = [x + y for x, y in delete_list]
    user_info.append(tuple(delete_buttons))
    user_info = zip(*user_info)
    return user_info


def user_info_with_delete():
    user_info = list_users()
    user_info = list(zip(*user_info))
    delete_list = zip(["/delete_user/"] * len(user_info[1]), user_info[1])
    delete_buttons = [x + y for x, y in delete_list]
    user_info.append(tuple(delete_buttons))
    user_info = zip(*user_info)
    return user_info


def add_player(name, nickname, shoot_hand, height, genital_size):
    _conn = sqlite3.connect(player_db_file_location)
    _c = _conn.cursor()
    hand = 1 if shoot_hand == "left" else 1
    now = datetime.datetime.now()
    game_won, favorite_number, game_played = 0, 0, 0

    inp = (name, nickname, hand, height, genital_size,
           now, game_won, favorite_number, game_played)
    _c.execute("INSERT INTO players values(?, ?, ?, ?, ?, ?, ?, ?, ?)", inp)
    _conn.commit()
    _conn.close()


def delete_player_from_db(name):
    _conn = sqlite3.connect(player_db_file_location)
    _c = _conn.cursor()
    _c.execute("DELETE FROM players WHERE name = '" + name + "';")
    _conn.commit()
    _conn.close()


def player_info_for_create():
    _conn = sqlite3.connect(player_db_file_location)
    _c = _conn.cursor()

    _c.execute("SELECT name, nickname, game_won, favorite_number, game_played FROM players;")
    result = [x for x in _c.fetchall()]

    _conn.close()
    return result


def list_players_name():
    _conn = sqlite3.connect(player_db_file_location)
    _c = _conn.cursor()

    _c.execute("SELECT name FROM players;")
    result = [x[0] for x in _c.fetchall()]

    _conn.close()
    return result


def add_user(id, name, password, is_admin):
    _conn = sqlite3.connect(user_db_file_location)
    _c = _conn.cursor()
    now = datetime.datetime.now()
    pwd_encoded = hashlib.sha256(password.encode()).hexdigest()
    _c.execute("INSERT INTO users values(?, ?, ?, ?, ?)",
               (id, name, pwd_encoded, is_admin, now))
    _conn.commit()
    _conn.close()


def delete_user_from_db(id):
    _conn = sqlite3.connect(user_db_file_location)
    _c = _conn.cursor()
    _c.execute("DELETE FROM users WHERE name = '" + id + "';")
    _conn.commit()
    _conn.close()


def list_player_info():
    _conn = sqlite3.connect(player_db_file_location)
    _c = _conn.cursor()

    _c.execute("SELECT name, nickname, shoot_hand, height, genital_size, creation_date, game_won, favorite_number, game_played FROM players;")
    result = [x for x in _c.fetchall()]
    _conn.close()
    return result


def list_users():
    _conn = sqlite3.connect(user_db_file_location)
    _c = _conn.cursor()

    _c.execute("SELECT user_id, name, is_admin, creation_date FROM users;")
    result = [x for x in _c.fetchall()]
    _conn.close()
    return result


def list_users_name():
    _conn = sqlite3.connect(user_db_file_location)
    _c = _conn.cursor()

    _c.execute("SELECT name FROM users;")
    result = [x[0] for x in _c.fetchall()]

    _conn.close()
    return result


def list_users_id():
    _conn = sqlite3.connect(user_db_file_location)
    _c = _conn.cursor()

    _c.execute("SELECT user_id FROM users;")
    result = [x[0] for x in _c.fetchall()]

    _conn.close()
    return result


def verify(name, pw):
    _conn = sqlite3.connect(user_db_file_location)
    _c = _conn.cursor()

    _c.execute("SELECT password FROM users WHERE name = '" + name + "';")
    fetch = _c.fetchone()
    result = False

    if fetch:
        # if no username matches, there are no possible passwords...
        result = fetch[0] == hashlib.sha256(pw.encode()).hexdigest()
        _conn.close()

    return result


def check_admin(name):
    _conn = sqlite3.connect(user_db_file_location)
    _c = _conn.cursor()

    _c.execute("SELECT is_admin FROM users WHERE name = '" + name + "';")
    result = _c.fetchone()[0]
    _conn.close()

    return result == "1"


def main():
    categ = "data_players"
    # "data_players"

    if categ == "data_players":
        # file = "ressources/players.db"
        # db = "players"
        add_player("Peter", "PJ", "right", 1.83, 30)
        add_player("Bruno", "B-Dawg", "left", 1.80, 20)

    if categ == "data_users":
        # file = "ressources/new_database/users.db"
        # db = "users"
        add_user(0, "Peter", "pass", 1)
        add_user(1, "Bruno", "pass", 1)
        add_user(2, "Blue", "pass", 0)


if __name__ == "__main__":
    main()
