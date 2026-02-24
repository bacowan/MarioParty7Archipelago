# RAM Locations
.equ CURRENT_MINIGAME_OFFSET,          0x80291559

# player data structure
.equ PLAYER_STRUCT_BASE_OFFSET, 0x80290C98
.equ PLAYER_STRUCT_SIZE,        0x110
.equ IS_CPU_MASK_BIT,           0x20

# custom save locations
.equ MAX_DICE_ROLL_SAVE,        0x8029D70A
.equ COMPLETED_MINIGAMES_SAVE,  0x81720003
.equ LOCK_JUMP_SAVE,            0x8172000D
.equ MAX_CAPSULE_SAVE,          0x81720005
.equ MAX_COINS,                 0x81720001
