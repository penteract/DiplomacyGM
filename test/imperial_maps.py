import unittest

from DiploGM.models.unit import UnitType
from test.utils import BoardBuilder,GameBuilder,title
from DiploGM.parse_order import parse_order

import logging
import sys

def orders_from_file(game, file):
    orders = {c.name:[] for c in game.variant.players}
    c = {}
    for line in file:
        line = line.strip()
        if not line:
            continue
        elif line[-1]==":":
            if line[:-1] in orders:
                #print("reading country", line)
                c = line[:-1]
            else:
                assert line.startswith("T")
                #print("reading T", line)
                for os in orders.values():
                    os.append(line[:-1].strip())
        else:
            """line = line.replace("_S"," sc")
            line = line.replace("_E"," ec")
            line = line.replace("_W"," wc")
            line = line.replace("_N"," nc")"""
            orders[c].append(line)
    for c in game.variant.players:
        #print("PLAYER",c.name)
        #print(orders[c.name])
        messages = parse_order("\n".join([".orders"]+orders[c.name]),c, game )["messages"]
        if any( "\x1b[0;31m" in m and "dlh - ahm" not in m for m in messages):
            for message in messages:
                print(message)
            print("\x1b[0;39m")
            raise Exception("Bad orders")

class TestGame(unittest.TestCase):
    def test_game_1(self):
        root = logging.getLogger("DiploGM.parse_order")
        root.setLevel(logging.DEBUG)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')

        handler.setFormatter(formatter)
        #root.addHandler(handler)
        g = GameBuilder(empty=False,variant="impdip")
        #b = g.bb
        orders_from_file(g.game, open("test/GAME/Phase 1.txt"))
        g.adjudicate()
        g.output(retreats=True)

