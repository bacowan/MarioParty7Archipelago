from typing import Dict, Any

import dolphin_memory_engine

from NetUtils import NetworkItem
from worlds.mp7 import item_name_to_id
from worlds.mp7.data import RAM_LOCATION_MAX_DICE_BLOCK, RAM_LOCATION_MAX_WALLET, RAM_LOCATION_MAX_CAPSULES
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

item_handlers = {
    item_name_to_id["Progressive Dice Block"]: progressive_dice_block,
    item_name_to_id["Progressive Wallet"]: progressive_wallet,
    item_name_to_id["Progressive Capsule Capacity"]: progressive_capsule_capacity,
    item_name_to_id["Minigame Jump"]: minigame_jump
}