from typing import Dict, Optional, TYPE_CHECKING
import re
from DiploGM.models.board import Board, FakeBoard
from DiploGM.models.turn import Turn, PhaseName
from itertools import chain


if TYPE_CHECKING:
    from DiploGM.models.turn import Turn

from DiploGM.models.province import Province
from collections.abc import Iterator



"""def loose_chain(a,b):
    if LOOSE_ADJACENCIES:
        return chain(a,b)
    else:
        return a
"""
number_re = re.compile("[0-9]+")
def prev_move_board(turn: Turn) -> Turn:
    if turn.phase == PhaseName.SPRING_MOVES:
        return Turn(phase=PhaseName.FALL_MOVES, year=turn.year-1, timeline=turn.timeline, start_year=turn.start_year)
    if turn.phase == PhaseName.FALL_MOVES:
        return Turn(phase=PhaseName.SPRING_MOVES, year=turn.year, timeline=turn.timeline, start_year=turn.start_year)

def next_move_board(turn: Turn) -> Turn:
    if turn.phase == PhaseName.SPRING_MOVES:
        return Turn(phase=PhaseName.FALL_MOVES, year=turn.year, timeline=turn.timeline, start_year=turn.start_year)
    if turn.phase == PhaseName.FALL_MOVES:
        return Turn(phase=PhaseName.SPRING_MOVES, year=turn.year+1, timeline=turn.timeline, start_year=turn.start_year)

def get_turn(s: str, start_year: int):
    assert s.startswith("T")
    n = number_re.match(s[1:]).group()
    s=s[1+len(n):]
    tl = int(n)
    phase=None

    #Reverse because some start with the same character. sorting by decreasing length would also work and would be more stable
    for k in reversed(PhaseName.__members__.values()):
        pn = k.to_string(short=True,move_type=0.5)
        if s.startswith(pn):
            phase=k
            s=s[len(pn):]
    n = number_re.match(s).group()
    s=s[len(n):]
    year = int(n)
    return (Turn(year=year, phase=phase, timeline=tl, start_year=start_year),s)

def get_retreat_turn(s: str, start_year: int):
    assert s.startswith("T")
    n = number_re.match(s[1:]).group()
    s=s[1+len(n):]
    tl = int(n)
    phase=None

    #PhaseName._member_names_.zip()
    for k in [PhaseName.SPRING_RETREATS,PhaseName.FALL_RETREATS]:
        if s[:2].lower() == k.to_string(short=True,move_type=0.5):
            phase=k
            s=s[2:]
            break
    else:
        raise Exception("Could not read phase from "+repr(s))
    n = number_re.match(s).group()
    s=s[len(n):]
    year = int(n)
    return (Turn(year=year, phase=phase, timeline=tl, start_year=start_year),s)


class Game():
    def __init__(self, variant: Board, boards : list[tuple[Turn,Board]]):
        variant.units.clear() # a single 2D board for finding adjacencies
        self.variant = variant
        self._boards : dict[(int, PhaseName, int)] = {(t.timeline,t.phase,t.year) : b for (t,b) in boards}
        mx = max(t[0].timeline for t in boards)
        allTurns = [[] for x in range(mx)]
        #boards.sort(key=lambda tb: (tb[0].year,tb[0] )
        for (t,b) in boards:
            assert t == b.turn
            allTurns[t.timeline-1].append(t)
        for r in allTurns:
            r.sort(key=lambda t: (t.year,t.phase.value))
        self._all_turns = allTurns

        default_board = self.get_board(allTurns[0][0])
        self.data = default_board.data # be nice for manager.create_game; TODO: this may sometimes need to change
        self.board_id = default_board.board_id
        self.start_year = default_board.turn.start_year

    def add_adjacencies(self,LOOSE_ADJACENCIES: bool=True):
        # vp = self.variant.name_to_province["nao3"]
        # print (vp.adjacent)
        if LOOSE_ADJACENCIES:
            loose_chain = chain
        else:
            def loose_chain(a,b):
                return a
        #add 5D adjacencies
        for board in self._boards.values():
            t = board.turn
            if t.phase == PhaseName.SPRING_MOVES or t.phase == PhaseName.FALL_MOVES:
                for t in [prev_move_board(t),
                            next_move_board(t),
                            Turn(phase=t.phase, year=t.year, timeline=t.timeline+1, start_year=t.start_year),
                            Turn(phase=t.phase, year=t.year, timeline=t.timeline-1, start_year=t.start_year)
                            ]:
                    if (t.timeline,t.phase,t.year) not in self._boards:
                        continue
                    other_board = self.get_board(t)
                    for p in board.provinces:
                        n = p.name.lower()
                        vp = self.variant.name_to_province[n]
                        for ap in loose_chain([vp],vp.adjacent):
                            p.adjacent.add(other_board.name_to_province[ap.name.lower()])
                        vpfa = vp.fleet_adjacent
                        if isinstance(vpfa,dict):
                            #vpfa = {None:vpfa}
                            for coast,adjs in vpfa.items():
                                pfac = p.fleet_adjacent[coast]
                                for (ap, acoast) in loose_chain([(vp,coast)], adjs):
                                    pfac.add((other_board.name_to_province[ap.name.lower()] ,acoast))
                        else:
                            for (ap, acoast) in loose_chain([(vp,None)], vpfa):
                                p.fleet_adjacent.add((other_board.name_to_province[ap.name.lower()] ,acoast))
                        # Province.adjacent: set[Province]
                        # Province.fleet_adjacent: set[tuple[Province, str | None]] | dict[str, set[tuple[Province, str | None]]]
    def get_turn_province_and_coast(self, prov:str):
        t,p = get_turn(prov,self.start_year)
        p = self.get_board(t).get_province_and_coast(p.strip())
        # assert not p[0].isFake
        return p
    def get_turn_and_province(self, prov:str):
        t,p = get_turn(prov,self.start_year)
        p = self.get_board(t).get_province(p.strip())
        # assert not p.isFake
        return p
    def get_board(self, t:Turn) -> Board | FakeBoard:
        # TODO: think about returning boards full of fake provinces when t has no associated board
        tdata = (t.timeline,t.phase,t.year)
        if tdata in self._boards:
            #return self._boards[tdata]#!!!!!!
            return self._boards[tdata]
        else:
            # return self.get_board(self.all_turns()[0][0])
            return FakeBoard(self.variant,t) # TODO: Modify so that provinces include turn information
        #return self._boards[t.timeline,t.phase,t.year]
    def all_turns(self) -> list[list[Turn]]:
        return self._all_turns

    def is_retreats(self) -> bool:
        print("\x1b[31mFunction Game.is_retreats() is not implemented; returning True\x1b[0m")
        return True

    def get_moves_boards(self) -> Iterator[Board]:
        for timeline in self._all_turns:
            for turn in timeline:
                if turn.is_moves():
                    yield self.get_board(turn)
    def get_moves_provinces(self) -> Iterator[Province]:
        for board in self.get_moves_boards():
            for p in board.provinces:
                yield p
    def get_moves_units(self) -> Iterator[Province]:
        for board in self.get_moves_boards():
            for u in board.units:
                yield u

    def get_current_retreat_boards(self) -> Iterator[Board]:
        for timeline in self._all_turns:
            if timeline[-1].is_retreats():
                    yield self.get_board(timeline[-1])

    def can_skip_retreats(self):
        """There are retreats boards but no units that need to retreat """
        no_boards = True
        for board in self.get_current_retreat_boards():
            no_boards = False
            for province in board.provinces:
                if province.dislodged_unit:
                    return False
        else:
            return not no_boards
