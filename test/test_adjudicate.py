import unittest

from DiploGM.models.unit import UnitType
from test.utils import BoardBuilder,GameBuilder
from DiploGM.parse_order import parse_order

class TestAdjudicate(unittest.TestCase):
    def test_adj_1(self):
        g = GameBuilder(empty=False)
        b = g.bb


        russia_order = ".order\n" + \
            "Timeline 1: Spring 1901\n" + \
            "F Sevastopol - Black Sea\n"
        parsed_orders = parse_order(russia_order, b.russia, g.game)
        print("test_move_order")
        print(parsed_orders["messages"])
        for x in parsed_orders["messages"]:
            print(x)
        turkey_order = """.order
            Timeline 1: Spring 1901
            F Ankara - Black Sea
            A Con - Bul
            A Smy - Ank
"""
        parsed_orders = parse_order(turkey_order, b.turkey, g.game)
        print("test_move_order")
        print(parsed_orders["messages"])
        for x in parsed_orders["messages"]:
            print(x)

        g.adjudicate()
