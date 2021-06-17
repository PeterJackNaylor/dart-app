from .utils.local_games import check_or_create


def init_global():
    global gb
    MAX_ROOMS = 1
    gb = {}
    gb["MAX_ROOMS"] = MAX_ROOMS
    gb["live_games"] = []
    rooms = [f"{i}" for i in range(0, MAX_ROOMS)]

    gb['teams'] = ["Blue", "Pink", "Red", "Green",
                   "White", "Brown", "The red devils"]
    gb["games"] = ["Cricket", "Template"]
    gb['available_rooms'] = {el: rooms.copy() for el in gb["games"]}

    for game in gb["games"]:
        check_or_create(f"ressources/local_games/{game}")
