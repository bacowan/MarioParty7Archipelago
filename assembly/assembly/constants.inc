# RAM Locations
.equ CURRENT_MINIGAME_OFFSET,          0x80291559
.equ CURRENT_BOARD_OFFSET,             0x8029D67B

# player data structure
.equ PLAYER_STRUCT_BASE_OFFSET, 0x80290C98
.equ PLAYER_STRUCT_SIZE,        0x110
.equ CURRENT_SPACE_OFFSET,      0x15

.equ IS_CPU_MASK_BIT,           0x20

# shop IDs
.equ GRAND_CANAL_LEFT_ID,       0x65
.equ GRAND_CANAL_RIGHT_ID,      0x67
.equ PAGODA_PEAK_BOTTOM_ID,     0x10
.equ PAGODA_PEAK_TOP_ID,        0x46
.equ NEON_HEIGHTS_LEFT_ID,      0x0F
.equ NEON_HEIGHTS_RIGHT_ID,     0x77
.equ WINDMILLVILLE_LEFT_ID,     0x5C
.equ WINDMILLVILLE_RIGHT_ID,    0x18
.equ BOWSER_BOTTOM_ID,          0x3B
.equ BOWSER_TOP_ID,             0x85

# custom save locations
.equ MAX_DICE_ROLL_SAVE,                    0x8029D70A
.equ COMPLETED_MINIGAMES_SAVE,              0x8029D70B
.equ LOCK_JUMP_SAVE,                        0x8029D70D
.equ MAX_CAPSULE_SAVE,                      0x8029D70E
.equ MAX_COINS,                             0x8029D70F
.equ MINIGAME_MAX_SPEED_SAVE,               0x8029D710
.equ BOUGHT_ITEMS_SAVE,                     0x8029D711
.equ UNLOCKED_STAGES_SAVE,                  0x8029D715
.equ GRAND_CANAL_REACHED_SPACES_SAVE,       0x8029D71B # 15 bytes
.equ PAGODA_PEAK_REACHED_SPACES_SAVE,       0x8029D72A # 11 bytes
.equ PYRAMID_PARK_REACHED_SPACES_SAVE,      0x8029D735 # 16 bytes
.equ WINDMILLVILLE_REACHED_SPACES_SAVE,     0x8029D745 # 16 bytes
.equ NEON_HEIGHTS_REACHED_SPACES_SAVE,      0x8029D755 # 18 bytes
.equ BOWSER_REACHED_SPACES_SAVE,            0x8029D767 # 16 bytes
