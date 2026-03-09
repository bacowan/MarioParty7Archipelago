.include "constants.inc"

.equ WINNER_LOC,        0x802B7F3A
.equ MINIGAME_INDEX_LOC, 0x80291559

.equ r_WINNER_INDEX,    r18
.equ r_MINIGAME_INDEX,  r18
.equ r_MINIGAME_GAP_START, r19

# Find out who won
lis     r19, WINNER_LOC@h         # 0x802b7F3A is the location of the winning player index
lbz     r_WINNER_INDEX, WINNER_LOC@l (r19)

# the player number will act as an offset from p1's info structure address. Structures are offset by 0x110 bytes.
# r19 will now store the full offset.
mulli r18, r18, PLAYER_STRUCT_SIZE

# load the cpu difficulty/is-player value into memory
lis     r19, PLAYER_STRUCT_BASE_OFFSET@h         # 0x80290C98 is where the first difficulty/is-player value is stored
add     r19, r19, r_WINNER_INDEX       # add the offset to the base memory value
lbz     r19, PLAYER_STRUCT_BASE_OFFSET@l(r19)

# if it is a computer player, then skip to the end
andi.   r19, r19, IS_CPU_MASK_BIT        # this bit will be set for CPUs but not human players
beq     end

# get the minigame id
lis     r19, MINIGAME_INDEX_LOC@h         # 0x80291559 is the location of the minigame index
lbz     r_MINIGAME_INDEX, MINIGAME_INDEX_LOC@l (r19)

# 0 index the minigames.
# The minigame ids are 45-46, 50-54, 57-61, so we need to exclude the gaps
li      r15, 47
cmplw   r18, r15
blt     first_set          # 45-46
li      r15, 55
cmplw   r18, r15
blt     second_set         # 50-54

addi    r18, r18, -50
b       set_end

first_set:
addi    r18, r18, -45
b       set_end

second_set:
addi    r18, r18, -48

set_end:

# The completed minigames are stored at 0x81720003 and 0x81720004
lis     r16, COMPLETED_MINIGAMES_SAVE@ha
lhz     r19, COMPLETED_MINIGAMES_SAVE@l(r16)

# make a bitmask for the current minigame
li      r17, 1
slw     r17, r17, r18

# apply the bitmask
or      r19, r19, r17

# save it back
sth     r19, COMPLETED_MINIGAMES_SAVE@l(r16)

end:

# Overwritten code
mr  r3, 28

# go back to the callsite
lis r19, 0x8003
ori r19, r19, 0xC6CC
mtctr r19
bctr
