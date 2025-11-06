from BaseClasses import Location, Region

class MarioParty7Location(Location):
    game: str = "Mario Party 7"

def add_location(name: str, reg: Region):
    location = MarioParty7Location(reg.player, name, location_name_to_id[name], reg)
    reg.locations += [location]

def coin_count_location_name_to_value(name: str):
    return name.split(" ")[0]

def space_count_location_name_to_value(name: str):
    return name.split(" ")[0]

coin_count_locations = [
    "10 Coins in Wallet",
    "20 Coins in Wallet",
    "30 Coins in Wallet",
    "40 Coins in Wallet",
    "50 Coins in Wallet",
    "60 Coins in Wallet",
    "70 Coins in Wallet",
    "80 Coins in Wallet",
    "90 Coins in Wallet",
    "100 Coins in Wallet",
    "150 Coins in Wallet",
    "200 Coins in Wallet"
]

space_locations = [
    "20 Unique Spaces",
    "40 Unique Spaces",
    "60 Unique Spaces",
    "80 Unique Spaces",
    "100 Unique Spaces",
    "120 Unique Spaces",
    "140 Unique Spaces",
    "160 Unique Spaces",
    "180 Unique Spaces",
    "200 Unique Spaces",
    "220 Unique Spaces",
    "240 Unique Spaces",
    "260 Unique Spaces",
    "280 Unique Spaces",
    "300 Unique Spaces"
]

minigame_locations = [
    "Warp Pipe Dreams Beaten",
    "Weight For It Beaten",
    "Mad Props Beaten",
    "Gimme a Sign Beaten",
    "Bridge Work Beaten",
    "Spin Doctor Beaten",
    "Hip Hop Drop Beaten",
    "Royal Rumpus Beaten",
    "Light Speed Beaten",
    "Apes of Wrath Beaten",
    "Fish And Cheeps Beaten",
    "Camp Ukiki Beaten"
]

board_locations = [
    "Grand Canal Beaten",
    "Pagoda Peak Beaten",
    "Pyramid Park Beaten",
    "Neon Heights Beaten",
    "Windmillville Beaten",
    "Bowser's Enchanted Inferno Beaten"
]

orb_hut_locations = [
    "Grand Canal Orb Hut 1 Left Item",
    "Grand Canal Orb Hut 1 Middle Item",
    "Grand Canal Orb Hut 1 Right Item",
    "Grand Canal Orb Hut 2 Left Item",
    "Grand Canal Orb Hut 2 Middle Item",
    "Grand Canal Orb Hut 2 Right Item",
    "Pagoda Peak Orb Hut 1 Left Item",
    "Pagoda Peak Orb Hut 1 Middle Item",
    "Pagoda Peak Orb Hut 1 Right Item",
    "Pagoda Peak Orb Hut 2 Left Item",
    "Pagoda Peak Orb Hut 2 Middle Item",
    "Pagoda Peak Orb Hut 2 Right Item",
    "Neon Heights Orb Hut 1 Left Item",
    "Neon Heights Orb Hut 1 Middle Item",
    "Neon Heights Orb Hut 1 Right Item",
    "Neon Heights Orb Hut 2 Left Item",
    "Neon Heights Orb Hut 2 Middle Item",
    "Neon Heights Orb Hut 2 Right Item",
    "Windmillville Orb Hut 1 Left Item",
    "Windmillville Orb Hut 1 Middle Item",
    "Windmillville Orb Hut 1 Right Item",
    "Windmillville Orb Hut 2 Left Item",
    "Windmillville Orb Hut 2 Middle Item",
    "Windmillville Orb Hut 2 Right Item",
    "Bowser's Enchanted Inferno Orb Hut 1 Left Item",
    "Bowser's Enchanted Inferno Orb Hut 1 Middle Item",
    "Bowser's Enchanted Inferno Orb Hut 1 Right Item",
    "Bowser's Enchanted Inferno Orb Hut 2 Left Item",
    "Bowser's Enchanted Inferno Orb Hut 2 Middle Item",
    "Bowser's Enchanted Inferno Orb Hut 2 Right Item"
]

all_locations = coin_count_locations + space_locations + minigame_locations + board_locations + orb_hut_locations

location_name_to_id = {name: address for address, name in enumerate(all_locations, 1)}