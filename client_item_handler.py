from typing import Dict, Any

import dolphin_memory_engine

from NetUtils import NetworkItem
from worlds.mp7 import item_name_to_id
from worlds.mp7.items import wallet_sizes, dice_sizes
from worlds.mp7.options import WalletProgression, CapsuleCapacityProgression
import bisect

RAM_LOCATION_MAX_DICE_BLOCK = 0x81720000
RAM_LOCATION_MAX_WALLET = 0x81720001
RAM_LOCATION_MAX_CAPSULES = 0x81720003

def handle_item(network_item: NetworkItem, slot_info: Dict[str, Any]) -> None:
    item_handlers[network_item.item](slot_info)

def ten_dice_block(slot_info: Dict[str, Any]) -> None:
    # 0 means only 1 can be rolled, 1 is 2, 2 is 5, and 3 is any
    if slot_info.get("dice_block_progression") == False:
        dolphin_memory_engine.write_byte(RAM_LOCATION_MAX_DICE_BLOCK, 3)
    else:
        current_value = dolphin_memory_engine.read_byte(RAM_LOCATION_MAX_DICE_BLOCK)
        if current_value < len(dice_sizes) - 1:
            dolphin_memory_engine.write_byte(RAM_LOCATION_MAX_DICE_BLOCK, current_value + 1)

def progressive_wallet(slot_info: Dict[str, Any]) -> None:
    progressive_wallet_option = slot_info.get("progressive_wallet")
    if progressive_wallet_option == WalletProgression.option_off:
        dolphin_memory_engine.write_word(RAM_LOCATION_MAX_WALLET, 999)
    else:
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
    if slot_info.get("capsule_capacity_progression") == False:
        dolphin_memory_engine.write_word(RAM_LOCATION_MAX_CAPSULES, 3)
    else:
        current_capsule_capacity = dolphin_memory_engine.read_byte(RAM_LOCATION_MAX_CAPSULES)
        if current_capsule_capacity < 3:
            dolphin_memory_engine.write_byte(RAM_LOCATION_MAX_CAPSULES, current_capsule_capacity + 1)

item_handlers = {
    item_name_to_id["10 dice block"]: ten_dice_block,
    item_name_to_id["Progressive Wallet"]: progressive_wallet,
    item_name_to_id["Progressive Capsule Capacity"]: progressive_capsule_capacity
}