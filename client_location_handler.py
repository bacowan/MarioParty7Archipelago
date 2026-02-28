from typing import Callable, List

import dolphin_memory_engine

from worlds.mp7.data import RAM_LOCATION_GRAND_CANAL_BEATEN_FLAG, RAM_LOCATION_PAGODA_PEAK_BEATEN_FLAG, \
    RAM_LOCATION_PYRAMID_PARK_BEATEN_FLAG, RAM_LOCATION_WINDMILLVILLE_BEATEN_FLAG, \
    RAM_LOCATION_NEON_HEIGHTS_BEATEN_FLAG, RAM_LOCATION_BOWSERS_ENCHANTED_INFERNO_BEATEN_FLAG, RAM_LOCATION_P1_INFO, \
    RAM_LOCATION_P2_INFO, COIN_OFFSET_FROM_PLAYER_LOCATION, RAM_LOCATION_GRAND_CANAL_REACHED_SPACES, \
    GRAND_CANAL_SPACE_IDS, RAM_LOCATION_PAGODA_PEAK_REACHED_SPACES, RAM_LOCATION_PYRAMID_PARK_REACHED_SPACES, \
    RAM_LOCATION_WINDMILLVILLE_REACHED_SPACES, RAM_LOCATION_NEON_HEIGHTS_REACHED_SPACES, \
    RAM_LOCATION_BOWSERS_ENCHANTED_INFERNO_REACHED_SPACES, PAGODA_PEAK_SPACE_IDS, PYRAMID_PARK_SPACE_IDS, \
    WINDMILLVILLE_SPACE_IDS, NEON_HEIGHTS_SPACE_IDS, BOWSERS_ENCHANTED_INFERNO
from worlds.stardew_valley.stardew_rule import false_


def get_human_player_offset() -> int:
    player_1 = dolphin_memory_engine.read_word(RAM_LOCATION_P1_INFO)
    if player_1 & 0x20: # this bit will be set for cpus but not humans
        return RAM_LOCATION_P1_INFO
    else:
        return RAM_LOCATION_P2_INFO

def board_beaten(flag_location: int) -> Callable[[], bool]:
    def func() -> bool:
        return dolphin_memory_engine.read_byte(flag_location) == 1
    return func

def coins_in_wallet(target_coin_count: int) -> Callable[[], bool]:
    def func() -> bool:
        player_offset = get_human_player_offset()
        coin_offset = player_offset + COIN_OFFSET_FROM_PLAYER_LOCATION
        coin_count = dolphin_memory_engine.read_word(coin_offset)
        return coin_count >= target_coin_count
    return func

def unique_spaces(space_count: int) -> Callable[[], bool]:
    def as_flags(values: List[int]) -> List[int]:
        return [1 << x for x in values]

    landed_spaces_info = [
        { 'offset': RAM_LOCATION_GRAND_CANAL_REACHED_SPACES, 'spaces': as_flags(GRAND_CANAL_SPACE_IDS) },
        { 'offset': RAM_LOCATION_PAGODA_PEAK_REACHED_SPACES, 'spaces': as_flags(PAGODA_PEAK_SPACE_IDS) },
        { 'offset': RAM_LOCATION_PYRAMID_PARK_REACHED_SPACES, 'spaces': as_flags(PYRAMID_PARK_SPACE_IDS) },
        { 'offset': RAM_LOCATION_WINDMILLVILLE_REACHED_SPACES, 'spaces': as_flags(WINDMILLVILLE_SPACE_IDS) },
        { 'offset': RAM_LOCATION_NEON_HEIGHTS_REACHED_SPACES, 'spaces': as_flags(NEON_HEIGHTS_SPACE_IDS) },
        { 'offset': RAM_LOCATION_BOWSERS_ENCHANTED_INFERNO_REACHED_SPACES, 'spaces': as_flags(BOWSERS_ENCHANTED_INFERNO) },
    ]
    def func() -> bool:
        count = 0
        for data in landed_spaces_info:
            length = data['spaces'][-1] / 8
            as_bytes = dolphin_memory_engine.read_bytes(data['offset'], length)
            as_int = int.from_bytes(as_bytes, byteorder='little')
            for space in data['spaces']:
                if space & as_int > 0:
                    count += 1
        return count > space_count
    return func

location_handlers = {
    "Grand Canal Beaten": board_beaten(RAM_LOCATION_GRAND_CANAL_BEATEN_FLAG),
    "Pagoda Peak Beaten": board_beaten(RAM_LOCATION_PAGODA_PEAK_BEATEN_FLAG),
    "Pyramid Park Beaten": board_beaten(RAM_LOCATION_PYRAMID_PARK_BEATEN_FLAG),
    "Neon Heights Beaten": board_beaten(RAM_LOCATION_WINDMILLVILLE_BEATEN_FLAG),
    "Windmillville Beaten": board_beaten(RAM_LOCATION_NEON_HEIGHTS_BEATEN_FLAG),
    "Bowser's Enchanted Inferno Beaten": board_beaten(RAM_LOCATION_BOWSERS_ENCHANTED_INFERNO_BEATEN_FLAG),
    "10 Coins in Wallet": coins_in_wallet(10),
    "20 Coins in Wallet": coins_in_wallet(20),
    "30 Coins in Wallet": coins_in_wallet(30),
    "40 Coins in Wallet": coins_in_wallet(40),
    "50 Coins in Wallet": coins_in_wallet(50),
    "60 Coins in Wallet": coins_in_wallet(60),
    "70 Coins in Wallet": coins_in_wallet(70),
    "80 Coins in Wallet": coins_in_wallet(80),
    "90 Coins in Wallet": coins_in_wallet(90),
    "100 Coins in Wallet": coins_in_wallet(100),
    "150 Coins in Wallet": coins_in_wallet(150),
    "200 Coins in Wallet": coins_in_wallet(200),
    "20 Unique Spaces": unique_spaces(20),
    "40 Unique Spaces": unique_spaces(40),
    "60 Unique Spaces": unique_spaces(20),
    "80 Unique Spaces": unique_spaces(60),
    "100 Unique Spaces": unique_spaces(100),
    "120 Unique Spaces": unique_spaces(120),
    "140 Unique Spaces": unique_spaces(140),
    "160 Unique Spaces": unique_spaces(160),
    "180 Unique Spaces": unique_spaces(180),
    "200 Unique Spaces": unique_spaces(200),
    "220 Unique Spaces": unique_spaces(220),
    "240 Unique Spaces": unique_spaces(240),
    "260 Unique Spaces": unique_spaces(260),
    "280 Unique Spaces": unique_spaces(280),
    "300 Unique Spaces": unique_spaces(300)
}