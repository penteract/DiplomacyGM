import unittest

from DiploGM.models.order import ConvoyTransport, Core, Hold, Move, Support
from DiploGM.models.unit import UnitType
from DiploGM.parse_order import parse_order, parse_remove_order
from test.utils import BoardBuilder, GameBuilder

class TestParseOrder(unittest.TestCase):
    def test_move_order(self):
        g = GameBuilder()
        b = g.bb

        f_black_sea = b.fleet("Black Sea", b.russia)
        a_sevastopol = b.army("Sevastopol", b.russia)
        a_armenia = b.army("Armenia", b.russia)
        f_rumania = b.fleet("Rumania", b.russia)
        a_moscow = b.army("Moscow", b.russia)
        p_ankara = b.board.get_province("Ankara")
        p_bulgaria = b.board.get_province("Bulgaria")
        b._save()


        order = ".order\n" + \
            "Timeline 1, Spring 1901: \n" + \
            "T1 - Spring '01:\n" + \
            "T1S01\n" + \
            "A Sevastopol - Ankara\n" + \
            "black sea convoy sevastopol to bulgaria sc\n" + \
            "Timeline 1 - Spring 1901 - \n" + \
            "armen s sEvAsToPoL to ankara\n" + \
            "f rumania s sev - bul South Coast\n" + \
            "a Moscow h"

        game = g.game
        #game.variant = BoardBuilder()

        parsed_orders = parse_order(order, b.russia, game)
        print("test_move_order")
        print(parsed_orders["messages"])
        for x in parsed_orders["messages"]:
            print(x)


        self.assertIsInstance(a_sevastopol.order, Move, "Sevastopol army order not parsed correctly")
        assert isinstance(a_sevastopol.order, Move)
        self.assertEqual(a_sevastopol.order.destination, p_ankara, "Sevastopol army move destination incorrect")

        self.assertIsInstance(f_black_sea.order, ConvoyTransport, "Black Sea fleet order not parsed correctly")
        assert isinstance(f_black_sea.order, ConvoyTransport)
        self.assertEqual(f_black_sea.order.source, a_sevastopol.province, "Black Sea fleet convoy source incorrect")
        self.assertEqual(f_black_sea.order.destination, p_bulgaria, "Black Sea fleet convoy destination incorrect")

        self.assertIsInstance(a_armenia.order, Support, "Armenia army order not parsed correctly")
        assert isinstance(a_armenia.order, Support)
        self.assertEqual(a_armenia.order.source, a_sevastopol.province, "Armenia army support source incorrect")
        self.assertEqual(a_armenia.order.destination, p_ankara, "Armenia army support destination incorrect")

        self.assertIsInstance(f_rumania.order, Support, "Rumania fleet order not parsed correctly")
        assert isinstance(f_rumania.order, Support)
        self.assertEqual(f_rumania.order.source, a_sevastopol.province, "Rumania fleet support source incorrect")
        self.assertEqual(f_rumania.order.destination, p_bulgaria, "Rumania fleet support destination incorrect")


        self.assertIsInstance(a_moscow.order, Hold, "Moscow army order not parsed correctly")

    def test_move_order_2(self):
        g = GameBuilder()
        b = g.bb

        f_black_sea = b.fleet("Black Sea", b.russia)
        a_sevastopol = b.army("Sevastopol", b.russia)
        a_armenia = b.army("Armenia", b.russia)
        f_rumania = b.fleet("Rumania", b.russia)
        a_moscow = b.army("Moscow", b.russia)
        p_ankara = b.board.get_province("Ankara")
        b._save()


        order = ".order\n" + \
            "Timeline 1: Spring 1901\n" + \
            "A Sevastopol - Ankara\n" + \
            "black sea convoy T1F01 sevastopol to ankara\n" + \
            "armen s T13F21 sEvAsToPoL to T13F01 ankara\n" + \
            "Timeline 3: Spring 1901\n" + \
            "f rumania s black sea holds\n" + \
            "Timeline 1: Spring 1903\n" + \
            "a Moscow h"

        game = g.game
        #game.variant = BoardBuilder()

        parsed_orders = parse_order(order, b.russia, game)
        #print("test_move_order")
        #print(parsed_orders["messages"])
        messages = parsed_orders["messages"][0].split("\n")
        # for x in messages:
        #     print(x)



        self.assertIsInstance(a_sevastopol.order, Move, "Sevastopol army order not parsed correctly")
        assert isinstance(a_sevastopol.order, Move)

        self.assertIsInstance(f_black_sea.order, ConvoyTransport, "Black Sea fleet order not parsed correctly")
        assert isinstance(f_black_sea.order, ConvoyTransport)

        self.assertIsInstance(a_armenia.order, Support, "Armenia army order not parsed correctly")
        assert isinstance(a_armenia.order, Support)


        #self.assertIsInstance(f_rumania.order, Support, "Rumania fleet order not parsed correctly")
        self.assertEqual(f_rumania.order, None, "Rumania fleet order should have failed")
        self.assertEqual(a_moscow.order, None, "Moscow order should have failed")
        #print("["+",\n".join(map(repr,messages))+"]")
        self.assertEqual(messages,
                         ['```ansi',
'',
'\x1b[0;32mA Sevastopol - T1sm1901 Ankara',
'\x1b[0;32mF Black Sea Convoys T1fm1901 Sevastopol - T1sm1901 Ankara',
'\x1b[0;32mA Armenia Supports T13fm1921 Sevastopol - T13fm1901 Ankara',
'\x1b[0;31mf rumania s black sea holds',
'\x1b[0;31ma Moscow h',
'```',
"`f rumania s black sea holds`: Can't order T3sm1901 Rumania because the board does not exist",
"`a Moscow h`: Can't order T1sm1903 Moscow because the board does not exist"]
                         )

    def test_build_order(self):
        g = GameBuilder()
        b = g.bb
        b.board.turn = b.board.turn.get_next_turn()
        b.board.turn = b.board.turn.get_next_turn()

        p_mar = b.board.get_province("Marseille")
        p_par = b.board.get_province("Paris")
        p_bre = b.board.get_province("Brest")
    
        order = ".order\n" + \
            "\n" + \
            "build f marsaille\n" + \
            "B A PaRiS\n" + \
            "b f bre"
            
        game = g.game
        game.variant = BoardBuilder()
        
        parsed_orders = parse_order(order, b.france, game)
        
        self.assertIsInstance(a_sevastopol.order, Move, "Sevastopol army order not parsed correctly")
        assert isinstance(a_sevastopol.order, Move)
        self.assertEqual(a_sevastopol.order.destination, p_ankara, "Sevastopol army move destination incorrect")
        
    def test_timeline_specifier(self):
        g = GameBuilder()
        b = g.bb

        order = ".order\n" + \
            "Timeline 1, Spring 1901: \n" + \
            "timeline 1 spring 01 \n" + \
            "timeline 1 spring 01 \n" + \
            "T1 - Spring '01:\n" + \
            "T 1 S 01 \n" + \
            "T1S01: \n" + \
            "t1s01\n"

        game = g.game
        #game.variant = BoardBuilder()

        parsed_orders = parse_order(order, b.russia, game)
        print("test_move_order")
        print(parsed_orders["messages"])
        for x in parsed_orders["messages"]:
            print(x)

    def test_remove_order(self):
        b = BoardBuilder()
        a_berlin = b.move(b.germany, UnitType.ARMY, "Berlin", "Kiel")

        order = ".remove order Berlin"
        parse_remove_order(order, b.germany, b.board)
        self.assertIsNone(a_berlin.order, "Order removal failed for Berlin army")
