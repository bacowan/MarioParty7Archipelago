from typing import Dict

# the board files are split into sub-files. The data for what spaces are what colour is in the 3rd file
SPACE_DATA_INDEXES: Dict[str, int] = {
    "grand_canal":                  42,
    "pagoda_peak":                  2,
    "pyramid_park":                 60,
    "windmillville":                1,
    "neon_heights":                 1,
    "bowsers_enchanted_inferno":    1,
}

ASSEMBLY_OFFSETS: Dict[str, int] = {
    "fix_die_max_hook":     0x001A_9D24,
    "fix_die_max":          0x0002_0924
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
    "windmillville":                0x4F24C2B4,
    "neon_heights":                 0x4F19B3E4,
    "bowsers_enchanted_inferno":    0x4F36C4F4,
}

FILE_SIZES: Dict[str, int] = {
    "grand_canal":                  0x0A0502,
    "pagoda_peak":                  0x11F21C,
    "pyramid_park":                 0x114B84,
    "windmillville":                0x12023E,
    "neon_heights":                 0x0B0ECE,
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
        "blue": 36,
        "red": 5,
        "mic": 4,
        "duel": 8,
        "dk": 3,
        "bowser": 4
    },
    "neon_heights": {
        "blue": 38,
        "red": 10,
        "mic": 3,
        "duel": 6,
        "dk": 3,
        "bowser": 3
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