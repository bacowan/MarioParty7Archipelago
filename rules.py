from BaseClasses import MultiWorld
from worlds.mp7 import MarioParty7Options
from worlds.generic.Rules import set_rule


def set_rules(world: MultiWorld, options: MarioParty7Options, player: int)  -> None:

    # boards
    set_rule(world.get_entrance("Menu -> Grand Canal", player),
             lambda state: state.has("Grand Canal"))
    set_rule(world.get_entrance("Menu -> Pagoda Peak", player),
             lambda state: state.has("Pagoda Peak"))
    set_rule(world.get_entrance("Menu -> Pyramid Park", player),
             lambda state: state.has("Pyramid Park"))
    set_rule(world.get_entrance("Menu -> Neon Heights", player),
             lambda state: state.has("Neon Heights"))
    set_rule(world.get_entrance("Menu -> Windmillville", player),
             lambda state: state.has("Windmillville"))
    set_rule(world.get_entrance("Menu -> Bowser's Enchanted Inferno", player),
             lambda state: state.has("Bowser's Enchanted Inferno"))

    # coin checks
    set_rule()