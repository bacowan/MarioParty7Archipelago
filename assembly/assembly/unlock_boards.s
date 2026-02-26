.include "constants.inc"

.equ BOARD_FLAG_LOC,        0x8052A605

.equ r_CURRENT_STAGE_INDEX, r3
.equ r_BOARD_FLAG_LOC,      r31
.equ r_UNLOCKED_STAGES,     r4
.equ r_IS_UNLOCKED,         r5

# This function starts at 0x804ed7a0 and goes until 0x804ed7fc.
# Loop through and copy each board's "unlocked" value.
# Base save location is at 0x8172000E with an offset of one byte.
# Loaded into 0x8052a604 with an offset of 2 bytes.
# The overwritten code sets a flag for each board to indicate whether or
# not it can be selected. That flag is only set if the stage before it
# is also unlocked.
# This code overwrites that behaviour and sets the flag based on what
# archipelago saves instead.

li      r_CURRENT_STAGE_INDEX, 0               # r3 is the current stage index
lis     r4, UNLOCKED_STAGES_SAVE@h          # r4 is the location in the save values
ori     r_UNLOCKED_STAGES, r4, UNLOCKED_STAGES_SAVE@l
lis     r31, BOARD_FLAG_LOC@h         # r31 is the store location
ori     r_BOARD_FLAG_LOC, r31, BOARD_FLAG_LOC@l

# Loop through each location
loop_start:
lbzx    r5, r_UNLOCKED_STAGES, r_CURRENT_STAGE_INDEX          # r5 is whether or not the stage is unlocked
rlwinm  r5, r5, 31, 1, 31   # Bitshift right 1. Treat 0b1x as unlocked. 1 is what the game will set it as, so we will ignore this value
xori    r_IS_UNLOCKED, r5, 1           # unlocked/locked is inversed in the save file

# for some reason these two lines get messed up, so replace them with nops
nop
nop

stb     r_IS_UNLOCKED, 0(r_BOARD_FLAG_LOC)
addi    r_CURRENT_STAGE_INDEX, r_CURRENT_STAGE_INDEX, 1
addi    r_BOARD_FLAG_LOC, r_BOARD_FLAG_LOC, 2         # the store location is 2 bytes each and the load location is 1 byte each
cmpwi   cr0, r_CURRENT_STAGE_INDEX, 6          # check all 6 stages
blt     loop_start
b       end

# The overwritten code is 24 lines long, so replace the rest with no-ops
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

end:
