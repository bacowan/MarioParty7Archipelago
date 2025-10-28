from Options import Toggle, PerGameCommonOptions
from dataclasses import dataclass

class DiceBlockProgression(Toggle):
    """Starts you off with a dice block that can only roll a 1. Better dice blocks are unlocked"""
    display_name = "Dice Block Progression"
    default = True

@dataclass
class MarioParty7Options(PerGameCommonOptions):
    dice_block_progression: DiceBlockProgression