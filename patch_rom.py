import csv
import os

import Utils
from typing import NamedTuple, IO

class Instructions(NamedTuple):
    start_address: int
    instructions: list[int]

# DOL File Format
# see https://wiibrew.org/wiki/DOL
DOL_TEXT_OFFSETS_OFFSET = 0x0 # Where the Text offset data starts in the DOL
DOL_TEXT_OFFSET_SIZE = 0x4 # Size of each Text offset
DOL_TEXT_LOADING_ADDRESS_OFFSET = 0x48 # Where the text loading addresses are offset in the DOL
DOL_TEXT_LOADING_ADDRESS_SIZE = 0x4 # Size of each text loading address
DOL_DATA_OFFSETS_OFFSET = 0x1C # Where the data offset data starts in the DOL
DOL_DATA_OFFSET_SIZE = 0x4 # Size of each data offset
DOL_DATA_OFFSET_COUNT = 11 # Number of slots for data offsets
DOL_SECTION_SIZE_OFFSET = 0x90 # Where the section sizes are offset in the DOL
DOL_SECTION_SIZE_SIZE = 0x4 # Size of each section size
DOL_BSS_ADDRESS_OFFSET = 0xD8
DOL_BSS_ADDRESS_SIZE = 0x4
DOL_BSS_SIZE_OFFSET = 0xDC
DOL_BSS_SIZE_SIZE = 0x4

# FST
FST_OFFSET_OFFSET = 0x424
FST_SIZE_OFFSET = 0x428
FST_ENTRY_SIZE = 0xC
FST_ENTRY_FILE_OFFSET_OFFSET = 0x4
FST_ENTRY_FILE_OFFSET_SIZE = 0x4
FST_ENTRY_NEXT_INDEX_OFFSET = 0x08
FST_ENTRY_NEXT_INDEX_SIZE = 0x4

# Values specific to Mario Party 7
DOL_OFFSET = 0x00020300 # Where the DOL starts in the ISO
DOL_SIZE = 0x279580
INITIAL_DATA_OFFSET = 0x23C780
FST_OFFSET = 0x299900
FST_SIZE = 0x51FA
INITIAL_BSS_ADDRESS = 0x80277980
INITIAL_BSS_SIZE = 0x80610

GAME_ID = b"GP7E01"
OUTPUT_FILE_NAME = "MarioParty7_patched.iso"
BSS_SIZE_INCREASE = 0x10 # RAM used for our hack
INJECTED_CODE_LOCATION = 0x802F8000



def apply_patches(iso_file: IO):
    with open(os.path.join(os.path.dirname(__file__), "assembly", "assembly_offsets.csv"), "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            with open(os.path.join(os.path.dirname(__file__), "assembly", "bin", row["filename"]), "rb") as binary_file:
                code_bytes = binary_file.read()
                iso_file.seek(int(row["iso_offset"], 16))
                iso_file.write(code_bytes)

def main():
    iso_path = Utils.open_filename("Path to ISO to patch", [("ISO", [".iso"])])
    if iso_path == "":
        return

    with open(iso_path, "r+b") as iso_file:
        if iso_file.read(6) != GAME_ID:
            Utils.messagebox("Error", "Not a valid Mario Party 7 ROM", True)
        else:
            iso_file.seek(0)
            apply_patches(iso_file)

if __name__ == "__main__":
    main()