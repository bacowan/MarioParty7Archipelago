from Options import Toggle, PerGameCommonOptions, Choice
from dataclasses import dataclass

class DiceBlockProgression(Toggle):
    """Starts you off with a dice block that can only roll a 1. Better dice blocks are unlocked as items"""
    display_name = "Dice Block Progression"
    default = True

class WalletProgression(Choice):
    """You have a "wallet" that indicates the max number of coins you can carry.
    Easy has wallet sizes of 30, 50, 100, and 999
    Medium has wallet sizes of 0, 20, 50, 100, and 999
    Hard has wallet sizes of 0, 5, 10, 20, 50, 100, and 999
    Off has only a wallet of 999"""
    display_name = "Wallet Progression"
    default = 0
    option_off = 0
    option_easy = 1
    option_medium = 2
    option_hard = 3

class CapsuleCapacityProgression(Toggle):
    """If enabled, you can't carry any capsules unless you unlock the ability to carry 1, 2 or 3 of them"""
    display_name = "Capsule Capacity Progression"
    default = False

class LockedMenuNavigation(Toggle):
    """The ability to navigate menus in: shops, star purchases, and board events are each locked behind checks"""
    display_name = "Locked Menu Navigation"
    default = False

class LockedMinigameActions(Toggle):
    """Certain abilities in minigames will not work unless they are unlocked"""
    display_name = "Locked Minigame Actions"
    default = True

class CoinCountsAsChecks(Toggle):
    """Having 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 150, and 200 coins at any given time are all checks"""
    display_name = "Coin Counts as Checks"
    default = True

class RandomizeStageOrder(Toggle):
    """If off, stages will be played in the default order. In on, the order of the stages will be randomized."""
    display_name = "Randomize Stage Order"
    default = True

class MinigameSanity(Toggle):
    """Each minigame is its own check. Until all minigames have been beaten,
    the minigame roulette will prioritize minigames than have yet to be beaten"""
    display_name = "Minigame Sanity"
    default = True

class BoardMinigameSanity(Toggle):
    """Succeeding in on board minigames count as checks"""
    display_name = "Board Minigame Sanity"
    default = False

class ShopSanity(Toggle):
    """Every item that you can buy in every stage is a check"""
    display_name = "Shop Sanity"
    default = False

class SpaceSanity(Toggle):
    """Every 20 spaces past counts as a check"""
    display_name = "Space Sanity"
    default = False

class RandomizeBoardSpaces(Toggle):
    """Board spaces are randomized"""
    display_name = "Board Space Randomization"
    default = False

@dataclass
class MarioParty7Options(PerGameCommonOptions):
    dice_block_progression: DiceBlockProgression
    wallet_progression: WalletProgression
    capsule_capacity_progression: CapsuleCapacityProgression
    coin_counts_as_checks: CoinCountsAsChecks
    minigame_sanity: MinigameSanity
    shop_sanity: ShopSanity
    board_sanity: BoardMinigameSanity
    space_sanity: SpaceSanity
    board_minigame_sanity: BoardMinigameSanity
    randomize_stage_order: RandomizeStageOrder
    randomize_minigame_spaces: RandomizeBoardSpaces
    randomize_board_spaces: RandomizeBoardSpaces
    locked_minigame_actions: LockedMinigameActions
    locked_menu_navigation: LockedMenuNavigation
