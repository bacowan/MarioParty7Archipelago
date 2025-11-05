from BaseClasses import MultiWorld, Region
from worlds.mp7 import MarioParty7Options
from worlds.mp7.locations import add_location, space_locations, coin_count_locations, minigame_locations


def create_regions(world: MultiWorld, options: MarioParty7Options, player: int):
    menu_region = Region("Menu", player, world)
    world.regions.append(menu_region)

    create_boards(world, menu_region, options, player)
    create_locations_available_anywhere(menu_region, options)

def create_locations_available_anywhere(menu_region: Region, options: MarioParty7Options):
    if options.space_sanity.value:
        for location in space_locations:
            add_location(location, menu_region)

    if options.coin_counts_as_checks.value:
        for location in coin_count_locations:
            add_location(location, menu_region)

    if options.minigame_sanity.value:
        for location in minigame_locations:
            add_location(location, menu_region)

def create_boards(world: MultiWorld, menu_region: Region, options: MarioParty7Options, player: int):
    grand_canal = create_board("Grand Canal", menu_region, world, player)
    pagoda_peak = create_board("Pagoda Peak", menu_region, world, player)
    pyramid_park = create_board("Pyramid Park", menu_region, world, player)
    neon_heights = create_board("Neon Heights", menu_region, world, player)
    windmillville = create_board("Windmillville", menu_region, world, player)
    bowsers_enchanted_inferno = create_board("Bowser's Enchanted Inferno", menu_region, world, player)

    add_location("Grand Canal Beaten", grand_canal)
    add_location("Pagoda Peak Beaten", pagoda_peak)
    add_location("Pyramid Park Beaten", pyramid_park)
    add_location("Neon Heights Beaten", neon_heights)
    add_location("Windmillville Beaten", windmillville)

    if options.shop_sanity.value:
        add_location("Grand Canal Orb Hut 1 Left Item", grand_canal)
        add_location("Grand Canal Orb Hut 1 Middle Item", grand_canal)
        add_location("Grand Canal Orb Hut 1 Right Item", grand_canal)
        add_location("Grand Canal Orb Hut 2 Left Item", grand_canal)
        add_location("Grand Canal Orb Hut 2 Middle Item", grand_canal)
        add_location("Grand Canal Orb Hut 2 Right Item", grand_canal)

        add_location("Pagoda Peak Orb Hut 1 Left Item", pagoda_peak)
        add_location("Pagoda Peak Orb Hut 1 Middle Item", pagoda_peak)
        add_location("Pagoda Peak Orb Hut 1 Right Item", pagoda_peak)
        add_location("Pagoda Peak Orb Hut 2 Left Item", pagoda_peak)
        add_location("Pagoda Peak Orb Hut 2 Middle Item", pagoda_peak)
        add_location("Pagoda Peak Orb Hut 2 Right Item", pagoda_peak)

        add_location("Neon Heights Orb Hut 1 Left Item", neon_heights)
        add_location("Neon Heights Orb Hut 1 Middle Item", neon_heights)
        add_location("Neon Heights Orb Hut 1 Right Item", neon_heights)
        add_location("Neon Heights Orb Hut 2 Left Item", neon_heights)
        add_location("Neon Heights Orb Hut 2 Middle Item", neon_heights)
        add_location("Neon Heights Orb Hut 2 Right Item", neon_heights)

        add_location("Windmillville Orb Hut 1 Left Item", windmillville)
        add_location("Windmillville Orb Hut 1 Middle Item", windmillville)
        add_location("Windmillville Orb Hut 1 Right Item", windmillville)
        add_location("Windmillville Orb Hut 2 Left Item", windmillville)
        add_location("Windmillville Orb Hut 2 Middle Item", windmillville)
        add_location("Windmillville Orb Hut 2 Right Item", windmillville)

        add_location("Bowser's Enchanted Inferno Orb Hut 1 Left Item", bowsers_enchanted_inferno)
        add_location("Bowser's Enchanted Inferno Orb Hut 1 Middle Item", bowsers_enchanted_inferno)
        add_location("Bowser's Enchanted Inferno Orb Hut 1 Right Item", bowsers_enchanted_inferno)
        add_location("Bowser's Enchanted Inferno Orb Hut 2 Left Item", bowsers_enchanted_inferno)
        add_location("Bowser's Enchanted Inferno Orb Hut 2 Middle Item", bowsers_enchanted_inferno)
        add_location("Bowser's Enchanted Inferno Orb Hut 2 Right Item", bowsers_enchanted_inferno)

def create_board(name: str, menu_region: Region, world: MultiWorld, player: int) -> Region:
    region = Region(name, player, world)
    menu_region.connect(region)
    world.regions.append(region)
    return region