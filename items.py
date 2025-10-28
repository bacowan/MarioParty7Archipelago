from BaseClasses import Item, ItemClassification, MultiWorld
from worlds.AutoWorld import World
from .options import MarioParty7Options


class MarioParty7Item(Item):
    game: str = "Mario Party 7"

    def __init__(self, name: str, world: World) -> None:
        super().__init__(name, item_classifications[name], item_name_to_id[name], world.player)

def create_items(world: World) -> None:
    world.multiworld.itempool.append(MarioParty7Item("10 dice block", world))

progression_items = [
    "10 dice block"
]

item_classifications = {
    **{ name: ItemClassification.progression for name in progression_items },
}

item_name_to_id = {name: address for address, name in enumerate(item_classifications, 1)}