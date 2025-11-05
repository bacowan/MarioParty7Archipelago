import random

from BaseClasses import Item, ItemClassification, MultiWorld
from worlds.AutoWorld import World
from .options import MarioParty7Options, WalletProgression


class MarioParty7Item(Item):
    game: str = "Mario Party 7"

    def __init__(self, name: str, player: int) -> None:
        super().__init__(name, item_classifications[name], item_name_to_id[name], player)

def create_items(world: MultiWorld, options: MarioParty7Options, player: int) -> None:
    world.itempool.append(MarioParty7Item("Grand Canal", player))
    world.itempool.append(MarioParty7Item("Pagoda Peak", player))
    world.itempool.append(MarioParty7Item("Pyramid Park", player))
    world.itempool.append(MarioParty7Item("Neon Heights", player))
    world.itempool.append(MarioParty7Item("Windmillville", player))
    world.itempool.append(MarioParty7Item("Bower's Enchanted Inferno", player))

    if options.dice_block_progression.value:
        for _ in range(4):
            world.itempool.append(MarioParty7Item("Progressive Dice Block", player))

    if options.wallet_progression.value == WalletProgression.option_easy:
        for _ in range(4):
            world.itempool.append(MarioParty7Item("Progressive Wallet", player))
    elif options.wallet_progression.value == WalletProgression.option_medium:
        for _ in range(5):
            world.itempool.append(MarioParty7Item("Progressive Wallet", player))
    elif options.wallet_progression.value == WalletProgression.option_hard:
        for _ in range(7):
            world.itempool.append(MarioParty7Item("Progressive Wallet", player))

    if options.locked_menu_navigation.value:
        world.itempool.append(MarioParty7Item("Shop Menu Navigation", player))
        world.itempool.append(MarioParty7Item("Star Purchase Menu Navigation", player))
        world.itempool.append(MarioParty7Item("Board Event Menu Navigation", player))

    if options.locked_minigame_actions.value:
        world.itempool.append(MarioParty7Item("Minigame Jump", player))
        world.itempool.append(MarioParty7Item("Minigame Run", player))
        world.itempool.append(MarioParty7Item("Minigame Mash", player))

    location_count = len([location for location in [region.locations for region in world.regions]])
    filler_count = location_count - len(world.itempool)

    for _ in range(filler_count):
        world.itempool.append(MarioParty7Item(random.choice(filler_items), player))


progression_items = [
    "Progressive Dice Block",
    "Progressive Wallet",
    "Shop Menu Navigation",
    "Star Purchase Menu Navigation",
    "Minigame Jump",
    "Minigame Run",
    "Minigame Mash",
    "Grand Canal",
    "Pagoda Peak",
    "Pyramid Park",
    "Neon Heights",
    "Windmillville",
    "Bower's Enchanted Inferno"
]

useful_items = [
    "Progressive Capsule Capacity",
    "Board Event Menu Navigation"
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