import unittest

from DiploGM.models.board import Board
from DiploGM.manager import Manager

from DiploGM.models.unit import UnitType
from test.utils import BoardBuilder

class TestMaps(unittest.TestCase):        
    def test_1_create_board(self):
        print("<h1>CREATE BOARD</h1>")
        b = BoardBuilder()

        b.output()       

    def test_2_basic_moves(self):
        print("<h1>BASIC MOVES</h1>")
        b = BoardBuilder()

        b.build(b.germany, (UnitType.FLEET, "Kiel"))
        b.build(b.germany, (UnitType.ARMY, "Mun"))
        b.build(b.germany, (UnitType.ARMY, "Ber"))
        b.builds_adjudicate(self)
        b.output()

        b.move(b.germany, UnitType.ARMY, "Ber", "Pru")
        f_kiel = b.move(b.germany, UnitType.FLEET, "Kie", "Ber")
        b.supportMove(b.germany, UnitType.ARMY, "Mun", f_kiel, "Ber")
        b.output()

        b.moves_adjudicate(self)

        b.move(b.germany, UnitType.FLEET, "Ber", "BAL")
        b.move(b.germany, UnitType.ARMY, "Pru", "War")
        b.move(b.germany, UnitType.ARMY, "Mun", "Tyr")
        b.output()
