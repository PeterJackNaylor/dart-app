
import random


def init_global():
    global gb
    gb = {}
    gb['live_games'] = []
    ports = list(range(2000, 3000))
    random.shuffle(ports)
    gb['available_ports'] = ports
