from typing import Callable

import dolphin_memory_engine

from worlds.mp7.data import RAM_LOCATION_GRAND_CANAL_BEATEN_FLAG, RAM_LOCATION_PAGODA_PEAK_BEATEN_FLAG, \
    RAM_LOCATION_PYRAMID_PARK_BEATEN_FLAG, RAM_LOCATION_WINDMILLVILLE_BEATEN_FLAG, \
    RAM_LOCATION_NEON_HEIGHTS_BEATEN_FLAG, RAM_LOCATION_BOWSERS_ENCHANTED_INFERNO_BEATEN_FLAG, RAM_LOCATION_P1_INFO, \
    RAM_LOCATION_P2_INFO, COIN_OFFSET_FROM_PLAYER_LOCATION


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
        coin_count = int.from_bytes(dolphin_memory_engine.read_word(coin_offset), byteorder='big')
        return coin_count >= target_coin_count
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
}