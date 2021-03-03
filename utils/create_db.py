import sqlite3

database = "users" # "players"


if database == "players":
    f = "ressources/new_database/players.db"
    connection = sqlite3.connect(f)
    cursor = connection.cursor()

    sql_command = f"""
    CREATE TABLE {database} ( 
    player_id INTEGER PRIMARY KEY, 
    name VARCHAR(20), 
    nickname VARCHAR(30), 
    shoot_hand CHAR(1),
    creation_date DATE);"""

elif database == "users":
    f = "ressources/new_database/users.db"
    connection = sqlite3.connect(f)
    cursor = connection.cursor()

    sql_command = f"""
    CREATE TABLE {database} ( 
    user_id INTEGER PRIMARY KEY, 
    name VARCHAR(20), 
    password VARCHAR(30), 
    is_admin CHAR(1),
    creation_date DATE);"""

elif database == "crocket_historic":
    f = "ressources/new_database/historic_crocket.db"
    connection = sqlite3.connect(f)
    cursor = connection.cursor()

    sql_command = f"""
    CREATE TABLE {database} ( 
    shoot_id INTEGER PRIMARY KEY, 
    game_type VARCHAR(20), 
    set_id INTEGER,
    round INTEGER, 
    shot_number INTEGER,
    player INTEGER,
    team VARCHAR(20), 
    x DECIMAL,
    y DECIMAL,
    value INTEGER,
    point_given INTEGER,
    point_taken INTEGER,
    time
    creation_date DATE);"""


cursor.execute(sql_command)


