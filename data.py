from typing import Dict

ASSEMBLY_OFFSETS: Dict[str, int] = {
    "fix_die_max_hook":     0x001A_9D24,
    "fix_die_max":          0x0002_0924
}

BOARD_SPACE_IDS: Dict[str, int] = {
    "blue": 1,
    "red": 2,
    "mic": 3,
    "duel": 5,
    "dk": 6,
    "bowser": 4
}

BOARD_SPACE_DATA: Dict[str, Dict[str, int]] = {
    "grand_canal": {
        "blue": 47,
        "red": 10,
        "mic": 2,
        "duel": 2,
        "dk": 2,
        "bowser": 0
    },
    "pagoda_peak": {
        "blue": 23,
        "red": 5,
        "mic": 2,
        "duel": 3,
        "dk": 4,
        "bowser": 1
    },
    "pyramid_park": {
        "blue": 45,
        "red": 9,
        "mic": 3,
        "duel": 5,
        "dk": 2,
        "bowser": 2
    },
    "windmillville": {
        "blue": 45,
        "red": 7,
        "mic": 2,
        "duel": 4,
        "dk": 2,
        "bowser": 2
    },
    "neon_heights": {
        "blue": 46,
        "red": 10,
        "mic": 2,
        "duel": 3,
        "dk": 2,
        "bowser": 2
    },
    "bowsers_enchanted_inferno": {
        "blue": 32,
        "red": 9,
        "mic": 2,
        "duel": 1,
        "dk": 1,
        "bowser": 0
    }
}