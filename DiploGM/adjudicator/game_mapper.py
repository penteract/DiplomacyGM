import copy
from xml.etree.ElementTree import register_namespace
from xml.etree.ElementTree import tostring as elementToString

import numpy as np
from lxml import etree
from lxml.etree import ElementTree, Element
import math

from DiploGM.map_parser.vector.utils import (
    clear_svg_element,
    get_element_color,
    get_svg_element,
    get_unit_coordinates,
    initialize_province_resident_data,
)
from DiploGM.models.turn import Turn
from DiploGM.models.board import Board
from DiploGM.models.game import Game
from DiploGM.adjudicator.mapper import Mapper
from DiploGM.db.database import logger
from DiploGM.models.order import (
    Hold,
    Core,
    ConvoyTransport,
    Support,
    RetreatMove,
    RetreatDisband,
    Build,
    Disband,
    Move,
    ConvoyMove,
    PlayerOrder,
)
from DiploGM.models.player import Player
from DiploGM.models.province import ProvinceType, Province
from DiploGM.models.unit import Unit, UnitType

from DiploGM.map_parser.vector.transform import TransGL3
from DiploGM.map_parser.vector.vector import Parser

# TODO: Move this (and vector.py's copy to a central file)
NAMESPACE: dict[str, str] = {
    "inkscape": "{http://www.inkscape.org/namespaces/inkscape}",
    "sodipodi": "http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd",
    "svg": "http://www.w3.org/2000/svg",
}
SVG_CONFIG_KEY: str = "svg config"


# OUTPUTLAYER = "layer16"
# UNITLAYER = "layer17"


# if you make any rendering changes,
# make sure to sync them with mapper.js


class GameMapper:
    def __init__(
            self,
            game: Game,
            restriction: Player | None = None,
            color_mode: str | None = None,
    ):
        register_namespace("", "http://www.w3.org/2000/svg")
        register_namespace("inkscape", "http://www.inkscape.org/namespaces/inkscape")
        register_namespace(
            "sodipodi", "http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
        )
        register_namespace("xlink", "http://www.w3.org/1999/xlink")

        self.game: Game = game
        self.game_svg: ElementTree = etree.parse(self.game.data["file"])
        self.player_restriction: Player | None = None

        # different colors
        if "color replacements" in self.game.data[SVG_CONFIG_KEY]:
            self.replacements = self.game.data[SVG_CONFIG_KEY]["color replacements"]
        else:
            self.replacements = None

        clear_svg_element(
            self.game_svg, self.game.data[SVG_CONFIG_KEY]["starting_units"]
        )

        self.cached_elements = {}
        for element_name in [
            "army",
            "fleet",
            "retreat_army",
            "retreat_fleet",
            "unit_output",
        ]:
            self.cached_elements[element_name] = get_svg_element(
                self.game_svg, self.game.data[SVG_CONFIG_KEY][element_name]
            )

        self.restriction = restriction
        # if restriction is not None:
        #     self.adjacent_provinces: set[str] = self.game.get_visible_provinces(
        #         restriction
        #     )
        # else:
        #     self.adjacent_provinces: set[str] = {
        #         province.name for province in self.game.provinces
        #     }

        self._moves_svg = copy.deepcopy(self.game_svg)
        self.cached_elements["unit_output_moves"] = get_svg_element(
            self._moves_svg, self.game.data[SVG_CONFIG_KEY]["unit_output"]
        )

        self.state_svg = copy.deepcopy(self.game_svg)

        self.color_mode = color_mode

    def draw_moves_map(self, player_restriction: Player | None, movement_only: bool = False, is_retreats: bool = True) \
            -> tuple[bytes, str]:
        root = None
        for timeline in self.game.all_turns():
            # root.append(create_element("g", {}))
            i = 0
            for turn in timeline:
                if is_retreats or not turn.is_retreats():
                    i += 1
                    svg, _ = Mapper(self.game.get_board(turn), color_mode=self.color_mode).draw_moves_map(turn,
                        player_restriction,
                        movement_only=movement_only)
                    if root is None:
                        root = svg
                    else:
                        group = create_element("g", {"transform": f"translate({1920 * i})"})
                        root.append(group)
                        for child in svg.getchildren():
                            group.append(child)
                    # print("\n", svg_element)
                    # for element in svg_element:
                    #     print("    ", element)
                    #     for new_element in element:
                    #         print("        ", new_element)
                    #     root.append(element)

        return elementToString(root), "map.svg"

def create_element(tag: str, attributes: dict[str, any]) -> etree.Element:
    attributes_str = {key: str(val) for key, val in attributes.items()}
    return etree.Element(tag, attributes_str)