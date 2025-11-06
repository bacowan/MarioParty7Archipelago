from BaseClasses import MultiWorld, CollectionState
from worlds.mp7 import MarioParty7Options
from worlds.generic.Rules import set_rule, add_rule
from worlds.mp7.items import create_event
from worlds.mp7.locations import coin_count_locations, coin_count_location_name_to_value, space_locations, \
    space_count_location_name_to_value

wallet_sizes = {
    "easy": [30, 50, 100, 999],
    "medium": [0, 20, 50, 100, 999],
    "hard": [0, 5, 10, 20, 50, 100, 999]
}

dice_sizes = [1, 2, 5, 10]

def set_rules(world: MultiWorld, options: MarioParty7Options, player: int) -> None:
    set_board_rules(world, options, player)
    if options.coin_counts_as_checks:
        set_coin_rules(world, options, player)
    if options.space_sanity:
        set_space_count_rules(world, options, player)
    if options.minigame_sanity and options.locked_minigame_actions:
        set_minigame_rules(world, options, player)
    if options.shop_sanity:
        set_shop_sanity_rules(world, options, player)

def set_shop_sanity_rules(world: MultiWorld, options: MarioParty7Options, player: int) -> None:
    # assume that you can only reach orb huts with a high enough dice roll

    # Grand Canal
    set_rule(world.get_location("Grand Canal Orb Hut 1 Left Item", player),
             lambda state: state.has("Grand Canal", player))
    set_rule(world.get_location("Grand Canal Orb Hut 1 Middle Item", player),
             lambda state: state.has("Grand Canal", player))
    set_rule(world.get_location("Grand Canal Orb Hut 1 Right Item", player),
             lambda state: state.has("Grand Canal", player))
    set_rule(world.get_location("Grand Canal Orb Hut 2 Left Item", player),
             lambda state: state.has("Grand Canal", player) and can_roll_at_least(5, options, state, player))
    set_rule(world.get_location("Grand Canal Orb Hut 2 Middle Item", player),
             lambda state: state.has("Grand Canal", player) and can_roll_at_least(5, options, state, player))
    set_rule(world.get_location("Grand Canal Orb Hut 2 Right Item", player),
             lambda state: state.has("Grand Canal", player) and can_roll_at_least(5, options, state, player))

    # Pagoda Peak
    set_rule(world.get_location("Pagoda Peak Orb Hut 1 Left Item", player),
             lambda state: state.has("Pagoda Peak", player))
    set_rule(world.get_location("Pagoda Peak Orb Hut 1 Middle Item", player),
             lambda state: state.has("Pagoda Peak", player))
    set_rule(world.get_location("Pagoda Peak Orb Hut 1 Right Item", player),
             lambda state: state.has("Pagoda Peak", player))
    set_rule(world.get_location("Pagoda Peak Orb Hut 2 Left Item", player),
             lambda state: state.has("Pagoda Peak", player) and can_roll_at_least(5, options, state, player))
    set_rule(world.get_location("Pagoda Peak Orb Hut 2 Middle Item", player),
             lambda state: state.has("Pagoda Peak", player) and can_roll_at_least(5, options, state, player))
    set_rule(world.get_location("Pagoda Peak Orb Hut 2 Right Item", player),
             lambda state: state.has("Pagoda Peak", player) and can_roll_at_least(5, options, state, player))

    # Neon Heights
    set_rule(world.get_location("Neon Heights Orb Hut 1 Left Item", player),
             lambda state: state.has("Neon Heights", player) and can_roll_at_least(2, options, state, player))
    set_rule(world.get_location("Neon Heights Orb Hut 1 Middle Item", player),
             lambda state: state.has("Neon Heights", player) and can_roll_at_least(2, options, state, player))
    set_rule(world.get_location("Neon Heights Orb Hut 1 Right Item", player),
             lambda state: state.has("Neon Heights", player) and can_roll_at_least(2, options, state, player))
    set_rule(world.get_location("Neon Heights Orb Hut 2 Left Item", player),
             lambda state: state.has("Neon Heights", player) and can_roll_at_least(10, options, state, player))
    set_rule(world.get_location("Neon Heights Orb Hut 2 Middle Item", player),
             lambda state: state.has("Neon Heights", player) and can_roll_at_least(10, options, state, player))
    set_rule(world.get_location("Neon Heights Orb Hut 2 Right Item", player),
             lambda state: state.has("Neon Heights", player) and can_roll_at_least(10, options, state, player))

    # Windmillville
    set_rule(world.get_location("Windmillville Orb Hut 1 Left Item", player),
             lambda state: state.has("Windmillville", player) and can_roll_at_least(5, options, state, player))
    set_rule(world.get_location("Windmillville Orb Hut 1 Middle Item", player),
             lambda state: state.has("Windmillville", player) and can_roll_at_least(5, options, state, player))
    set_rule(world.get_location("Windmillville Orb Hut 1 Right Item", player),
             lambda state: state.has("Windmillville", player) and can_roll_at_least(5, options, state, player))
    set_rule(world.get_location("Windmillville Orb Hut 2 Left Item", player),
             lambda state: state.has("Windmillville", player) and can_roll_at_least(10, options, state, player))
    set_rule(world.get_location("Windmillville Orb Hut 2 Middle Item", player),
             lambda state: state.has("Windmillville", player) and can_roll_at_least(10, options, state, player))
    set_rule(world.get_location("Windmillville Orb Hut 2 Right Item", player),
             lambda state: state.has("Windmillville", player) and can_roll_at_least(10, options, state, player))

    # Bowser's Enchanted Inferno
    set_rule(world.get_location("Bowser's Enchanted Inferno Orb Hut 1 Left Item", player),
             lambda state: state.has("Bowser's Enchanted Inferno", player))
    set_rule(world.get_location("Bowser's Enchanted Inferno Orb Hut 1 Middle Item", player),
             lambda state: state.has("Bowser's Enchanted Inferno", player))
    set_rule(world.get_location("Bowser's Enchanted Inferno Orb Hut 1 Right Item", player),
             lambda state: state.has("Bowser's Enchanted Inferno", player))
    set_rule(world.get_location("Bowser's Enchanted Inferno Orb Hut 2 Left Item", player),
             lambda state: state.has("Bowser's Enchanted Inferno", player) and can_roll_at_least(10, options, state, player))
    set_rule(world.get_location("Bowser's Enchanted Inferno Orb Hut 2 Middle Item", player),
             lambda state: state.has("Bowser's Enchanted Inferno", player) and can_roll_at_least(10, options, state, player))
    set_rule(world.get_location("Bowser's Enchanted Inferno Orb Hut 2 Right Item", player),
             lambda state: state.has("Bowser's Enchanted Inferno", player) and can_roll_at_least(10, options, state, player))

def set_minigame_rules(world: MultiWorld, options: MarioParty7Options, player: int) -> None:
    set_rule(world.get_location("Warp Pipe Dreams Beaten", player),
             lambda state: state.has("Minigame Run", player) and state.has("Minigame Jump", player))
    set_rule(world.get_location("Weight For It Beaten", player),
             lambda state: state.has("Minigame Run", player))
    set_rule(world.get_location("Gimme a Sign Beaten", player),
             lambda state: state.has("Minigame Run", player))
    set_rule(world.get_location("Bridge Work Beaten", player),
             lambda state: state.has("Minigame Run", player))
    set_rule(world.get_location("Spin Doctor Beaten", player),
             lambda state: state.has("Minigame Run", player))
    set_rule(world.get_location("Royal Rumpus Beaten", player),
             lambda state: state.has("Minigame Run", player) and state.has("Minigame Jump", player))
    set_rule(world.get_location("Apes of Wrath Beaten", player),
             lambda state: state.has("Minigame Run", player) and state.has("Minigame Jump", player))
    set_rule(world.get_location("Fish And Cheeps Beaten", player),
             lambda state: state.has("Minigame Mash", player))
    set_rule(world.get_location("Camp Ukiki Beaten", player),
             lambda state: state.has("Minigame Run", player) and state.has("Minigame Jump", player))

def set_space_count_rules(world: MultiWorld, options: MarioParty7Options, player: int) -> None:
    # assume that you can only reach a certain amount of spaces with small dice
    # and few unlocked stages
    for location in [x for x in space_locations if space_count_location_name_to_value(x) > 10]:
        add_rule(world.get_location(location, player), lambda state:
            can_roll_at_least(2, options, state, player)
            or state.count_group("Boards", player) > 3)

    for location in [x for x in space_locations if space_count_location_name_to_value(x) > 100]:
        add_rule(world.get_location(location, player), lambda state:
            state.count_group("Boards", player) > 2
            and (
                    can_roll_at_least(5, options, state, player)
                    or (can_roll_at_least(2, options, state, player) and state.count_group("Boards", player) > 3)
            ))

    for location in [x for x in space_locations if space_count_location_name_to_value(x) > 200]:
        add_rule(world.get_location(location, player), lambda state:
            can_roll_at_least(10, options, state, player)
            and state.count_group("Boards", player) > 3)

def set_coin_rules(world: MultiWorld, options: MarioParty7Options, player: int) -> None:
    # base requirement for having a wallet that can actually hold the correct number of coins
    for location in coin_count_locations:
        coin_count = coin_count_location_name_to_value(location)
        add_rule(world.get_location(location, player), lambda state: is_wallet_size_at_least(coin_count, options, state, player))

    # assume that you can only collect a certain amount of coins with small dice
    for location in [x for x in coin_count_locations if coin_count_location_name_to_value(x) > 20]:
        add_rule(world.get_location(location, player), lambda state: can_roll_at_least(2, options, state, player))
    for location in [x for x in coin_count_locations if coin_count_location_name_to_value(x) > 50]:
        add_rule(world.get_location(location, player), lambda state: can_roll_at_least(5, options, state, player))
    for location in [x for x in coin_count_locations if coin_count_location_name_to_value(x) > 100]:
        add_rule(world.get_location(location, player), lambda state: can_roll_at_least(10, options, state, player))

def set_board_rules(world: MultiWorld, options: MarioParty7Options, player: int) -> None:
    set_rule(world.get_entrance("Menu -> Grand Canal", player),
             lambda state: state.has("Grand Canal", player))
    set_rule(world.get_entrance("Menu -> Pagoda Peak", player),
             lambda state: state.has("Pagoda Peak", player))
    set_rule(world.get_entrance("Menu -> Pyramid Park", player),
             lambda state: state.has("Pyramid Park", player))
    set_rule(world.get_entrance("Menu -> Neon Heights", player),
             lambda state: state.has("Neon Heights", player))
    set_rule(world.get_entrance("Menu -> Windmillville", player),
             lambda state: state.has("Windmillville", player))

    if options.win_condition == options.win_condition.option_beat_all_stages:
        set_rule(world.get_entrance("Menu -> Bowser's Enchanted Inferno", player),
                 lambda state: state.has("Bowser's Enchanted Inferno"))
    else:
        create_event("Beat Grand Canal", player)
        create_event("Beat Pagoda Peak", player)
        create_event("Beat Pyramid Park", player)
        create_event("Beat Neon Heights", player)
        create_event("Beat Windmillville", player)
        set_rule(world.get_entrance("Menu -> Bowser's Enchanted Inferno", player),
                 lambda state: state.has("Beat Grand Canal", player)
                    and state.has("Pagoda Peak", player)
                    and state.has("Beat Pyramid Park", player)
                    and state.has("Beat Neon Heights", player)
                    and state.has("Beat Windmillville", player))

def is_wallet_size_at_least(value: int, options: MarioParty7Options, state: CollectionState, player: int) -> bool:
    if options.wallet_progression.value == options.wallet_progression.option_off:
        return True
    elif options.wallet_progression.value == options.wallet_progression.option_easy:
        wallets = wallet_sizes["easy"]
    elif options.wallet_progression.value == options.wallet_progression.option_medium:
        wallets = wallet_sizes["medium"]
    else:
        wallets = wallet_sizes["hard"]

    progressive_wallet_count = state.count("Progressive Wallet", player)
    if progressive_wallet_count >= len(wallets):
        return True
    else:
        return value >= wallets[progressive_wallet_count]

def can_roll_at_least(value: int, options: MarioParty7Options, state: CollectionState, player: int) -> bool:
    if not options.dice_block_progression.value:
        return True

    progressive_dice_count = state.count("Progressive Dice Block", player)
    if progressive_dice_count >= len(dice_sizes):
        return True
    else:
        return value >= dice_sizes[progressive_dice_count]