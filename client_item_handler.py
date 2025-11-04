import dolphin_memory_engine

from NetUtils import NetworkItem
from worlds.mp7 import item_name_to_id

RAM_LOCATION_MAX_DICE_BLOCK = 0x81720000

async def handle_item(network_item: NetworkItem) -> None:
    item_handlers[network_item.item]()

def ten_dice_block():
    # value of 0 means only 1 can be rolled. 1 means default behaviour.
    dolphin_memory_engine.write_byte(RAM_LOCATION_MAX_DICE_BLOCK, 1)

item_handlers = {
    item_name_to_id["10 dice block"]: ten_dice_block
}