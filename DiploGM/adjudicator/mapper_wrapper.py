from xml.etree.ElementTree import Element
from xml.etree.ElementTree import tostring as elementToString

from DiploGM.adjudicator.mapper import Mapper
from DiploGM.models.board import Board
from DiploGM.models.game import Game
from DiploGM.models.player import Player
from DiploGM.models.turn import Turn

BOARD_PADDING: tuple[int, int] = [25, 25]

class MapperWrapper:
    def __init__(self, game: Game, restriction: Player | None = None, color_mode: str | None = None):
        self.game = Game
        self.player_restriction: Player | None = None
        self.color_mode = color_mode
        
        self.board_svgs: dict[Turn, Element[str]]= {}
    
    # Draws a map with currently-submitted orders
    def draw_moves_map(self):
        turns = self.game.all_turns()
        for board in [self.game.get_board(t) for t in turns]:
            board: Board = board
            element, _ = Mapper(board, self.player_restriction).draw_moves_map(board.turn, self.player_restriction)
            self.board_svgs[board.turn, element]
            
        
        for turn, element in self.board_svgs:
            if turn.is_retreats():
                pass      
            group = Element(tag="g").extend(element)
            elementToString(group)
                
                

    def draw_current_map():
        pass