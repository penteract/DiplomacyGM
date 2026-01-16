import unittest

from DiploGM.models.board import Board
from DiploGM.manager import Manager

from DiploGM.models.unit import UnitType
from test.utils import BoardBuilder

class TestMaps(unittest.TestCase):        
    def test_1(self):
        print("<h1>TEST 1</h1>")
        b = BoardBuilder()

        b.output()       

    def test_2(self):
        print("<h1>TEST 2</h1>")
        b = BoardBuilder()

        b.build(b.germany, (UnitType.FLEET, "Kiel"))
        b.build(b.germany, (UnitType.ARMY, "Mun"))
        b.builds_adjudicate(self)
        b.output()

        f_kiel = b.move(b.germany, UnitType.FLEET, "Kiel", "Berlin")
        b.supportMove(b.germany, UnitType.ARMY, "Munich", f_kiel, "Berlin")
        b.output()

        b.moves_adjudicate(self)
        b.output()
