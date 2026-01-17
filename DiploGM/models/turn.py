from __future__ import annotations
from enum import Enum

class PhaseName(Enum):
    SPRING_MOVES = 0
    SPRING_RETREATS = 1
    FALL_MOVES = 2
    FALL_RETREATS = 3
    WINTER_BUILDS = 4
    
    def is_moves(self) -> bool:
        return self in [PhaseName.SPRING_MOVES, PhaseName.FALL_MOVES]
        
    def is_retreats(self) -> bool:
        return self in [PhaseName.SPRING_RETREATS, PhaseName.FALL_RETREATS]
        
    def is_builds(self) -> bool:
        return self == PhaseName.WINTER_BUILDS
    
    #TODO: This function dupes some code `Turn` below, consider which approach makes more sense
    def to_string(self, short: bool, move_type: bool) -> str:
        name = str(self._name_).split("_")
        
        if not move_type:
            name = name[0] 
        else:
            name = " ".join(name)
            
        name = name.title()

        if short:
            name = "".join(x[0] for x in name.split()).lower()
            
        return name

    def __str__(self) -> str:
        return self.to_string(short=False, move_type=True)

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
        
    def __str__(self) -> str:
        return self.to_string(short=False, move_type=True)
    
    def to_string(self, short, move_type):
        if self.year < 0:
            year_str =  f"{str(1-self.year)} BCE"
        else:
            year_str = str(self.year)
        return f"Timeline {self.timeline} {self.phase.to_string(short=short, move_type=move_type)} {year_str}"

    def get_indexed_name(self) -> str:
        return f"{self.get_year_index()} {self.phase} Timeline {self.timeline}"
    
    def get_short_name(self) -> str:
        return f"{str(self.year % 100)}{self.phase} T{self.timeline}"
        
    def get_phase(self) -> str:
        return str(self.phase)
    
    def get_short_phase(self) -> str:
        return str(self.phase)
    
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
        return self.phase.is_moves()
        
    def is_retreats(self) -> bool:
        return self.phase.is_retreats()
        
    def is_builds(self) -> bool:
        return self.phase.is_builds()
        
    def is_fall(self) -> bool:
        return "Fall" in str(self.phase)

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
        m = zip(PhaseName.__members__.values(), map(lambda x: x.to_string(short=False, move_type=True), PhaseName._member_map_.values()))
        m = list(m)
        print(m)
        for ph,n in m:
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
