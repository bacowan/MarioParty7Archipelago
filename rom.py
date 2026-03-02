import json
import os
import random
from typing import TYPE_CHECKING, Optional, List, Dict, BinaryIO

from worlds.Files import APProcedurePatch
from settings import get_settings
from .compression import lzss_decompress, lzss_compress
from .data import ASSEMBLY_OFFSETS, BOARD_SPACE_DATA, BOARD_SPACE_IDS, FILE_OFFSETS, FILE_SIZES, FST_OFFSETS, \
    SPACE_DATA_INDEXES, SHOP_STAGE_ORDER, SHOP_HUT_ORDER, SHOP_ITEM_ORDER, ITEM_NAMES_BASE_ADDRESS, MAX_ITEM_NAME_LENGTH
from .options import RandomizeBoardSpaces, DiceBlockProgression, ShopSanity
from .space_data import SpaceData

if TYPE_CHECKING:
    from . import MarioParty7World

class MarioParty7ProcedurePatch(APProcedurePatch):
    game = "Mario Party 7"
    hash = "BD367C67FCA5D93E581A43D1F61F4514"
    patch_file_ending = ".apmp7"
    result_file_ending = ".iso"

    procedure = "custom"

    @classmethod
    def get_source_data(cls) -> bytes:
        with open(get_settings().mario_party_7_settings.rom_file, "rb") as infile:
            base_rom_bytes = bytes(infile.read())

        return base_rom_bytes

    def patch(self, target: str):
        vanilla_rom = self.get_source_data()
        with open(target, 'wb') as f:
            f.write(vanilla_rom)

        patch_data = json.loads(self.get_file("data.json"))

        with open(target, 'r+b') as iso:
            unlock_boards(iso)
            if patch_data["progressive_dice_blocks"]:
                set_progressive_dice_blocks(iso)
            if patch_data["progressive_wallet"]:
                set_progressive_wallet(iso)
            if patch_data["progressive_capsule_capacity"]:
                set_progressive_capsule_capacity(iso)
            if patch_data["locked_minigame_actions"]:
                set_locked_minigame_actions(iso)
            if patch_data["minigame_sanity"]:
                set_minigame_sanity(iso)
            if patch_data["shop_sanity"]:
                set_shop_sanity(iso, patch_data["shop_items"])
            if patch_data["space_sanity"]:
                set_space_sanity(iso)
            if patch_data["board_data"] is not None:
                for (board, space_data) in patch_data["board_data"].items():
                    set_board_spaces(iso, board, space_data)

def unlock_boards(iso: BinaryIO):
    write_assembly("unlock_boards", iso)
    write_assembly("bowsers_inferno_lock_override", iso)

def set_progressive_wallet(iso: BinaryIO):
    write_assembly("max_coin_count_1_hook", iso)
    write_assembly("max_coin_count_1", iso)
    write_assembly("max_coin_count_2_hook", iso)
    write_assembly("max_coin_count_2", iso)

def set_progressive_dice_blocks(iso: BinaryIO):
    write_assembly("fix_die_max_hook", iso)
    write_assembly("fix_die_max", iso)

def set_progressive_capsule_capacity(iso: BinaryIO):
    write_assembly("max_capsule_hook", iso)
    write_assembly("max_capsule", iso)

def set_locked_minigame_actions(iso: BinaryIO):
    write_assembly("set_max_speed_hook", iso)
    write_assembly("set_max_speed", iso)
    write_assembly("lock_jump_hook", iso)
    write_assembly("lock_jump", iso)
    write_assembly("lock_jump_hook_2", iso)
    write_assembly("lock_jump_2", iso)

def set_minigame_sanity(iso: BinaryIO):
    write_assembly("fix_minigame_selection_hook", iso)
    write_assembly("fix_minigame_selection", iso)

def set_space_sanity(iso: BinaryIO):
    write_assembly("write_reached_spaces", iso)
    write_assembly("write_reached_spaces_hook", iso)

def set_shop_sanity(iso: BinaryIO, patch_items: Dict[str, tuple[str, str]]):
    write_assembly("set_shop_items_hook", iso)
    write_assembly("set_shop_items", iso)
    write_assembly("set_shop_items_hook", iso)
    write_assembly("set_shop_items", iso)

    # set item names
    item_name_offset_address = ITEM_NAMES_BASE_ADDRESS
    iso.seek(item_name_offset_address)
    item_name_offset = int.from_bytes(iso.read(4), "big")
    for stage in SHOP_STAGE_ORDER:
        for hut in SHOP_HUT_ORDER:
            for item_ordinal in SHOP_ITEM_ORDER:
                # get the name of the item and convert to bytes
                location_name = f"{stage} {hut} {item_ordinal}"
                (item_name, player) = patch_items.get(location_name)
                item_text = f"{item_name} for {player}"
                item_text = item_text[:MAX_ITEM_NAME_LENGTH]
                item_bytes = encode_text(item_text)

                # write the new data
                iso.seek(ITEM_NAMES_BASE_ADDRESS + item_name_offset)
                iso.write(item_bytes)
                iso.seek(item_name_offset_address)
                iso.write(item_name_offset.to_bytes(4, "big"))

                # update the pointers
                item_name_offset_address += 4
                item_name_offset += len(item_bytes) + (4 - len(item_bytes) % 4)

CUSTOM_ENCODINGS = {
    "\n": 0xC2,
    " ": 0x10,
    "-": 0x3D
}
def encode_text(text: str) -> bytes:
    res = bytearray([0x00, 0xFF, 0x00, 0xFF])
    for char in text:
        if char in CUSTOM_ENCODINGS:
            res.append(CUSTOM_ENCODINGS[char])
        else:
            res.append(ord(char))
    res.append(0xFF)
    return res


def set_board_spaces(iso: BinaryIO, board: str, space_data: List[int]):
    # load compressed data and decompress
    file_offset = FILE_OFFSETS[board]
    file_size = FILE_SIZES[board]
    iso.seek(file_offset)
    section_count = int.from_bytes(iso.read(4), "big")
    iso.seek(file_offset + SPACE_DATA_INDEXES[board] * 4 + 4)
    space_section_offest = int.from_bytes(iso.read(4), "big")
    if SPACE_DATA_INDEXES[board] == section_count - 1:
        next_section_offset = file_size
    else:
        next_section_offset = int.from_bytes(iso.read(4), "big")
    iso.seek(file_offset + space_section_offest)
    decompressed_size = int.from_bytes(iso.read(4), "big")
    iso.read(4) # this word is the compression type; for space data it should be lzss
    compressed_space_data = iso.read(next_section_offset - space_section_offest - 8)
    decompressed_data = lzss_decompress(compressed_space_data, decompressed_size)

    # update space types
    structured_space_data = SpaceData.from_binary(decompressed_data)
    space_index = 0
    for space in structured_space_data.spaces:
        if space.get_color() in BOARD_SPACE_IDS.values():
            space.set_color(space_data[space_index])
            space_index += 1

    # recompress
    recompressed_space_data = lzss_compress(structured_space_data.to_binary())
    size_diff = len(recompressed_space_data) - len(compressed_space_data)
    # add a padding byte if the section size isn't a multiple of 2
    size_diff += size_diff % 2

    # if the size has increased, we need to move the file to the end of the iso
    if size_diff > 0:
        # move the file
        iso.seek(file_offset)
        file_data = iso.read(file_size)
        iso.seek(0, 2)  # 2 = SEEK_END
        new_file_offset = iso.tell()
        iso.write(file_data)

        # TODO: zero out old data? Is it necessary?

        # update section offsets of everything after the changed section
        iso.seek(new_file_offset)
        section_count = int.from_bytes(iso.read(4), "big")
        for i in range(SPACE_DATA_INDEXES[board] + 1, section_count):
            iso.seek(new_file_offset + i * 4 + 4)
            section_offset = int.from_bytes(iso.read(4), "big")
            new_section_offset = section_offset + size_diff
            iso.seek(new_file_offset + i * 4 + 4)
            iso.write(new_section_offset.to_bytes(4, byteorder='big'))

        # shift data
        iso.seek(new_file_offset + next_section_offset)
        remaining_data = iso.read() # just read everything until the end of the file
        iso.seek(new_file_offset + next_section_offset + size_diff)
        iso.write(remaining_data)
        iso.flush()

        # update the FST
        iso.seek(FST_OFFSETS[board] + 4)
        iso.write(new_file_offset.to_bytes(4, byteorder='big'))
        iso.write((file_size + size_diff).to_bytes(4, byteorder='big'))

        file_offset = new_file_offset

    # write new data
    iso.seek(file_offset + space_section_offest + 8)
    iso.write(recompressed_space_data)
    iso.flush()

    # make sure the file has a multiple of 16 bytes
    iso.seek(0, 2)
    new_iso_size = iso.tell()
    iso.write(b'\x00' * (16 - (new_iso_size % 16)))
    iso.flush()

def load_assembly(bin_name: str) -> bytes:
    with open(os.path.join(os.path.dirname(__file__), "assembly", "bin", bin_name), "rb") as binary_file:
        return binary_file.read()

def write_assembly(bin_name: str, iso: BinaryIO):
    assembly_offset = ASSEMBLY_OFFSETS[bin_name]
    if isinstance(assembly_offset, int):
        iso.seek(assembly_offset)
        iso.write(load_assembly(bin_name))
    else:
        for offset in assembly_offset:
            iso.seek(offset)
            iso.write(load_assembly(bin_name))

def randomize_board(board_name: str, is_balanced: bool) -> List[int]:
    board_data = BOARD_SPACE_DATA[board_name]
    if is_balanced:
        new_board_data = dict(board_data)

        res = []
        for key, value in new_board_data.items():
            res.extend([BOARD_SPACE_IDS[key]] * value)
        random.shuffle(res)
        return res
    else:
        total_spaces = sum(board_data.values())
        new_space_values = [int(random.random() * 6) for _ in range(total_spaces)]
        # make sure there's always at least one
        if BOARD_SPACE_IDS["duel"] not in new_space_values:
            new_space_values[random.randint(0, total_spaces - 1)] = BOARD_SPACE_IDS["duel"]
        res = [list(BOARD_SPACE_IDS.values())[x] for x in new_space_values]

    return res



def write_json(world: "MarioParty7World", patch: MarioParty7ProcedurePatch) -> None:
    boards: Optional[Dict[str, List[int]]] = None
    if world.options.randomize_board_spaces != RandomizeBoardSpaces.option_off:
        is_balanced = world.options.randomize_board_spaces == RandomizeBoardSpaces.option_balanced
        boards = {
            "grand_canal": randomize_board("grand_canal", is_balanced),
            "pagoda_peak": randomize_board("pagoda_peak", is_balanced),
            "pyramid_park": randomize_board("pyramid_park", is_balanced),
            "windmillville": randomize_board("windmillville", is_balanced),
            "neon_heights": randomize_board("neon_heights", is_balanced),
            "bowsers_enchanted_inferno": randomize_board("bowsers_enchanted_inferno", is_balanced)
        }

    shop_items: Optional[Dict[str, (str, str)]] = None
    if world.options.shop_sanity == ShopSanity.option_true:
        shop_items = {}
        location_names = []
        for stage in SHOP_STAGE_ORDER:
            for hut in SHOP_HUT_ORDER:
                for item in SHOP_ITEM_ORDER:
                    location_names.append(f"{stage} {hut} {item}")
        for location in world.multiworld.get_locations(world.player):
            if location.name in location_names:
                player_name = "You" if location.item.player == world.player else world.multiworld.worlds[location.item.player].player_name
                shop_items[location.name] = (location.item.name, player_name)

    patch_data = {
        "progressive_dice_blocks": world.options.dice_block_progression == DiceBlockProgression.option_true,
        "progressive_wallet": world.options.wallet_progression.value,
        "progressive_capsule_capacity": world.options.capsule_capacity_progression.value,
        "locked_minigame_actions": world.options.locked_minigame_actions.value,
        "minigame_sanity": world.options.minigame_sanity.value,
        "shop_sanity": world.options.shop_sanity.value,
        "space_sanity": world.options.space_sanity.value,
        "board_data": boards,
        "shop_items": shop_items,
    }

    patch.write_file("data.json", json.dumps(patch_data).encode())