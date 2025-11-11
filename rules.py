from BaseClasses import MultiWorld, CollectionState
from worlds.mp7 import MarioParty7Options
from worlds.generic.Rules import set_rule, add_rule
from worlds.mp7.items import wallet_sizes, dice_sizes
from worlds.mp7.locations import coin_count_locations, coin_count_location_name_to_value, space_locations, \
    space_count_location_name_to_value, orb_hut_locations, board_locations

def set_rules(world: MultiWorld, options: MarioParty7Options, player: int) -> None:
    set_board_rules(world, options, player)
    set_victory_condition(world, options, player)
    if options.coin_counts_as_checks:
        set_coin_rules(world, options, player)
    if options.space_sanity:
        set_space_count_rules(world, options, player)
    if options.minigame_sanity and options.locked_minigame_actions:
        set_minigame_rules(world, options, player)
    if options.shop_sanity:
        set_shop_sanity_rules(world, options, player)

def has_enough_money_for_shop_item(location_name: str, options: MarioParty7Options, state: CollectionState, player: int) -> bool:
    # Left item will always be 5 coins, middle 10, right 20
    if location_name.endswith("Left Item"):
        return is_wallet_size_at_least(5, options, state, player)
    if location_name.endswith("Middle Item"):
        return is_wallet_size_at_least(10, options, state, player)
    return is_wallet_size_at_least(20, options, state, player)

def set_shop_sanity_rules(world: MultiWorld, options: MarioParty7Options, player: int) -> None:

    # Need to be able to navigate the shops in order to buy anything from them
    if options.locked_menu_navigation.value:
        for location in orb_hut_locations:
            add_rule(world.get_location(location, player), lambda state: state.has("Shop Menu Navigation", player))

    # Make sure the player can afford the item
    if options.wallet_progression.value != options.wallet_progression.option_off:
        for location in orb_hut_locations:
            add_rule(world.get_location(location, player),
                     lambda state, loc=location: has_enough_money_for_shop_item(loc, options, state, player))

    # Grand Canal
    add_rule(world.get_location("Grand Canal Orb Hut 1 Left Item", player),
             lambda state: state.has("Grand Canal", player))
    add_rule(world.get_location("Grand Canal Orb Hut 1 Middle Item", player),
             lambda state: state.has("Grand Canal", player))
    add_rule(world.get_location("Grand Canal Orb Hut 1 Right Item", player),
             lambda state: state.has("Grand Canal", player))
    add_rule(world.get_location("Grand Canal Orb Hut 2 Left Item", player),
             lambda state: state.has("Grand Canal", player) and can_roll_at_least(5, options, state, player))
    add_rule(world.get_location("Grand Canal Orb Hut 2 Middle Item", player),
             lambda state: state.has("Grand Canal", player) and can_roll_at_least(5, options, state, player))
    add_rule(world.get_location("Grand Canal Orb Hut 2 Right Item", player),
             lambda state: state.has("Grand Canal", player) and can_roll_at_least(5, options, state, player))

    # Pagoda Peak
    add_rule(world.get_location("Pagoda Peak Orb Hut 1 Left Item", player),
             lambda state: state.has("Pagoda Peak", player))
    add_rule(world.get_location("Pagoda Peak Orb Hut 1 Middle Item", player),
             lambda state: state.has("Pagoda Peak", player))
    add_rule(world.get_location("Pagoda Peak Orb Hut 1 Right Item", player),
             lambda state: state.has("Pagoda Peak", player))
    add_rule(world.get_location("Pagoda Peak Orb Hut 2 Left Item", player),
             lambda state: state.has("Pagoda Peak", player) and can_roll_at_least(5, options, state, player))
    add_rule(world.get_location("Pagoda Peak Orb Hut 2 Middle Item", player),
             lambda state: state.has("Pagoda Peak", player) and can_roll_at_least(5, options, state, player))
    add_rule(world.get_location("Pagoda Peak Orb Hut 2 Right Item", player),
             lambda state: state.has("Pagoda Peak", player) and can_roll_at_least(5, options, state, player))

    # Neon Heights
    add_rule(world.get_location("Neon Heights Orb Hut 1 Left Item", player),
             lambda state: state.has("Neon Heights", player) and can_roll_at_least(2, options, state, player))
    add_rule(world.get_location("Neon Heights Orb Hut 1 Middle Item", player),
             lambda state: state.has("Neon Heights", player) and can_roll_at_least(2, options, state, player))
    add_rule(world.get_location("Neon Heights Orb Hut 1 Right Item", player),
             lambda state: state.has("Neon Heights", player) and can_roll_at_least(2, options, state, player))
    add_rule(world.get_location("Neon Heights Orb Hut 2 Left Item", player),
             lambda state: state.has("Neon Heights", player) and can_roll_at_least(10, options, state, player))
    add_rule(world.get_location("Neon Heights Orb Hut 2 Middle Item", player),
             lambda state: state.has("Neon Heights", player) and can_roll_at_least(10, options, state, player))
    add_rule(world.get_location("Neon Heights Orb Hut 2 Right Item", player),
             lambda state: state.has("Neon Heights", player) and can_roll_at_least(10, options, state, player))

    # Windmillville
    add_rule(world.get_location("Windmillville Orb Hut 1 Left Item", player),
             lambda state: state.has("Windmillville", player) and can_roll_at_least(5, options, state, player))
    add_rule(world.get_location("Windmillville Orb Hut 1 Middle Item", player),
             lambda state: state.has("Windmillville", player) and can_roll_at_least(5, options, state, player))
    add_rule(world.get_location("Windmillville Orb Hut 1 Right Item", player),
             lambda state: state.has("Windmillville", player) and can_roll_at_least(5, options, state, player))
    add_rule(world.get_location("Windmillville Orb Hut 2 Left Item", player),
             lambda state: state.has("Windmillville", player) and can_roll_at_least(10, options, state, player))
    add_rule(world.get_location("Windmillville Orb Hut 2 Middle Item", player),
             lambda state: state.has("Windmillville", player) and can_roll_at_least(10, options, state, player))
    add_rule(world.get_location("Windmillville Orb Hut 2 Right Item", player),
             lambda state: state.has("Windmillville", player) and can_roll_at_least(10, options, state, player))

    # Bowser's Enchanted Inferno
    add_rule(world.get_location("Bowser's Enchanted Inferno Orb Hut 1 Left Item", player),
             lambda state: state.has("Bowser's Enchanted Inferno", player))
    add_rule(world.get_location("Bowser's Enchanted Inferno Orb Hut 1 Middle Item", player),
             lambda state: state.has("Bowser's Enchanted Inferno", player))
    add_rule(world.get_location("Bowser's Enchanted Inferno Orb Hut 1 Right Item", player),
             lambda state: state.has("Bowser's Enchanted Inferno", player))
    add_rule(world.get_location("Bowser's Enchanted Inferno Orb Hut 2 Left Item", player),
             lambda state: state.has("Bowser's Enchanted Inferno", player) and can_roll_at_least(10, options, state, player))
    add_rule(world.get_location("Bowser's Enchanted Inferno Orb Hut 2 Middle Item", player),
             lambda state: state.has("Bowser's Enchanted Inferno", player) and can_roll_at_least(10, options, state, player))
    add_rule(world.get_location("Bowser's Enchanted Inferno Orb Hut 2 Right Item", player),
             lambda state: state.has("Bowser's Enchanted Inferno", player) and can_roll_at_least(10, options, state, player))

def set_minigame_rules(world: MultiWorld, options: MarioParty7Options, player: int) -> None:
    add_rule(world.get_location("Warp Pipe Dreams Beaten", player),
             lambda state: state.has("Minigame Run", player) and state.has("Minigame Jump", player))
    add_rule(world.get_location("Weight For It Beaten", player),
             lambda state: state.has("Minigame Run", player))
    # add_rule(world.get_location("Gimme a Sign Beaten", player),
    #          lambda state: state.has("Minigame Run", player))
    add_rule(world.get_location("Bridge Work Beaten", player),
             lambda state: state.has("Minigame Run", player))
    add_rule(world.get_location("Spin Doctor Beaten", player),
             lambda state: state.has("Minigame Run", player))
    add_rule(world.get_location("Royal Rumpus Beaten", player),
             lambda state: state.has("Minigame Run", player) and state.has("Minigame Jump", player))
    add_rule(world.get_location("Apes of Wrath Beaten", player),
             lambda state: state.has("Minigame Run", player) and state.has("Minigame Jump", player))
    add_rule(world.get_location("Fish And Cheeps Beaten", player),
             lambda state: state.has("Minigame Mash", player))
    add_rule(world.get_location("Camp Ukiki Beaten", player),
             lambda state: state.has("Minigame Run", player) and state.has("Minigame Jump", player))

def set_space_count_rules(world: MultiWorld, options: MarioParty7Options, player: int) -> None:
    # assume that you can only reach a certain amount of spaces with small dice
    # and few unlocked stages
    for location in [x for x in space_locations if space_count_location_name_to_value(x) < 30]:
        add_rule(world.get_location(location, player), lambda state:
            can_roll_at_least(5, options, state, player)
            or state.count_group("Boards", player) > 3)

    for location in [x for x in space_locations if 30 <= space_count_location_name_to_value(x) < 100]:
        add_rule(world.get_location(location, player), lambda state:
            state.count_group("Boards", player) > 2
            and (
                    can_roll_at_least(5, options, state, player)
                    or (can_roll_at_least(2, options, state, player) and state.count_group("Boards", player) > 3)
            ))

    for location in [x for x in space_locations if space_count_location_name_to_value(x) >= 100]:
        add_rule(world.get_location(location, player), lambda state:
            state.count_group("Boards", player) > 2
            and (
                    can_roll_at_least(10, options, state, player)
                    or (can_roll_at_least(5, options, state, player) and state.count_group("Boards", player) > 3)
            ))

def set_coin_rules(world: MultiWorld, options: MarioParty7Options, player: int) -> None:
    # base requirement for having a wallet that can actually hold the correct number of coins
    for location in coin_count_locations:
        coin_count = coin_count_location_name_to_value(location)
        add_rule(world.get_location(location, player),
                 lambda state, cc=coin_count: is_wallet_size_at_least(cc, options, state, player))

    # assume that you can only collect a certain amount of coins with small dice
    for location in [x for x in coin_count_locations if 20 <= coin_count_location_name_to_value(x) < 50]:
        add_rule(world.get_location(location, player), lambda state: can_roll_at_least(2, options, state, player))
    for location in [x for x in coin_count_locations if 50 <= coin_count_location_name_to_value(x) < 100]:
        add_rule(world.get_location(location, player), lambda state: can_roll_at_least(5, options, state, player))
    for location in [x for x in coin_count_locations if coin_count_location_name_to_value(x) >= 100]:
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
                 lambda state: state.has("Bowser's Enchanted Inferno", player))
    else:
        set_rule(world.get_entrance("Menu -> Bowser's Enchanted Inferno", player),
                 lambda state: state.has("Grand Canal", player)
                    and state.has("Pagoda Peak", player)
                    and state.has("Pyramid Park", player)
                    and state.has("Neon Heights", player)
                    and state.has("Windmillville", player))

    # assume that you can only beat any given stage with a big enough dice block
    add_rule(world.get_location("Grand Canal Beaten", player),
             lambda state: can_roll_at_least(5, options, state, player))
    add_rule(world.get_location("Grand Canal Beaten Event Location", player),
             lambda state: can_roll_at_least(5, options, state, player))
    add_rule(world.get_location("Pagoda Peak Beaten", player),
             lambda state: can_roll_at_least(5, options, state, player))
    add_rule(world.get_location("Pagoda Peak Beaten Event Location", player),
             lambda state: can_roll_at_least(5, options, state, player))
    add_rule(world.get_location("Pyramid Park Beaten", player),
             lambda state: can_roll_at_least(5, options, state, player))
    add_rule(world.get_location("Pyramid Park Beaten Event Location", player),
             lambda state: can_roll_at_least(5, options, state, player))
    add_rule(world.get_location("Neon Heights Beaten", player),
             lambda state: can_roll_at_least(5, options, state, player))
    add_rule(world.get_location("Neon Heights Beaten Event Location", player),
             lambda state: can_roll_at_least(5, options, state, player))
    add_rule(world.get_location("Windmillville Beaten", player),
             lambda state: can_roll_at_least(5, options, state, player))
    add_rule(world.get_location("Windmillville Beaten Event Location", player),
             lambda state: can_roll_at_least(5, options, state, player))
    add_rule(world.get_location("Bowser's Enchanted Inferno Beaten Event Location", player),
             lambda state: can_roll_at_least(5, options, state, player))
    if options.win_condition == options.win_condition.option_beat_all_stages:
        add_rule(world.get_location("Bowser's Enchanted Inferno Beaten", player),
                 lambda state: can_roll_at_least(5, options, state, player))

    # assume that you can only beat any given stage with a big enough wallet
    add_rule(world.get_location("Grand Canal Beaten", player),
             lambda state: is_wallet_size_at_least(20, options, state, player))
    add_rule(world.get_location("Grand Canal Beaten Event Location", player),
             lambda state: is_wallet_size_at_least(20, options, state, player))
    add_rule(world.get_location("Pagoda Peak Beaten", player),
             lambda state: is_wallet_size_at_least(20, options, state, player))
    add_rule(world.get_location("Pagoda Peak Beaten Event Location", player),
             lambda state: is_wallet_size_at_least(20, options, state, player))
    add_rule(world.get_location("Pyramid Park Beaten", player),
             lambda state: is_wallet_size_at_least(20, options, state, player))
    add_rule(world.get_location("Pyramid Park Beaten Event Location", player),
             lambda state: is_wallet_size_at_least(20, options, state, player))
    add_rule(world.get_location("Neon Heights Beaten", player),
             lambda state: is_wallet_size_at_least(20, options, state, player))
    add_rule(world.get_location("Neon Heights Beaten Event Location", player),
             lambda state: is_wallet_size_at_least(20, options, state, player))
    add_rule(world.get_location("Windmillville Beaten", player),
             lambda state: is_wallet_size_at_least(20, options, state, player))
    add_rule(world.get_location("Windmillville Beaten Event Location", player),
             lambda state: is_wallet_size_at_least(20, options, state, player))
    add_rule(world.get_location("Bowser's Enchanted Inferno Beaten Event Location", player),
             lambda state: is_wallet_size_at_least(20, options, state, player))
    if options.win_condition == options.win_condition.option_beat_all_stages:
        add_rule(world.get_location("Bowser's Enchanted Inferno Beaten", player),
                 lambda state: is_wallet_size_at_least(20, options, state, player))

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
        return wallets[progressive_wallet_count] >= value

def can_roll_at_least(value: int, options: MarioParty7Options, state: CollectionState, player: int) -> bool:
    if not options.dice_block_progression.value:
        return True

    progressive_dice_count = state.count("Progressive Dice Block", player)
    if progressive_dice_count >= len(dice_sizes):
        return True
    else:
        return dice_sizes[progressive_dice_count] >= value

def set_victory_condition(world: MultiWorld, options: MarioParty7Options, player: int) -> None:
    if options.win_condition == options.win_condition.option_beat_all_stages:
        world.completion_condition[player] = lambda state: (
            state.has("Grand Canal Beaten Event Item", player)
            and state.has("Pagoda Peak Beaten Event Item", player)
            and state.has("Pyramid Park Beaten Event Item", player)
            and state.has("Neon Heights Beaten Event Item", player)
            and state.has("Windmillville Beaten Event Item", player)
            and state.has("Bowser's Enchanted Inferno Beaten Event Item", player))
    else:
        world.completion_condition[player] = lambda state: state.has("Bowser's Enchanted Inferno Beaten Event Item", player)