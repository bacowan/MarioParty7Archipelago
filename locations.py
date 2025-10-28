from BaseClasses import Location, Region


class MarioParty7Location(Location):
    game: str = "Mario Party 7"

def add_location(name: str, reg: Region):
    location = MarioParty7Location(reg.player, name, location_name_to_id[name], reg)
    reg.locations += [location]

all_locations = [
    "Beat Minigame"
]

location_name_to_id = {name: address for address, name in enumerate(all_locations, 1)}