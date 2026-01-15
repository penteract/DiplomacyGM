import unittest

from DiploGM.models.board import Board
from DiploGM.manager import Manager

from DiploGM.models.unit import UnitType
from test.utils import BoardBuilder

class TestMaps(unittest.TestCase):
    def test_maps_1(self):
        b = BoardBuilder()

        print(b.manager.draw_map(0)[0].decode("utf-8"))
        
        # a_rumania = b.core(b.germany, UnitType.ARMY, "Rumania")
        # p_rumania = b.board.get_province("Rumania")

        # b.assertIllegal(a_rumania)
        # b.moves_adjudicate(self)
        # self.assertFalse(p_rumania.half_core == b.germany, "Rumania shouldn't be cored")
        pass
