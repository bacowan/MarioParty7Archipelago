from typing import TYPE_CHECKING

from worlds.Files import APProcedurePatch, APTokenMixin
from settings import get_settings

if TYPE_CHECKING:
    from . import MarioParty7World

class MarioParty7ProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "Mario Party 7"
    hash = "BD367C67FCA5D93E581A43D1F61F4514"
    patch_file_ending = ".apmp7"
    result_file_ending = ".iso"

    @classmethod
    def get_source_data(cls) -> bytes:
        with open(get_settings().mario_party_7_settings.rom_file, "rb") as infile:
            base_rom_bytes = bytes(infile.read())

        return base_rom_bytes

def write_tokens(world: "MarioParty7World", patch: MarioParty7ProcedurePatch) -> None:
    pass