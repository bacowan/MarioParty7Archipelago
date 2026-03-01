.include "constants.inc"
.include "macros.inc"

.equ r_SPACE_ID,    r3
.equ r_BOARD_OFFSET, r6
.equ r_CURRENT_BOARD, r4

# save registers
stwu    r1, -32(r1)

stw     r4, 4(r1)
stw     r5, 8(r1)
stw     r6, 12(r1)
stw     r7, 16(r1)

# figure out who the current player is
.equ r_CURRENT_PLAYER_DIFFICULTY, r4
GET_CURRENT_PLAYER_DIFFICULTY r_CURRENT_PLAYER_DIFFICULTY, r5

# if it is a computer player, then skip to the end
andi. r4, r_CURRENT_PLAYER_DIFFICULTY, IS_CPU_MASK_BIT # this bit will be set for CPUs but not human players
bne end

# Figure out what board we're on and set the base offset accordingly
lis     r4, CURRENT_BOARD_OFFSET@ha
lbz     r_CURRENT_BOARD, CURRENT_BOARD_OFFSET@l(r4)

# Grand Canal
cmpwi   r_CURRENT_BOARD, 0
bne     check_pagoda_peak
lis     r6, GRAND_CANAL_REACHED_SPACES_SAVE@h
ori     r_BOARD_OFFSET, r6, GRAND_CANAL_REACHED_SPACES_SAVE@l
b       get_board_done

# Pagoda Peak
check_pagoda_peak:
cmpwi   r_CURRENT_BOARD, 1
bne     check_pyramid_park
lis     r6, PAGODA_PEAK_REACHED_SPACES_SAVE@h
ori     r_BOARD_OFFSET, r6, PAGODA_PEAK_REACHED_SPACES_SAVE@l
b       get_board_done

# Pyramid Park
check_pyramid_park:
cmpwi   r_CURRENT_BOARD, 2
bne     check_windmillville
lis     r6, PYRAMID_PARK_REACHED_SPACES_SAVE@h
ori     r_BOARD_OFFSET, r6, PYRAMID_PARK_REACHED_SPACES_SAVE@l
b       get_board_done

# Windmillville
check_windmillville:
cmpwi   r_CURRENT_BOARD, 3
bne     check_neon_heights
lis     r6, WINDMILLVILLE_REACHED_SPACES_SAVE@h
ori     r_BOARD_OFFSET, r6, WINDMILLVILLE_REACHED_SPACES_SAVE@l
b       get_board_done

# Neon Heights
check_neon_heights:
cmpwi   r_CURRENT_BOARD, 4
bne     check_bowser
lis     r6, NEON_HEIGHTS_REACHED_SPACES_SAVE@h
ori     r_BOARD_OFFSET, r6, NEON_HEIGHTS_REACHED_SPACES_SAVE@l
b       get_board_done

# Bower
check_bowser:
lis     r6, BOWSER_REACHED_SPACES_SAVE@h
ori     r_BOARD_OFFSET, r6, BOWSER_REACHED_SPACES_SAVE@l

get_board_done:


# We save the nth bit (where n is the space id stored in r3) as a bit flag to the save location in memory.
# First, figure out which bit this is
.equ r_WORD_OFFSET, r4
.equ r_BIT_INDEX, r5

srwi    r4, r_SPACE_ID, 5               # wordIndex = spaceId / 32
andi.   r_BIT_INDEX, r_SPACE_ID, 0x1f   # bitIndex = spaceId % 32
slwi    r_WORD_OFFSET, r4, 2            # wordOffset = wordIndex * 4 (byte offset)

# load the word to be changed
.equ    r_FLAGS, r5
lwzx    r_FLAGS, r_WORD_OFFSET, r_BOARD_OFFSET

# set the new flag
.equ r_NEW_FLAG, r7
li      r7, 1
slw     r_NEW_FLAG, r7, r_BIT_INDEX     # shift the bit over to its correct position within the word
or      r_FLAGS, r_NEW_FLAG, r_FLAGS    # set the new word to be saved

stwx    r_FLAGS, r_WORD_OFFSET, r_BOARD_OFFSET # save it

end:

# set return line
lis r4, 0x8015
ori r4, r4, 0xd568
mtctr r4

# restore registers
lwz     r4, 4(r1)
lwz     r5, 8(r1)
lwz     r6, 12(r1)
lwz     r7, 16(r1)
addi    r1,  r1, 32

# restore previous code
sth	r3, 0 (r29)

# jump back
bctr
