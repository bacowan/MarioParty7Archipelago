import random
from typing import Dict, Any, Callable

import dolphin_memory_engine

from NetUtils import NetworkItem
from worlds.mp7 import item_name_to_id
from worlds.mp7.data import RAM_LOCATION_MAX_DICE_BLOCK, RAM_LOCATION_MAX_WALLET, RAM_LOCATION_MAX_CAPSULES, \
    GRAND_CANAL_UNLOCK_OFFSET, PAGODA_PEAK_UNLOCK_OFFSET, PYRAMID_PARK_UNLOCK_OFFSET, WINDMILLVILLE_UNLOCK_OFFSET, \
    NEON_HEIGHTS_UNLOCK_OFFSET, BOWSERS_ENCHANTED_INFERNO_UNLOCK_OFFSET, RAM_LOCATION_P1_INFO, RAM_LOCATION_P2_INFO, \
    CAPSULE_OFFSET_FROM_PLAYER_LOCATION, COIN_OFFSET_FROM_PLAYER_LOCATION, CAPSULE_IDS
from worlds.mp7.items import wallet_sizes, dice_sizes
from worlds.mp7.options import WalletProgression
import bisect


def handle_item(network_item: NetworkItem, slot_info: Dict[str, Any]) -> None:
    item_handlers[network_item.item](slot_info)

def progressive_dice_block(slot_info: Dict[str, Any]) -> None:
    if slot_info.get("dice_block_progression"):
        # 0 means only 1 can be rolled, 1 is 2, 2 is 5, and 3 is any
        current_value = dolphin_memory_engine.read_byte(RAM_LOCATION_MAX_DICE_BLOCK)
        if current_value < len(dice_sizes) - 1:
            dolphin_memory_engine.write_byte(RAM_LOCATION_MAX_DICE_BLOCK, current_value + 1)

def progressive_wallet(slot_info: Dict[str, Any]) -> None:
    progressive_wallet_option = slot_info.get("progressive_wallet")
    if progressive_wallet_option != WalletProgression.option_off:
        current_value = dolphin_memory_engine.read_word(RAM_LOCATION_MAX_WALLET)
        if progressive_wallet_option == WalletProgression.option_easy:
            wallets = wallet_sizes.get("easy")
        elif progressive_wallet_option == WalletProgression.option_medium:
            wallets = wallet_sizes.get("medium")
        else:
            wallets = wallet_sizes.get("hard")
        current_wallet_size_index = bisect.bisect_left(wallets, current_value)
        if current_wallet_size_index < len(wallets) - 1:
            dolphin_memory_engine.write_word(RAM_LOCATION_MAX_WALLET, wallets[current_wallet_size_index + 1])

def progressive_capsule_capacity(slot_info: Dict[str, Any]) -> None:
    if slot_info.get("capsule_capacity_progression"):
        current_capsule_capacity = dolphin_memory_engine.read_byte(RAM_LOCATION_MAX_CAPSULES)
        if current_capsule_capacity < 3:
            dolphin_memory_engine.write_byte(RAM_LOCATION_MAX_CAPSULES, current_capsule_capacity + 1)

def minigame_jump(slot_info: Dict[str, Any]) -> None:
    if slot_info.get("minigame_sanity"):
        pass

def stage_key(save_offset: int) -> Callable[[dict[str, Any]], None]:
    def func(slot_info: Dict[str, Any]) -> None:
        dolphin_memory_engine.write_byte(save_offset, 3)
    return func

def coins(amount: int) -> Callable[[dict[str, Any]], None]:
    def func(slot_info: Dict[str, Any]) -> None:
        # find the human player
        p1_difficulty = dolphin_memory_engine.read_byte(RAM_LOCATION_P1_INFO)
        if p1_difficulty >> 4 == 1:
            coin_count_location = RAM_LOCATION_P1_INFO + COIN_OFFSET_FROM_PLAYER_LOCATION
        else:
            p2_difficulty = dolphin_memory_engine.read_byte(RAM_LOCATION_P2_INFO)
            if p2_difficulty >> 4 == 1:
                coin_count_location = RAM_LOCATION_P2_INFO + COIN_OFFSET_FROM_PLAYER_LOCATION
            else:
                return

        current_coins = dolphin_memory_engine.read_word(coin_count_location)
        max_wallet = dolphin_memory_engine.read_word(RAM_LOCATION_MAX_WALLET)
        new_coins = min(current_coins + amount, max_wallet)
        if new_coins > current_coins:
            dolphin_memory_engine.write_word(coin_count_location, new_coins)


    return func

def random_capsule(slot_info: Dict[str, Any]) -> None:
    # find the human player
    p1_difficulty = dolphin_memory_engine.read_byte(RAM_LOCATION_P1_INFO)
    if p1_difficulty >> 4 == 1:
        base_capsule_location = RAM_LOCATION_P1_INFO + CAPSULE_OFFSET_FROM_PLAYER_LOCATION
    else:
        p2_difficulty = dolphin_memory_engine.read_byte(RAM_LOCATION_P2_INFO)
        if p2_difficulty >> 4 == 1:
            base_capsule_location = RAM_LOCATION_P2_INFO + CAPSULE_OFFSET_FROM_PLAYER_LOCATION
        else:
            return

    blank_capsule_locations = []
    for i in range(3):
        memory_location = base_capsule_location + i
        capsule = dolphin_memory_engine.read_byte(memory_location)
        if capsule != 0xFF:
            blank_capsule_locations.append(memory_location)

    max_capsules = dolphin_memory_engine.read_byte(RAM_LOCATION_MAX_CAPSULES)
    if 3 - len(blank_capsule_locations) < max_capsules:
        dolphin_memory_engine.write_byte(blank_capsule_locations[0], random.choice(CAPSULE_IDS))


item_handlers = {
    item_name_to_id["Progressive Dice Block"]: progressive_dice_block,
    item_name_to_id["Progressive Wallet"]: progressive_wallet,
    item_name_to_id["Progressive Capsule Capacity"]: progressive_capsule_capacity,
    item_name_to_id["Minigame Jump"]: minigame_jump,
    item_name_to_id["Grand Canal Key"]: stage_key(GRAND_CANAL_UNLOCK_OFFSET),
    item_name_to_id["Pagoda Peak Key"]: stage_key(PAGODA_PEAK_UNLOCK_OFFSET),
    item_name_to_id["Pyramid Park Key"]: stage_key(PYRAMID_PARK_UNLOCK_OFFSET),
    item_name_to_id["Windmillville Key"]: stage_key(WINDMILLVILLE_UNLOCK_OFFSET),
    item_name_to_id["Neon Heights Key"]: stage_key(NEON_HEIGHTS_UNLOCK_OFFSET),
    item_name_to_id["Bowser's Enchanted Inferno Key"]: stage_key(BOWSERS_ENCHANTED_INFERNO_UNLOCK_OFFSET),
    item_name_to_id["1 Coin"]: coins(1),
    item_name_to_id["5 Coin"]: coins(5),
    item_name_to_id["10 Coin"]: coins(10),
    item_name_to_id["Random Capsule"]: random_capsule,
}