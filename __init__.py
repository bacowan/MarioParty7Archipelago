from typing import Any

from Options import OptionError
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, components, launch_subprocess
from .items import item_classifications, MarioParty7Item, item_name_to_id, create_items, create_item, item_name_groups
from .locations import all_locations, location_name_to_id
from .options import MarioParty7Options
from .regions import create_regions
from .rules import set_rules


class MarioParty7WebWorld(WebWorld):
    theme = "partyTime"

class MarioParty7World(World):
    """
    Mario Party 7
    """
    game = "Mario Party 7"
    item_name_to_id = item_name_to_id
    location_name_to_id = location_name_to_id
    options_dataclass = MarioParty7Options
    options: MarioParty7Options
    item_name_groups = item_name_groups

    def generate_early(self):
        if self.options.wallet_progression and not self.options.minigame_sanity:
            raise OptionError("If Wallet Progression is set then Minigame Sanity must also be set")
        if self.options.dice_block_progression and not self.options.minigame_sanity:
            raise OptionError("If Dice Block Progression is set then Minigame Sanity must also be set")

    def create_item(self, item: str):
        return create_item(item, self.player)

    def create_regions(self) -> None:
        create_regions(self.multiworld, self.options, self.player)

    def create_items(self) -> None:
        create_items(self.multiworld, self.options, self.player)

    def set_rules(self) -> None:
        set_rules(self.multiworld, self.options, self.player)

    def fill_slot_data(self) -> dict[str, Any]:
        return self.options.as_dict("wallet_progression")

def launch_client():
    from .Mp7Client import main
    launch_subprocess(main, name="Mario Party 7 client")


def add_client_to_launcher() -> None:
    version = "0.2.0"
    found = False
    for c in components:
        if c.display_name == "Mario Party 7 Client":
            found = True
            if getattr(c, "version", 0) < version:
                c.version = version
                c.func = launch_client
                return
    if not found:
        components.append(Component("Mario Party 7 Client", "MarioParty7Client",
                                    func=launch_client))


add_client_to_launcher()