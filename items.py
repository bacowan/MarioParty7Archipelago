import random

from BaseClasses import Item, ItemClassification, MultiWorld
from worlds.AutoWorld import World
from .options import MarioParty7Options, WalletProgression


class MarioParty7Item(Item):
    game: str = "Mario Party 7"

def create_item(name: str, player: int) -> MarioParty7Item:
    return MarioParty7Item(name, item_classifications[name], item_name_to_id[name], player)

def create_event_item(name: str, player: int) -> MarioParty7Item:
    return MarioParty7Item(name, ItemClassification.progression, None, player)

def create_items(world: MultiWorld, options: MarioParty7Options, player: int) -> None:
    board_unlocks = [
        create_item("Grand Canal Key", player),
        create_item("Pagoda Peak Key", player),
        create_item("Pyramid Park Key", player),
        create_item("Neon Heights Key", player),
        create_item("Windmillville Key", player),
        create_item("Bowser's Enchanted Inferno Key", player)
    ]

    if options.win_condition.value == options.win_condition.option_beat_bowsers_enchanted_inferno:
        # If the objective is to beat bowser's enchanted inferno, exclude it from the possible
        # options for initial stage
        initial_board_random_max_index = len(board_unlocks) - 2
    else:
        initial_board_random_max_index = len(board_unlocks) - 1

    initial_board_random_index = random.randint(0, initial_board_random_max_index)
    initial_board = board_unlocks[initial_board_random_index]
    world.push_precollected(initial_board)
    board_unlocks.remove(initial_board)

    for board in board_unlocks:
        world.itempool.append(board)

    if options.dice_block_progression.value:
        for _ in range(4):
            world.itempool.append(create_item("Progressive Dice Block", player))

    if options.wallet_progression.value == WalletProgression.option_easy:
        for _ in range(4):
            world.itempool.append(create_item("Progressive Wallet", player))
    elif options.wallet_progression.value == WalletProgression.option_medium:
        for _ in range(5):
            world.itempool.append(create_item("Progressive Wallet", player))
    elif options.wallet_progression.value == WalletProgression.option_hard:
        for _ in range(7):
            world.itempool.append(create_item("Progressive Wallet", player))

    if options.locked_minigame_actions.value:
        world.itempool.append(create_item("Minigame Jump", player))
        world.itempool.append(create_item("Minigame Run", player))
        world.itempool.append(create_item("Minigame Mash", player))

    location_count = 0
    for _ in world.get_locations(player):
        location_count += 1

    filler_count = location_count - len(world.itempool)

    for _ in range(filler_count):
        world.itempool.append(create_item(random.choice(filler_items), player))


progression_items = [
    "Progressive Dice Block",
    "Progressive Wallet",
    "Minigame Jump",
    "Minigame Run",
    "Minigame Mash",
    "Grand Canal Key",
    "Pagoda Peak Key",
    "Pyramid Park Key",
    "Neon Heights Key",
    "Windmillville Key",
    "Bowser's Enchanted Inferno Key"
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

item_name_groups = {
    "Boards": { "Grand Canal Key", "Pyramid Park Key", "Neon Heights Key", "Windmillville Key", "Bower's Enchanted Inferno Key" }
}

dice_sizes = [1, 2, 5, 10]

wallet_sizes = {
    "easy": [30, 50, 100, 999],
    "medium": [0, 20, 50, 100, 999],
    "hard": [0, 5, 10, 20, 50, 100, 999]
}