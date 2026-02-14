import settings
from worlds.mp7.rom import MarioParty7ProcedurePatch


class MarioParty7Settings(settings.Group):
    class MarioParty7RomFile(settings.UserFilePath):
        """File name of your English Mario Party 7 ROM"""
        description = "Mario Party 7 ROM File"
        copy_to = "Mario Party 7 (USA) (Rev 1).iso"
        md5s = [MarioParty7ProcedurePatch.hash]

    rom_file: MarioParty7RomFile = MarioParty7RomFile(MarioParty7RomFile.copy_to)