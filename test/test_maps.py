import unittest

from DiploGM.models.board import Board
from DiploGM.manager import Manager

from DiploGM.models.unit import UnitType
from test.utils import BoardBuilder

from test.utils import title

class TestMaps(unittest.TestCase):
    def test_1_create_board(self):
        title("CREATE BOARD")
        
        b = BoardBuilder()
        b.output()       

    def test_2_basic_moves(self):
        title("BASIC MOVES")
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
        b.move(b.germany, UnitType.ARMY, "Mun", "Tyrolia")
        b.output()

    def test_2_full_game(self):
        title("FULL GAME")
        b=BoardBuilder(empty = False)

        b.move(b.austria, UnitType.ARMY, "Bud", "Ser")
        b.move(b.austria, UnitType.ARMY, "Vie", "Gal")
        b.move(b.austria, UnitType.FLEET, "Tri", "Alb")

        b.move(b.england, UnitType.ARMY, "Lvp", "Yor")
        b.move(b.england, UnitType.FLEET, "Edi", "NTH")
        b.move(b.england, UnitType.FLEET, "Lon", "ENG")

        b.move(b.france, UnitType.ARMY, "Mar", "Spa")
        b.move(b.france, UnitType.ARMY, "Par", "Bur")
        b.move(b.france, UnitType.FLEET, "Bre", "MAO")

        b.move(b.germany, UnitType.ARMY, "Ber", "Kie")
        b.move(b.germany, UnitType.ARMY, "Mun", "Ruh")
        b.move(b.germany, UnitType.FLEET, "Kie", "Den")

        b.move(b.italy, UnitType.ARMY, "Rom", "Apu")
        b.hold(b.italy, UnitType.ARMY, "Ven")
        b.move(b.italy, UnitType.FLEET, "Nap", "ION")

        b.move(b.russia, UnitType.ARMY, "Mos", "Ukr")
        b.move(b.russia, UnitType.ARMY, "War", "Vie")
        b.move(b.russia, UnitType.FLEET, "Sev", "BLA")
        b.move(b.russia, UnitType.FLEET, "St. Petersburg sc", "BOT") # bug in `get_province_and_coast`

        b.move(b.turkey, UnitType.ARMY, "Con", "Bul")
        b.move(b.turkey, UnitType.ARMY, "Smy", "Con")
        b.move(b.turkey, UnitType.FLEET, "Ank", "BLA")

        b.output()
        b.moves_adjudicate(self)

        b.move(b.austria, UnitType.ARMY, "Vie", "Tri")
        f_alb = b.move(b.austria, UnitType.FLEET, "Alb", "Gre")
        b.supportMove(b.austria, UnitType.ARMY, "Ser", f_alb, "Gre")

        a_yor = b.move(b.england, UnitType.ARMY, "Yor", "Nwy")
        b.move(b.england, UnitType.FLEET, "ENG", "Bre")
        b.convoy(b.england, "NTH", a_yor, "Nwy")

        b.move(b.france, UnitType.ARMY, "Bur", "Bel")
        b.hold(b.france, UnitType.ARMY, "Spa")
        b.move(b.france, UnitType.FLEET, "MAO", "Por")

        b.move(b.germany, UnitType.ARMY, "Kie", "Hol")
        b.move(b.germany, UnitType.ARMY, "Ruh", "Mun")
        b.move(b.germany, UnitType.FLEET, "Den", "Swe")

        b.hold(b.italy, UnitType.ARMY, "Apu")
        b.move(b.italy, UnitType.ARMY, "Ven", "Tri")
        b.move(b.italy, UnitType.FLEET, "ION", "AEG")

        b.move(b.russia, UnitType.ARMY, "War", "Gal")
        b.move(b.russia, UnitType.FLEET, "BOT", "Swe")
        f_sev = b.move(b.russia, UnitType.FLEET, "Sev", "Rum")
        b.supportMove(b.russia, UnitType.ARMY, "Ukr", f_sev, "Rum")

        b.move(b.turkey, UnitType.ARMY, "Bul", "Gre")
        b.move(b.turkey, UnitType.ARMY, "Con", "Bul")
        b.move(b.turkey, UnitType.FLEET, "Ank", "BLA")

        b.output()
        b.moves_adjudicate(self)

        b.build(b.austria, (UnitType.ARMY, "Bud"), (UnitType.ARMY, "Tri"))
        b.build(b.england, (UnitType.ARMY, "Edi"), (UnitType.FLEET, "Lon"))
        b.build(b.france, (UnitType.ARMY, "Par"), (UnitType.FLEET, "Mar"))
        b.build(b.germany, (UnitType.ARMY, "Ber"), (UnitType.FLEET, "Kie"))
        # No builds for Italy
        b.build(b.russia, (UnitType.ARMY, "StP"))
        b.build(b.turkey, (UnitType.FLEET, "Smy"))

        b.builds_adjudicate(self)
        b.output()
