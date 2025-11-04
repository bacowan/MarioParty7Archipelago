from Options import Toggle, PerGameCommonOptions
from dataclasses import dataclass

class DiceBlockProgression(Toggle):
    """Starts you off with a dice block that can only roll a 1. Better dice blocks are unlocked as items"""
    display_name = "Dice Block Progression"
    default = True

class MinigameSanity(Toggle):
    """Each minigame is its own check. Only one minigame is unlocked to begin with, and further
    minigames are unlocked via checks"""
    display_name = "Minigame Sanity"
    default = True

@dataclass
class MarioParty7Options(PerGameCommonOptions):
    dice_block_progression: DiceBlockProgression
    minigame_sanity: MinigameSanity