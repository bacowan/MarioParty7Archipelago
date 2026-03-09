import math
from typing import Callable, List

import dolphin_memory_engine

from worlds.mp7.data import RAM_LOCATION_GRAND_CANAL_BEATEN_FLAG, RAM_LOCATION_PAGODA_PEAK_BEATEN_FLAG, \
    RAM_LOCATION_PYRAMID_PARK_BEATEN_FLAG, RAM_LOCATION_WINDMILLVILLE_BEATEN_FLAG, \
    RAM_LOCATION_NEON_HEIGHTS_BEATEN_FLAG, RAM_LOCATION_BOWSERS_ENCHANTED_INFERNO_BEATEN_FLAG, RAM_LOCATION_P1_INFO, \
    RAM_LOCATION_P2_INFO, COIN_OFFSET_FROM_PLAYER_LOCATION, RAM_LOCATION_GRAND_CANAL_REACHED_SPACES, \
    GRAND_CANAL_SPACE_IDS, RAM_LOCATION_PAGODA_PEAK_REACHED_SPACES, RAM_LOCATION_PYRAMID_PARK_REACHED_SPACES, \
    RAM_LOCATION_WINDMILLVILLE_REACHED_SPACES, RAM_LOCATION_NEON_HEIGHTS_REACHED_SPACES, \
    RAM_LOCATION_BOWSERS_ENCHANTED_INFERNO_REACHED_SPACES, PAGODA_PEAK_SPACE_IDS, PYRAMID_PARK_SPACE_IDS, \
    WINDMILLVILLE_SPACE_IDS, NEON_HEIGHTS_SPACE_IDS, BOWSERS_ENCHANTED_INFERNO, BEATEN_MINIGAME_SAVE_ORDER, \
    RAM_LOCATION_COMPLETED_MINIGAMES, RAM_LOCATION_BOUGHT_ITEMS, SHOP_STAGE_ORDER


def get_human_player_offset() -> int:
    player_1 = dolphin_memory_engine.read_byte(RAM_LOCATION_P1_INFO)
    if player_1 & 0x10: # this bit will be set for human but not cpu
        return RAM_LOCATION_P1_INFO
    else:
        return RAM_LOCATION_P2_INFO

def board_beaten(flag_location: int) -> Callable[[], bool]:
    def func() -> bool:
        return dolphin_memory_engine.read_byte(flag_location) == 1
    return func

def minigame_beaten(minigame_name: str) -> Callable[[], bool]:
    minigame_index = BEATEN_MINIGAME_SAVE_ORDER.index(minigame_name)
    def func() -> bool:
        as_int = int.from_bytes(
            dolphin_memory_engine.read_bytes(RAM_LOCATION_COMPLETED_MINIGAMES, 2),
            byteorder='big')
        mask = 1 << minigame_index
        return as_int & mask > 0
    return func

def coins_in_wallet(target_coin_count: int) -> Callable[[], bool]:
    def func() -> bool:
        player_offset = get_human_player_offset()
        coin_offset = player_offset + COIN_OFFSET_FROM_PLAYER_LOCATION
        coin_count = int.from_bytes(dolphin_memory_engine.read_bytes(coin_offset, 2), byteorder='big')
        return coin_count >= target_coin_count
    return func

def unique_spaces(space_count: int) -> Callable[[], bool]:
    def as_flags(values: List[int]) -> List[int]:
        return [1 << x for x in values]

    def byte_count(values: List[int]) -> int:
        return math.ceil(values[-1] / 8)

    landed_spaces_info = [
        { 'offset': RAM_LOCATION_GRAND_CANAL_REACHED_SPACES, 'spaces': as_flags(GRAND_CANAL_SPACE_IDS), 'byte_count': byte_count(GRAND_CANAL_SPACE_IDS) },
        { 'offset': RAM_LOCATION_PAGODA_PEAK_REACHED_SPACES, 'spaces': as_flags(PAGODA_PEAK_SPACE_IDS), 'byte_count': byte_count(PAGODA_PEAK_SPACE_IDS) },
        { 'offset': RAM_LOCATION_PYRAMID_PARK_REACHED_SPACES, 'spaces': as_flags(PYRAMID_PARK_SPACE_IDS), 'byte_count': byte_count(PYRAMID_PARK_SPACE_IDS) },
        { 'offset': RAM_LOCATION_WINDMILLVILLE_REACHED_SPACES, 'spaces': as_flags(WINDMILLVILLE_SPACE_IDS), 'byte_count': byte_count(WINDMILLVILLE_SPACE_IDS) },
        { 'offset': RAM_LOCATION_NEON_HEIGHTS_REACHED_SPACES, 'spaces': as_flags(NEON_HEIGHTS_SPACE_IDS), 'byte_count': byte_count(NEON_HEIGHTS_SPACE_IDS) },
        { 'offset': RAM_LOCATION_BOWSERS_ENCHANTED_INFERNO_REACHED_SPACES, 'spaces': as_flags(BOWSERS_ENCHANTED_INFERNO), 'byte_count': byte_count(BOWSERS_ENCHANTED_INFERNO) },
    ]
    def func() -> bool:
        count = 0
        for data in landed_spaces_info:
            as_bytes = dolphin_memory_engine.read_bytes(data['offset'], data['byte_count'])
            as_int = int.from_bytes(as_bytes, byteorder='little')
            for space in data['spaces']:
                if space & as_int > 0:
                    count += 1
        return count > space_count
    return func

def bought_items(board_name: str, shop_index: int, item_index: int) -> Callable[[], bool]:
    bit_index = 1 << (SHOP_STAGE_ORDER.index(board_name) * 3) << item_index
    def func() -> bool:
        saved_flags = dolphin_memory_engine.read_word(RAM_LOCATION_BOUGHT_ITEMS)
        return saved_flags & bit_index > 0
    return func

location_handlers = {
    "Grand Canal Beaten": board_beaten(RAM_LOCATION_GRAND_CANAL_BEATEN_FLAG),
    "Pagoda Peak Beaten": board_beaten(RAM_LOCATION_PAGODA_PEAK_BEATEN_FLAG),
    "Pyramid Park Beaten": board_beaten(RAM_LOCATION_PYRAMID_PARK_BEATEN_FLAG),
    "Neon Heights Beaten": board_beaten(RAM_LOCATION_WINDMILLVILLE_BEATEN_FLAG),
    "Windmillville Beaten": board_beaten(RAM_LOCATION_NEON_HEIGHTS_BEATEN_FLAG),
    "Bowser's Enchanted Inferno Beaten": board_beaten(RAM_LOCATION_BOWSERS_ENCHANTED_INFERNO_BEATEN_FLAG),
    "Warp Pipe Dreams Beaten": minigame_beaten("warp pipe dreams"),
    "Weight For It Beaten": minigame_beaten("weight for it"),
    "Mad Props Beaten": minigame_beaten("mad props"),
    "Gimme a Sign Beaten": minigame_beaten("gimme a sign"),
    "Bridge Work Beaten": minigame_beaten("bridge work"),
    "Spin Doctor Beaten": minigame_beaten("spin doctor"),
    "Hip Hop Drop Beaten": minigame_beaten("hip hop drop"),
    "Royal Rumpus Beaten": minigame_beaten("royal rumpus"),
    "Light Speed Beaten": minigame_beaten("light speed"),
    "Apes of Wrath Beaten": minigame_beaten("apes of wrath"),
    "Fish And Cheeps Beaten": minigame_beaten("fish and cheeps"),
    "Camp Ukiki Beaten": minigame_beaten("camp ukiki"),
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
    "300 Unique Spaces": unique_spaces(300),
    "Grand Canal Orb Hut 1 Left Item": bought_items("Grand Canal", 0, 0),
    "Grand Canal Orb Hut 1 Middle Item": bought_items("Grand Canal", 0, 1),
    "Grand Canal Orb Hut 1 Right Item": bought_items("Grand Canal", 0, 2),
    "Grand Canal Orb Hut 2 Left Item": bought_items("Grand Canal", 1, 0),
    "Grand Canal Orb Hut 2 Middle Item": bought_items("Grand Canal", 1, 1),
    "Grand Canal Orb Hut 2 Right Item": bought_items("Grand Canal", 1, 2),
    "Pagoda Peak Orb Hut 1 Left Item": bought_items("Pagoda Peak", 0, 0),
    "Pagoda Peak Orb Hut 1 Middle Item": bought_items("Pagoda Peak", 0, 1),
    "Pagoda Peak Orb Hut 1 Right Item": bought_items("Pagoda Peak", 0, 2),
    "Pagoda Peak Orb Hut 2 Left Item": bought_items("Pagoda Peak", 1, 0),
    "Pagoda Peak Orb Hut 2 Middle Item": bought_items("Pagoda Peak", 1, 1),
    "Pagoda Peak Orb Hut 2 Right Item": bought_items("Pagoda Peak", 1, 2),
    "Neon Heights Orb Hut 1 Left Item": bought_items("Neon Heights", 0, 0),
    "Neon Heights Orb Hut 1 Middle Item": bought_items("Neon Heights", 0, 1),
    "Neon Heights Orb Hut 1 Right Item": bought_items("Neon Heights", 0, 2),
    "Neon Heights Orb Hut 2 Left Item": bought_items("Neon Heights", 1, 0),
    "Neon Heights Orb Hut 2 Middle Item": bought_items("Neon Heights", 1, 1),
    "Neon Heights Orb Hut 2 Right Item": bought_items("Neon Heights", 1, 2),
    "Windmillville Orb Hut 1 Left Item": bought_items("Windmillville", 0, 0),
    "Windmillville Orb Hut 1 Middle Item": bought_items("Windmillville", 0, 1),
    "Windmillville Orb Hut 1 Right Item": bought_items("Windmillville", 0, 2),
    "Windmillville Orb Hut 2 Left Item": bought_items("Windmillville", 1, 0),
    "Windmillville Orb Hut 2 Middle Item": bought_items("Windmillville", 1, 1),
    "Windmillville Orb Hut 2 Right Item": bought_items("Windmillville", 1, 2),
    "Pyramid Park Orb Hut 1 Left Item": bought_items("Pyramid Park", 0, 0),
    "Pyramid Park Orb Hut 1 Middle Item": bought_items("Pyramid Park", 0, 1),
    "Pyramid Park Orb Hut 1 Right Item": bought_items("Pyramid Park", 0, 2),
    "Pyramid Park Orb Hut 2 Left Item": bought_items("Pyramid Park", 1, 0),
    "Pyramid Park Orb Hut 2 Middle Item": bought_items("Pyramid Park", 1, 1),
    "Pyramid Park Orb Hut 2 Right Item": bought_items("Pyramid Park", 1, 2),
    "Bowser's Enchanted Inferno Orb Hut 1 Left Item": bought_items("Bowser's Enchanted Inferno", 0, 0),
    "Bowser's Enchanted Inferno Orb Hut 1 Middle Item": bought_items("Bowser's Enchanted Inferno", 0, 1),
    "Bowser's Enchanted Inferno Orb Hut 1 Right Item": bought_items("Bowser's Enchanted Inferno", 0, 2),
    "Bowser's Enchanted Inferno Orb Hut 2 Left Item": bought_items("Bowser's Enchanted Inferno", 1, 0),
    "Bowser's Enchanted Inferno Orb Hut 2 Middle Item": bought_items("Bowser's Enchanted Inferno", 1, 1),
    "Bowser's Enchanted Inferno Orb Hut 2 Right Item": bought_items("Bowser's Enchanted Inferno", 1, 2)
}