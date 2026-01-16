from __future__ import annotations
from enum import Enum

class PhaseName(Enum):
    SPRING_MOVES = 0
    SPRING_RETREATS = 1
    FALL_MOVES = 2
    FALL_RETREATS = 3
    WINTER_BUILDS = 4

PHASE_NAMES = {
            PhaseName.SPRING_MOVES: "Spring Moves",
            PhaseName.SPRING_RETREATS: "Spring Retreats",
            PhaseName.FALL_MOVES: "Fall Moves",
            PhaseName.FALL_RETREATS: "Fall Retreats",
            PhaseName.WINTER_BUILDS: "Winter Builds"
        }

SHORT_PHASE_NAMES = {
            PhaseName.SPRING_MOVES: "sm",
            PhaseName.SPRING_RETREATS: "sr",
            PhaseName.FALL_MOVES: "fm",
            PhaseName.FALL_RETREATS: "fr",
            PhaseName.WINTER_BUILDS: "wa"
        }

class Turn:
    def __init__(self, year: int = 1642
                 ,phase: PhaseName = PhaseName.SPRING_MOVES
                 ,start_year: int = 1642
                 ,timeline:int = 1,
                 ):
        self.year: int = year
        self.phase: PhaseName = phase if phase in PhaseName else PhaseName.SPRING_MOVES
        self.timeline: int = timeline
        self.start_year: int = None #start_year
        ## TODO: update everything except __init__
    
    def __str__(self):
        if self.year < 0:
            year_str =  f"{str(1-self.year)} BCE"
        else:
            year_str = str(self.year)
        return f"Timeline {self.timeline} {PHASE_NAMES[self.phase]} {year_str}"

    def get_indexed_name(self) -> str:
        return f"{self.get_year_index()} {PHASE_NAMES[self.phase]} Timeline {self.timeline}"
    
    def get_short_name(self) -> str:
        return f"{str(self.year % 100)}{SHORT_PHASE_NAMES[self.phase]} T{self.timeline}"
        
    def get_phase(self) -> str:
        return PHASE_NAMES[self.phase]
    
    def get_short_phase(self) -> str:
        return SHORT_PHASE_NAMES[self.phase]
    
    def get_year_index(self) -> int:
        return self.year# - self.start_year # Incompatibility :)
    
    def get_next_turn(self) -> Turn:
        if self.phase == PhaseName.WINTER_BUILDS:
            return Turn(self.year + 1, PhaseName.SPRING_MOVES, self.start_year, self.timeline)
        return Turn(self.year, PhaseName(self.phase.value + 1), self.start_year, self.timeline)
    
    def get_previous_turn(self):
        if self.phase == PhaseName.SPRING_MOVES:
            return Turn(self.year - 1, PhaseName.WINTER_BUILDS, self.start_year,self.timeline)
        return Turn(self.year, PhaseName(self.phase.value - 1), self.start_year,self.timeline)

    def is_moves(self) -> bool:
        return "Moves" in PHASE_NAMES[self.phase]
        
    def is_retreats(self) -> bool:
        return "Retreats" in PHASE_NAMES[self.phase]
        
    def is_builds(self) -> bool:
        return "Builds" in PHASE_NAMES[self.phase]
        
    def is_fall(self) -> bool:
        return "Fall" in PHASE_NAMES[self.phase]

    def __eq__(self,other) -> bool:
        if not isinstance(other,Turn):
            return NotImplemented
        #if other.start_year != self.start_year:
        #    raise Exception("Comparing Turns with different start years")
        return other.timeline == self.timeline and other.year == self.year and other.phase == self.phase

    @staticmethod
    def turn_from_string(turn_str: str) -> Turn | None:
        split_index = turn_str.index(" ")
        year = int(turn_str[:split_index])
        phase_name = turn_str[split_index:].strip()
        for ph,n in PHASE_NAMES.items():
            if phase_name.startswith(n):
                phase = ph
                timeline_str = phase_name[len(n):].strip()
                break
        else:
            return None
        timeline_strs = timeline_str.split()
        if len(timeline_strs)!=2 or timeline_strs[0]!="Timeline":
            return None
        return Turn(year=year,phase=phase,timeline=int(timeline_strs[1]))
"""
All instances of  Turn constructor 'Turn(' outside tests have been checked
"""
