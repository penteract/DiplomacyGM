import unittest

from DiploGM.models.unit import UnitType
from test.utils import BoardBuilder,GameBuilder,title
from DiploGM.parse_order import parse_order

import logging
import sys

class TestGame(unittest.TestCase):
    def test_game_1(self):
        root = logging.getLogger("DiploGM.parse_order")
        root.setLevel(logging.DEBUG)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')

        handler.setFormatter(formatter)
        #root.addHandler(handler)
        g = GameBuilder(empty=False)
        #b = g.bb

        with open("test/hTurn5.txt") as orders_file:
            orders = None
            c = None
            title(__name__)
            for line in orders_file:
                line = line.strip()

                if not line:
                    continue
                if line.startswith("TURN") or line.startswith("RETREATS"):
                    #print("reading turn", line)
                    if orders is not None:
                        for c in g.game.variant.players:
                            #print("PLAYER",c.name)
                            #print(orders[c.name])
                            messages = parse_order("\n".join([".orders"]+orders[c.name]),c, g.game )["messages"]
                            if any( "\x1b[0;31m" in m for m in messages):
                                for message in messages:
                                    print(message)
                                print("\x1b[0;39m")
                                #raise Exception("Bad orders")
                        g.adjudicate()
                        if line.startswith("TURN") and g.game.can_skip_retreats():
                            g.adjudicate()
                        g.output(retreats=True)
                        if "4" in line:
                            #break
                            pass
                    title(line)
                        #break
                    orders = {c.name:[] for c in g.game.variant.players}
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



#         russia_order = ".order\n" + \
#             "Timeline 1: Spring 1901\n" + \
#             "F Sevastopol - Black Sea\n"
#         parsed_orders = parse_order(russia_order, b.russia, g.game)
#         print("test_move_order")
#         print(parsed_orders["messages"])
#         for x in parsed_orders["messages"]:
#             print(x)
#         turkey_order = """.order
#             Timeline 1: Spring 1901
#             F Ankara - Black Sea
#             A Con - Bul
#             A Smy - Ank
# """
#         parsed_orders = parse_order(turkey_order, b.turkey, g.game)
#         print("test_move_order")
#         print(parsed_orders["messages"])
#         for x in parsed_orders["messages"]:
#             print(x)
#
#         g.adjudicate()
