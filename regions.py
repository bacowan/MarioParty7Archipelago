from BaseClasses import MultiWorld, Region
from worlds.mp7 import MarioParty7Options
from worlds.mp7.locations import add_location


def create_regions(world: MultiWorld, options: MarioParty7Options, player: int):
    menu_region = Region("Menu", player, world)

    # stages
    grand_canal = Region("Grand Canal", player, world)
    menu_region.connect(grand_canal)

    world.regions.append(menu_region)
    world.regions.append(grand_canal)

    # minigames
    minigames_region = Region("Minigames", player, world)
    add_location("Beat Minigame", minigames_region)

    grand_canal.connect(minigames_region)

    world.regions.append(minigames_region)