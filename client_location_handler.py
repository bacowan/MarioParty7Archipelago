from typing import Callable

import dolphin_memory_engine

from worlds.mp7.data import RAM_LOCATION_GRAND_CANAL_BEATEN_FLAG, RAM_LOCATION_PAGODA_PEAK_BEATEN_FLAG, \
    RAM_LOCATION_PYRAMID_PARK_BEATEN_FLAG, RAM_LOCATION_WINDMILLVILLE_BEATEN_FLAG, \
    RAM_LOCATION_NEON_HEIGHTS_BEATEN_FLAG, RAM_LOCATION_BOWSERS_ENCHANTED_INFERNO_BEATEN_FLAG


def board_beaten(flag_location: int) -> Callable[[], bool]:
    def func() -> bool:
        return dolphin_memory_engine.read_byte(flag_location) == 1
    return func

location_handlers = {
    "Grand Canal Beaten": board_beaten(RAM_LOCATION_GRAND_CANAL_BEATEN_FLAG),
    "Pagoda Peak Beaten": board_beaten(RAM_LOCATION_PAGODA_PEAK_BEATEN_FLAG),
    "Pyramid Park Beaten": board_beaten(RAM_LOCATION_PYRAMID_PARK_BEATEN_FLAG),
    "Neon Heights Beaten": board_beaten(RAM_LOCATION_WINDMILLVILLE_BEATEN_FLAG),
    "Windmillville Beaten": board_beaten(RAM_LOCATION_NEON_HEIGHTS_BEATEN_FLAG),
    "Bowser's Enchanted Inferno Beaten": board_beaten(RAM_LOCATION_BOWSERS_ENCHANTED_INFERNO_BEATEN_FLAG)
}