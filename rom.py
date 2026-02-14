import json
import os
import random
from typing import TYPE_CHECKING, Optional, List, Dict

from worlds.Files import APProcedurePatch, APTokenTypes
from settings import get_settings
from .data import ASSEMBLY_OFFSETS, BOARD_SPACE_DATA, BOARD_SPACE_IDS
from .options import RandomizeBoardSpaces, DiceBlockProgression
from .patch_data import PatchData, BoardData

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

            if patch_data["progressive_dice_blocks"]:
                self.set_progressive_dice_blocks(iso)

    def set_progressive_dice_blocks(self, iso):
        iso.seek(ASSEMBLY_OFFSETS["fix_die_max_hook"])
        iso.write(load_assembly("fix_die_max_hook"))

        iso.seek(ASSEMBLY_OFFSETS["fix_die_max"])
        iso.write(load_assembly("fix_die_max"))


def load_assembly(bin_name: str) -> bytes:
    with open(os.path.join(os.path.dirname(__file__), "assembly", "bin", bin_name), "rb") as binary_file:
        return binary_file.read()

def randomize_board(board_name: str, is_balanced: bool) -> List[int]:
    board_data = BOARD_SPACE_DATA[board_name]
    if is_balanced:
        new_board_data = dict(board_data)
        new_board_data["duel"] -= 1 # one duel space will be manually inserted
    else:
        total_spaces = sum(board_data.values())
        new_space_counts = [int(random.random() * 6) + 1 for _ in range(total_spaces)]
        new_board_data = {
            "blue": new_space_counts[0],
            "red": new_space_counts[1],
            "mic": new_space_counts[2],
            "duel": new_space_counts[3],
            "dk": new_space_counts[4],
            "bowser": new_space_counts[5]
        }

    res = []
    for key, value in new_board_data.items():
        res.extend([BOARD_SPACE_IDS[key]] * value)
    random.shuffle(res)
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

    patch_data = {
        "progressive_dice_blocks": world.options.dice_block_progression == DiceBlockProgression.option_true,
        "board_data": boards
    }

    patch.write_file("data.json", json.dumps(patch_data).encode())


    # if world.options.dice_block_progression:
    #     patch.write_token(
    #         APTokenTypes.WRITE,
    #         ASSEMBLY_OFFSETS["fix_die_max_hook"],
    #         load_assembly("fix_die_max_hook")
    #     )
    #     patch.write_token(
    #         APTokenTypes.WRITE,
    #         ASSEMBLY_OFFSETS["fix_die_max"],
    #         load_assembly("fix_die_max")
    #     )