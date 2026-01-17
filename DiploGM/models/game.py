from typing import Dict, Optional, TYPE_CHECKING
import re
from DiploGM.models.board import Board, FakeBoard
from DiploGM.models.turn import Turn, PhaseName
from itertools import chain

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
    if phase == PhaseName.FALL_MOVES:
        Turn(phase=PhaseName.SPRING_MOVES, year=turn.year, timeline=turn.timeline, start_year=turn.start_year)

def next_move_board(turn: Turn) -> Turn:
    if turn.phase == PhaseName.SPRING_MOVES:
        return Turn(phase=PhaseName.FALL_MOVES, year=turn.year, timeline=turn.timeline, start_year=turn.start_year)
    if phase == PhaseName.FALL_MOVES:
        Turn(phase=PhaseName.SPRING_MOVES, year=turn.year+1, timeline=turn.timeline, start_year=turn.start_year)

def get_turn(s: str, start_year: int):
    assert s.startswith("T")
    n = number_re.match(s[1:]).group()
    s=s[1+n:]
    tl = int(n)
    phase=None
    
    PhaseName._member_names_.zip()
    
    m = zip(PhaseName.__members__.values(), map(lambda x: x.to_string(short=True, move_type=True), PhaseName._member_map_.values()))
    
    for k,v in map:
        
        if s.startswith(v):
            phase=k
            s=s[len(v):]
    n = number_re.match(s).group()
    s=s[n:]
    year = int(n)
    return (Turn(year=year, phase=phase, timeline=tl, start_year=start_year),s)


class Game():
    def __init__(self, variant: Board, boards : list[tuple[Turn,Board]]):
        variant.units.clear() # a single 2D board for finding adjacencies
        self.variant = variant
        self._boards : dict[(int, PhaseName, int)] = {(t.timeline,t.phase,t.year) : b for (t,b) in boards}
        mx = max(t[0].timeline for t in boards)
        allboards = [[] for x in range(mx)]
        #boards.sort(key=lambda tb: (tb[0].year,tb[0] )
        for (t,b) in boards:
            allboards[t.timeline-1].append(t)
        for r in allboards:
            r.sort(key=lambda t: (t.year,t.phase.value))
        self._all_boards = allboards

        default_board = self.get_board(allboards[0][0])
        self.data = default_board.data # be nice for manager.create_game; TODO: this may sometimes need to change
        self.board_id = default_board.board_id
        self.start_year = default_board.turn.start_year

    def add_adjacencies(self,LOOSE_ADJACENCIES: bool=True):
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
                    if (t.timeline,t.phase,t.year) not in self._all_boards:
                        continue
                    other_board = self.get_board(t)
                    for p in board.provinces:
                        n = p.name.lower()
                        vp = variant.name_to_province[n]
                        for ap in loose_chain([vp],vp.adjacent):
                            p.adjacent.add(other_board.name_to_province[ap.name.lower()])
                        vpfa = vp.fleet_adjacent
                        if isinstance(fleets,dict):
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
        p = self.get_board(t).get_province_and_coast(p)
        assert not p.isFake
    def get_turn_and_province(self, prov:str):
        t,p = get_turn(prov,self.start_year)
        p = self.get_board(t).get_province(p)
        assert not p.isFake
        return p
    def get_board(self, t:Turn) -> Board | FakeBoard:
        # TODO: think about returning boards full of fake provinces when t has no associated board
        tdata = (t.timeline,t.phase,t.year)
        if tdata in self._boards:
            #return self._boards[tdata]#!!!!!!
            return self._boards[tdata]
        else:
            # return self.get_board(self.all_boards()[0][0])
            return FakeBoard(self.variant,t) # TODO: Modify so that provinces include turn information
        #return self._boards[t.timeline,t.phase,t.year]
    def all_boards(self) -> list[list[Turn]]:
        return self._all_boards

    def is_retreats(self) -> bool:
        return True
