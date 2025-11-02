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
DOL_TEXT_LOADING_ADDRESS_OFFSET = 0x4C # Where the text loading addresses are offset in the DOL
DOL_TEXT_LOADING_ADDRESS_SIZE = 0x4 # Size of each text loading address
DOL_DATA_OFFSETS_OFFSET = 0x1C # Where the data offset data starts in the DOL
DOL_DATA_OFFSET_SIZE = 0x4 # Size of each data offset
DOL_DATA_OFFSET_COUNT = 11 # Number of slots for data offsets
DOL_SECTION_SIZE_OFFSET = 0x90 # Where the section sizes are offset in the DOL
DOL_SECTION_SIZE_SIZE = 0x4 # Size of each section size

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
INITIAL_DATA_OFFSET = 0x23C780
FST_OFFSET = 0x299900
FST_SIZE = 0x51FA

GAME_ID = b"GP7E01"

OUTPUT_FILE_NAME = "MarioParty7_patched.iso"

def overwrite_assembly(input_file: IO, output_file: IO):
    # Load the binary to append
    for binary in os.listdir(os.path.join(os.path.dirname(__file__), "assembly", "bin")):
        pass

def append_assembly(input_file: IO, output_file: IO):
    pass

def apply_patches(input_file: IO, output_file: IO):
    # Start by copying everything up until the end of the dol code
    output_file.write(input_file.read(INITIAL_DATA_OFFSET))

    # Append the new code
    binary_code_file_path = os.path.join(os.path.dirname(__file__), "assembly", "bin", "appended_code")
    new_code_size = os.path.getsize(binary_code_file_path)
    new_code_size = new_code_size + (0x20 - (new_code_size % 0x20)) # things should be 0x20 aligned
    new_code_size_bytes = new_code_size.to_bytes(DOL_DATA_OFFSET_SIZE, byteorder="big")
    # with (open(binary_code_file_path, "rb")) as new_code_file:
    #     output_file.write(new_code_file.read())

    # append the rest of the iso
    input_file.seek(INITIAL_DATA_OFFSET)
    output_file.seek(INITIAL_DATA_OFFSET + new_code_size)
    output_file.write(input_file.read())

    # update the dol with the new code offsets and new data offsets
    # # text offset
    # text_section_ordinal = 2 # In Mario Party 7, only text sections 0 and 1 are in use, so we'll hijack section 2
    # output_file.seek(DOL_OFFSET + DOL_TEXT_OFFSETS_OFFSET + DOL_TEXT_OFFSET_SIZE * text_section_ordinal)
    # output_file.write(INITIAL_DATA_OFFSET.to_bytes(4, byteorder="big"))
    #
    # # text size
    # output_file.seek(DOL_OFFSET + DOL_SECTION_SIZE_OFFSET + DOL_SECTION_SIZE_SIZE * text_section_ordinal)
    # output_file.write(new_code_size.to_bytes(4, byteorder="big"))

    # go through each data offset and increment it to match the new offset
    for i in range(0, DOL_DATA_OFFSET_COUNT):
        data_offset_offset = DOL_OFFSET + DOL_DATA_OFFSETS_OFFSET + DOL_DATA_OFFSET_SIZE * i
        input_file.seek(data_offset_offset)
        data_offset_bytes = input_file.read(DOL_DATA_OFFSET_SIZE)
        data_offset = int.from_bytes(data_offset_bytes, byteorder="big", signed=False)
        if data_offset != 0:
            output_file.seek(data_offset_offset)
            output_file.write((data_offset + new_code_size).to_bytes(DOL_DATA_OFFSET_SIZE, byteorder="big"))

    # update the FST pointer in the same way
    new_fst_offset = FST_OFFSET + new_code_size
    output_file.seek(FST_OFFSET_OFFSET)
    output_file.write(new_fst_offset.to_bytes(4, byteorder="big"))

    # update all the FST file offsets that have moved

    # the first entry is the root directory and tells us where its last child is
    output_file.seek(new_fst_offset + FST_ENTRY_NEXT_INDEX_OFFSET)
    last_index_bytes = output_file.read(FST_ENTRY_NEXT_INDEX_SIZE)
    last_index = int.from_bytes(last_index_bytes, byteorder="big", signed=False)

    for fst_entry_offset in range(new_fst_offset + FST_ENTRY_SIZE, new_fst_offset + last_index, FST_ENTRY_SIZE):
        output_file.seek(fst_entry_offset)
        fst_entry = output_file.read(FST_ENTRY_SIZE)
        is_file = fst_entry[0] & 0x01 == 0 # the last bit of the first byte indicates if the entry is a file or a folder
        if is_file:
            offset = int.from_bytes(
                fst_entry[FST_ENTRY_FILE_OFFSET_OFFSET:FST_ENTRY_FILE_OFFSET_OFFSET + FST_ENTRY_FILE_OFFSET_SIZE],
                byteorder="big",
                signed=False) # bytes 4-8 represent the file offset
            if offset > INITIAL_DATA_OFFSET:
                output_file.seek(fst_entry_offset + FST_ENTRY_FILE_OFFSET_OFFSET)
                output_file.write((offset + new_code_size).to_bytes(FST_ENTRY_FILE_OFFSET_SIZE, byteorder="big"))

def main():
    iso_path = Utils.open_filename("Path to unpatched ISO", [("ISO", [".iso"])])
    if iso_path == "":
        return
    output_directory = Utils.open_directory("Directory to output patched ISO")
    if output_directory == "":
        return
    output_path = os.path.join(output_directory, OUTPUT_FILE_NAME)
    if os.path.exists(output_path):
        os.remove(output_path)

    with (
        open(iso_path, "rb") as input_file,
        open(os.path.join(output_directory, OUTPUT_FILE_NAME), "w+b") as output_file,
    ):
        if input_file.read(6) != GAME_ID:
            Utils.messagebox("Error", "Not a valid Mario Party 7 ROM", True)
        else:
            input_file.seek(0)
            apply_patches(input_file, output_file)

if __name__ == "__main__":
    main()