
import datetime
import sqlite3
import hashlib

user_db_file_location = "ressources/users.db"
player_db_file_location =  "ressources/players.db"

def add_player(id, name, nickname, shoot_hand):
    _conn = sqlite3.connect(player_db_file_location)
    _c = _conn.cursor()
    num = 0 if shoot_hand == "right" else 1
    now = datetime.datetime.now()
    _c.execute(f"INSERT INTO players values(?, ?, ?, ?, ?)", (id, name, nickname, num, now))
    
    _conn.commit()
    _conn.close()

def add_user(id, name, password, is_admin):
    _conn = sqlite3.connect(user_db_file_location)
    _c = _conn.cursor()
    now = datetime.datetime.now()
    pwd_encoded = hashlib.sha256(password.encode()).hexdigest()
    _c.execute(f"INSERT INTO users values(?, ?, ?, ?, ?)", (id, name, pwd_encoded, is_admin, now))
    
    _conn.commit()
    _conn.close()

def delete_user_from_db(id):
    _conn = sqlite3.connect(user_db_file_location)
    _c = _conn.cursor()
    _c.execute("DELETE FROM users WHERE name = '" + id + "';")
    _conn.commit()
    _conn.close()
    

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
    result = _c.fetchone()[0] == hashlib.sha256(pw.encode()).hexdigest()
    
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
    categ = "data_users" # "data_players"

    if categ == "data_players":
        file = "ressources/players.db"
        db = "players"
        add_player(0, "Peter", "PJ", "right")
        add_player(1, "Bruno", "B-Dawg", "left")

    if categ == "data_users":
        file = "ressources/new_database/users.db"
        db = "users"
        add_user(0, "Peter", "pass", 1)
        add_user(1, "Bruno", "pass", 1)
        add_user(2, "Blue", "pass", 0)

if __name__ == "__main__":
    main()