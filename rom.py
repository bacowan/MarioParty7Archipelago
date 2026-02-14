import os
from typing import TYPE_CHECKING


from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes
from settings import get_settings
from .data import ASSEMBLY_OFFSETS

if TYPE_CHECKING:
    from . import MarioParty7World

class MarioParty7ProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "Mario Party 7"
    hash = "BD367C67FCA5D93E581A43D1F61F4514"
    patch_file_ending = ".apmp7"
    result_file_ending = ".iso"

    procedure = [
        ("apply_tokens", ["token_data.bin"])
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        with open(get_settings().mario_party_7_settings.rom_file, "rb") as infile:
            base_rom_bytes = bytes(infile.read())

        return base_rom_bytes

def load_assembly(bin_name: str) -> bytes:
    with open(os.path.join(os.path.dirname(__file__), "assembly", "bin", bin_name), "rb") as binary_file:
        return binary_file.read()

def write_tokens(world: "MarioParty7World", patch: MarioParty7ProcedurePatch) -> None:
    with open(os.path.join(os.path.dirname(__file__), "assembly", "assembly_offsets.csv"), "r") as csv_file:
        if world.options.dice_block_progression:
            patch.write_token(
                APTokenTypes.WRITE,
                ASSEMBLY_OFFSETS["fix_die_max_hook"],
                load_assembly("fix_die_max_hook")
            )
            patch.write_token(
                APTokenTypes.WRITE,
                ASSEMBLY_OFFSETS["fix_die_max"],
                load_assembly("fix_die_max")
            )

    patch.write_file("token_data.bin", patch.get_token_binary())