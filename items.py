from BaseClasses import Item, ItemClassification, MultiWorld
from worlds.AutoWorld import World
from .options import MarioParty7Options


class MarioParty7Item(Item):
    game: str = "Mario Party 7"

    def __init__(self, name: str, world: World) -> None:
        super().__init__(name, item_classifications[name], item_name_to_id[name], world.player)

def create_items(world: World) -> None:
    world.multiworld.itempool.append(MarioParty7Item("Progressive Dice Block", world))

progression_items = [
    "Progressive Dice Block",
    "Progressive Wallet",
    "Shop Menu Navigation",
    "Star Purchase Menu Navigation",
    "Board Event Menu Navigation",
    "Minigame Jump",
    "Minigame Run",
    "Minigame Mash"
]

useful_items = [
    "Progressive Capsule Capacity"
]

filler_items = [
    "1 Coin",
    "5 Coins",
    "10 Coins",
    "Random Capsule"
]

item_classifications = {
    **{ name: ItemClassification.progression for name in progression_items },
    **{ name: ItemClassification.useful for name in useful_items },
    **{ name: ItemClassification.filler for name in filler_items }
}

item_name_to_id = {name: address for address, name in enumerate(item_classifications, 1)}