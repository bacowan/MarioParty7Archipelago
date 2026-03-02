from typing import Dict, List

CAPSULE_IDS = [
    0x0,
    0x1,
    0x2,
    0x3,
    0x4,
    0x5,
    0x6,
    0x7,
    0xA,
    0xB,
    0xC,
    0xD,
    0xE,
    0xF,
    0x10,
    0x14,
    0x15,
    0x16,
    0x17,
    0x18,
    0x19,
    0x1E,
    0x1F,
    0x20,
    0x21,
    0x22,
    0x23,
]

SPACE_TYPES = {
    "blue": 1,
    "red": 2,
    "question": 3,
    "bowser": 4,
    "duel": 5,
    "dk": 6,
    "mic": 11
}

# the board files are split into sub-files. The data for what spaces are what colour is in the 3rd file
SPACE_DATA_INDEXES: Dict[str, int] = {
    "grand_canal":                  42,
    "pagoda_peak":                  2,
    "pyramid_park":                 60,
    "windmillville":                1,
    "neon_heights":                 1,
    "bowsers_enchanted_inferno":    1,
}

ASSEMBLY_OFFSETS: Dict[str, int | List[int]] = {
    "fix_die_max_hook":                 0x001A_9D24,
    "fix_die_max":                      0x0002_0924,
    "max_coin_count_1_hook":            0x0018_3D70,
    "max_coin_count_1":                 0x0002_09B8,
    "max_coin_count_2_hook":            0x0005_BF34,
    "max_coin_count_2":                 0x0002_0A44,
    "max_capsule_hook":                 0x0018_4658,
    "max_capsule":                      0x0002_21C0,
    "set_max_speed_hook":               0x0009_D728,
    "set_max_speed":                    0x0002_2520,
    "lock_jump_hook":                   0x000E_4ECC,
    "lock_jump":                        0x0002_23B8,
    "lock_jump_hook_2":                 0x000B_F7D0,
    "lock_jump_2":                      0x0002_242C,
    "unlock_boards":                    [0x349B_D26C, 0x349B_D95C],
    "bowsers_inferno_lock_override":    [0x349B_D300, 0x349B_D9F0],
    "fix_minigame_selection_hook":      0x0023_D6B8,
    "fix_minigame_selection":           0x0002_2034,
    "set_shop_items_hook":              0x0023_4234,
    "set_shop_items":                   0x0002_2204,
    "write_reached_spaces_hook":        0x0017_A604,
    "write_reached_spaces":             0x0002_1D30,
    "set_bought_item":                  0x0002_1230,
    "set_bought_item_hook":             0x0018_4748,
}

FST_OFFSETS: Dict[str, int] = {
    "grand_canal":                  0x29A4D0,
    "pagoda_peak":                  0x29A4DC,
    "pyramid_park":                 0x29A4E8,
    "windmillville":                0x29A4F4,
    "neon_heights":                 0x29A500,
    "bowsers_enchanted_inferno":    0x29A50C,
}

FILE_OFFSETS: Dict[str, int] = {
    "grand_canal":                  0x4EEC7140,
    "pagoda_peak":                  0x4EF67644,
    "pyramid_park":                 0x4F086860,
    "windmillville":                0x4F19B3E4,
    "neon_heights":                 0x4F24C2B4,
    "bowsers_enchanted_inferno":    0x4F36C4F4,
}

FILE_SIZES: Dict[str, int] = {
    "grand_canal":                  0x0A0502,
    "pagoda_peak":                  0x11F21C,
    "pyramid_park":                 0x114B84,
    "windmillville":                0x0B0ECE,
    "neon_heights":                 0x12023E,
    "bowsers_enchanted_inferno":    0x13034C,
}

BOARD_SPACE_IDS: Dict[str, int] = {
    "blue":     0x01,
    "red":      0x02,
    "mic":      0x0B,
    "duel":     0x05,
    "dk":       0x06,
    "bowser":   0x04
}

BOARD_SPACE_DATA: Dict[str, Dict[str, int]] = {
    "grand_canal": {
        "blue": 36,
        "red": 8,
        "mic": 3,
        "duel": 7,
        "dk": 3,
        "bowser": 3
    },
    "pagoda_peak": {
        "blue": 18,
        "red": 3,
        "mic": 3,
        "duel": 6,
        "dk": 3,
        "bowser": 3
    },
    "pyramid_park": {
        "blue": 37,
        "red": 8,
        "mic": 3,
        "duel": 7,
        "dk": 3,
        "bowser": 3
    },
    "windmillville": {
        "blue": 38,
        "red": 10,
        "mic": 3,
        "duel": 6,
        "dk": 3,
        "bowser": 3
    },
    "neon_heights": {
        "blue": 36,
        "red": 5,
        "mic": 4,
        "duel": 8,
        "dk": 3,
        "bowser": 4
    },
    "bowsers_enchanted_inferno": {
        "blue": 10,
        "red": 6,
        "mic": 2,
        "duel": 7,
        "dk": 2,
        "bowser": 0
    }
}

# relevant stage spaces for space sanity. Includes all actual "spaces" (i.e. not orb spaces, junctions, etc.)
GRAND_CANAL_SPACE_IDS = [0x0, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9, 0xa, 0xb, 0xc, 0xd, 0xe, 0xf, 0x11, 0x14, 0x15, 0x17, 0x18, 0x1a, 0x1c, 0x1d, 0x1e, 0x1f, 0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x27, 0x28, 0x29, 0x2b, 0x2d, 0x2e, 0x2f, 0x30, 0x32, 0x34, 0x36, 0x37, 0x38, 0x3b, 0x3f, 0x40, 0x41, 0x42, 0x43, 0x44, 0x45, 0x54, 0x55, 0x56, 0x57, 0x58, 0x59, 0x5a, 0x5b, 0x5c, 0x5d, 0x5e, 0x5f, 0x60, 0x6e, 0x6f]
PAGODA_PEAK_SPACE_IDS = [0x0, 0x1, 0x2, 0x3, 0x5, 0x6, 0x7, 0xa, 0xb, 0xc, 0xd, 0xe, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x19, 0x1a, 0x1b, 0x1f, 0x23, 0x25, 0x26, 0x27, 0x28, 0x29, 0x2a, 0x2b, 0x2c, 0x2d, 0x2e, 0x2f, 0x31, 0x32, 0x33, 0x40, 0x4b]
PYRAMID_PARK_SPACE_IDS = [0x0, 0x1, 0x2, 0x3, 0x5, 0x6, 0x9, 0xa, 0xc, 0xe, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x19, 0x1c, 0x1f, 0x20, 0x21, 0x23, 0x24, 0x25, 0x26, 0x27, 0x2a, 0x2d, 0x2e, 0x2f, 0x30, 0x31, 0x32, 0x33, 0x35, 0x36, 0x38, 0x39, 0x3a, 0x3b, 0x3c, 0x3d, 0x3f, 0x41, 0x43, 0x44, 0x45, 0x46, 0x48, 0x49, 0x4a, 0x4b, 0x4d, 0x4f, 0x50, 0x51, 0x58, 0x59, 0x5d, 0x60, 0x62, 0x63, 0x64, 0x69, 0x76]
WINDMILLVILLE_SPACE_IDS = [0x0, 0x1, 0x2, 0x3, 0x5, 0x6, 0x9, 0xa, 0xc, 0xe, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x19, 0x1c, 0x1f, 0x20, 0x21, 0x23, 0x24, 0x25, 0x26, 0x27, 0x2a, 0x2d, 0x2e, 0x2f, 0x30, 0x31, 0x32, 0x33, 0x35, 0x36, 0x38, 0x39, 0x3a, 0x3b, 0x3c, 0x3d, 0x3f, 0x41, 0x43, 0x44, 0x45, 0x46, 0x48, 0x49, 0x4a, 0x4b, 0x4d, 0x4f, 0x50, 0x51, 0x58, 0x59, 0x5d, 0x60, 0x62, 0x63, 0x64, 0x69, 0x76]
NEON_HEIGHTS_SPACE_IDS = [0x0, 0x1, 0x2, 0x4, 0x5, 0x6, 0x7, 0xa, 0xb, 0xc, 0xe, 0xf, 0x10, 0x11, 0x12, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1b, 0x1c, 0x1d, 0x1e, 0x1f, 0x20, 0x21, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x29, 0x2a, 0x2b, 0x2c, 0x2d, 0x2e, 0x2f, 0x32, 0x33, 0x34, 0x36, 0x37, 0x38, 0x39, 0x3a, 0x3c, 0x3d, 0x3e, 0x3f, 0x40, 0x41, 0x42, 0x43, 0x45, 0x48, 0x4f, 0x78, 0x88, 0x89]
BOWSERS_ENCHANTED_INFERNO = [0x1, 0x2, 0x5, 0x6, 0x8, 0xa, 0xb, 0xc, 0xe, 0xf, 0x11, 0x12, 0x13, 0x15, 0x16, 0x18, 0x1a, 0x1c, 0x1e, 0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x2a, 0x2b, 0x2c, 0x2d, 0x2e, 0x2f, 0x30, 0x33, 0x34, 0x36, 0x39, 0x45, 0x5f, 0x62, 0x70]

# we use the duty-free shop text for archipelago item names
SHOP_STAGE_ORDER =          ["Grand Canal", "Pagoda Peak", "Neon Heights", "Windmillville", "Bowser's Enchanted Inferno"]
SHOP_HUT_ORDER =            ["Orb Hut 1", "Orb Hut 2"]
SHOP_ITEM_ORDER =           ["Left Item", "Middle Item", "Right Item"]
MAX_ITEM_NAME_LENGTH =      360 # based on the total space for text in this area averaged over 36 items (conservative estimate)

# RAM Map
ITEM_NAMES_BASE_ADDRESS =       0x4CEB2028
RAM_LOCATION_P1_INFO =          0x80290c98
RAM_LOCATION_P2_INFO =          0x80290da8

RAM_LOCATION_GRAND_CANAL_BEATEN_FLAG =                  0x80529ec3
RAM_LOCATION_PAGODA_PEAK_BEATEN_FLAG =                  0x80529ec4
RAM_LOCATION_PYRAMID_PARK_BEATEN_FLAG =                 0x80529ec5
RAM_LOCATION_WINDMILLVILLE_BEATEN_FLAG =                0x80529ec6
RAM_LOCATION_NEON_HEIGHTS_BEATEN_FLAG =                 0x80529ec7
RAM_LOCATION_BOWSERS_ENCHANTED_INFERNO_BEATEN_FLAG =    0x80529ec8

# ap save data locations
RAM_LOCATION_MAX_DICE_BLOCK =                           0x8029D70A
RAM_LOCATION_COMPLETED_MINIGAMES =                      0x8029D70B
RAM_LOCATION_LOCK_JUMP =                                0x8029D70D
RAM_LOCATION_MAX_CAPSULES =                             0x8029D70E
RAM_LOCATION_MAX_WALLET =                               0x8029D70F
RAM_LOCATION_MAX_SPEED =                                0x8029D710
RAM_LOCATION_BOUGHT_ITEMS =                             0x8029D711
RAM_LOCATION_GRAND_CANAL_UNLOCK =                       0x8029D715
RAM_LOCATION_PAGODA_PEAK_UNLOCK =                       0x8029D716
RAM_LOCATION_PYRAMID_PARK_UNLOCK =                      0x8029D717
RAM_LOCATION_WINDMILLVILLE_UNLOCK =                     0x8029D718
RAM_LOCATION_NEON_HEIGHTS_UNLOCK =                      0x8029D719
RAM_LOCATION_BOWSERS_ENCHANTED_INFERNO_UNLOCK =         0x8029D71A
RAM_LOCATION_GRAND_CANAL_REACHED_SPACES =               0x8029D71B
RAM_LOCATION_PAGODA_PEAK_REACHED_SPACES =               0x8029D72A
RAM_LOCATION_PYRAMID_PARK_REACHED_SPACES =              0x8029D735
RAM_LOCATION_WINDMILLVILLE_REACHED_SPACES =             0x8029D745
RAM_LOCATION_NEON_HEIGHTS_REACHED_SPACES =              0x8029D755
RAM_LOCATION_BOWSERS_ENCHANTED_INFERNO_REACHED_SPACES = 0x8029D767

# Data structure info
COIN_OFFSET_FROM_PLAYER_LOCATION =      0x26
CAPSULE_OFFSET_FROM_PLAYER_LOCATION =   0x6

BEATEN_MINIGAME_SAVE_ORDER = ["warp pipe dreams", "weight for it", "mad props", "gimme a sign", "bridge work",
                              "spin doctor", "hip hop drop", "royal rumpus", "light speed", "apes of wrath",
                              "fish and cheeps", "camp ukiki"]