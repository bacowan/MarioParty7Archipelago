from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, components, launch_subprocess


class MarioParty7WebWorld(WebWorld):
    theme = "partyTime"

class MarioParty7World(World):
    """
    Mario Party 7
    """
    game = "Mario Party 7"
    item_name_to_id = {}
    location_name_to_id = {}

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