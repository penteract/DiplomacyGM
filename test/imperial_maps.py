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
        if not line or line.startswith("#"):
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
                #orders[c].append(line[:-1].strip())
        else:
            """line = line.replace("_S"," sc")
            line = line.replace("_E"," ec")
            line = line.replace("_W"," wc")
            line = line.replace("_N"," nc")"""
            orders[c].append(line)
    file.close()
    for c in sorted(game.variant.players,key=lambda x:x.name):
        #print("PLAYER",c.name)
        #print(orders[c.name])
        parsed = parse_order("\n".join([".orders"]+orders[c.name]),c, game )
        #print("po:",,c.name)
        messages = parsed["messages"] if "messages" in parsed else [parsed["message"]]
        #parse_order("\n".join([".orders"]+orders[c.name]),c, game )["messages"]
        if any( "\x1b[0;31m" in m
               and "dlh - ahm" not in m
               and "`+ A ghe`: You haven't cored Ghent." not in m
               for m in messages):
            for message in messages:
                #n = message.rfind("```")
                #print(c.name, message[n+3:])
                print(message)
            print("\x1b[0;39m")
            #raise Exception("Bad orders")
        if "messages" not in parsed and not any(True for b in game.get_current_retreat_boards()):
            print(c,messages[0])
            raise Exception("No orders")

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
        g.adjudicate()
        #g.output(retreats=True)
        #title("Turn 2")
        orders_from_file(g.game, open("test/GAME/Phase 2.txt"))
        g.adjudicate()
        #g.output(retreats=True)
        #title("Turn 2 Retreats")
        orders_from_file(g.game, open("test/GAME/Phase 2 Retreats.txt"))
        g.adjudicate()
        #g.output(retreats=True)
        #title("Turn 3")
        orders_from_file(g.game, open("test/GAME/Phase 3.txt"))
        g.adjudicate()
        #g.output(retreats=True)
        orders_from_file(g.game, open("test/GAME/Phase 3 Retreats.txt"))
        g.adjudicate()
        orders_from_file(g.game, open("test/GAME/Phase 4.txt"))
        title("Awaiting Turn 4 retreats")
        g.adjudicate()
        g.output(retreats=True)
