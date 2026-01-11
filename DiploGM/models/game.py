from typing import Dict, Optional, TYPE_CHECKING

from DiploGM.models.board import Board
from DiploGM.models.turn import Turn

class Game():
  def __init__(self, boards:list[tuple[Turn,Board]]):
    self._boards = {(t.timeline,t.phase,t.year) : b for (t,b) in boards}
    mx = max(t[0].timeline for t in boards)
    allboards = [[] for x in range(mx)]
    #boards.sort(key=lambda tb: (tb[0].year,tb[0] )
    for (t,b) in boards:
      allboards[t.timeline-1].append(t)
    for r in allboards:
      r.sort(key=lambda t: (t.year,t.phase))
    self._all_boards = allboards
  def get_board(self, t:Turn) -> Board:
    # TODO: think about
    return self._boards[t.timeline,t.phase,t.year]
  def all_boards(self) -> list[list[Turn]]:
    return self._all_boards
