
.include "constants.inc"

# r19: completed minigame flags
# r16: number of 0s (uncompleted minigames) in the flags
# r26: output

.equ    r_MINIGAME_TYPE, r23
.equ    r_COMPLETED_MINIGAMES, r19
.equ    r_OUTPUT, r26

.equ    ENUM_1V1_MINIGAME, 6

# r23 will store the kind of minigame this is. If it is a 1v1 minigame r23 will be 6
cmpwi   r_MINIGAME_TYPE, ENUM_1V1_MINIGAME
bne     default

# r19 will hold what minigames have been completed. It's stored in memory at 0x81720003 and 0x81720004.
# They are bitflags where 1 is completed and 0 is not. Left aligned.
lis     r19, COMPLETED_MINIGAMES_SAVE@h
lhz     r_COMPLETED_MINIGAMES, COMPLETED_MINIGAMES_SAVE@l(r19)

# if all minigames or no minigames have been beaten, just use the default behaviour.
# There are 12 minigames, so the flags will either be 0b1111 1111 1111 0000 or 0
cmpli   0, 1, r_COMPLETED_MINIGAMES, 0xFFF0
beq     default
cmpli   0, 1, r_COMPLETED_MINIGAMES, 0
beq     default

# count the 0s, then select a random one
# TODO: r15 probably isn't needed; can just use r19 and shift that
.equ r_ZERO_COUNT, r16
.equ r_REMAINING_CHECKS, r20
.equ r_COMPLETED_MINIGAMES_SHIFTED, r15
li      r_ZERO_COUNT, 0                                                 # r16 holds the count of 0s
li      r_REMAINING_CHECKS, 12                                          # we will check the leftmost 12 bits
mr      r_COMPLETED_MINIGAMES_SHIFTED, r_COMPLETED_MINIGAMES            # copy the flags temporarily

loop_start:
andi.   r14, r_COMPLETED_MINIGAMES_SHIFTED, 0x8000    # check the value of the leftmost bit to see if it's 1 or 0.

bne     loop_end            # if 1, don't count
addi    r_ZERO_COUNT, r_ZERO_COUNT, 1

loop_end:
slwi    r_COMPLETED_MINIGAMES_SHIFTED, r_COMPLETED_MINIGAMES_SHIFTED, 1         # shift the bits to check the next one
addic.  r_REMAINING_CHECKS, r_REMAINING_CHECKS, -1
bne     loop_start          # loop until r20 == 0

# get a "random" value by checking the time
.equ r_RANDOM, r20
mftb    r_RANDOM

# take the modulus of that random number with the number of 0s we found. We will select that as the minigame
.equ    r_SELECTED_MINIGAME, r15
divwu   r15, r_RANDOM, r_ZERO_COUNT         # r15 = r_RANDOM / r_ZERO_COUNT
mullw   r15, r15, r16                       # r15 = r15 * r_ZERO_COUNT
subf    r_SELECTED_MINIGAME, r15, r_RANDOM  # r15 = r_RANDOM - r15

# select the nth 0 minigame
.equ    r_CHECKING_MINIGAME, r20
addi    r_SELECTED_MINIGAME, r_SELECTED_MINIGAME, 1
li      r_CHECKING_MINIGAME, 0          # r20 stores the index of the flags as we loop through,
                                        # which will correspond to the selected game index

next_loop_start:
andi.   r14, r_COMPLETED_MINIGAMES, 0x8000    # check the most significant bit

bne     next_loop_end       # if 1, don't count
addi    r_SELECTED_MINIGAME, r_SELECTED_MINIGAME, -1

next_loop_end:
slwi    r_COMPLETED_MINIGAMES, r_COMPLETED_MINIGAMES, 1         # bit shift left to check the next bit
addi    r_CHECKING_MINIGAME, r_CHECKING_MINIGAME, 1         # increment the minigame index

cmpwi   r_SELECTED_MINIGAME, 0              # Once r15 hits 0 then we're done
bne     next_loop_start

# since the loop starts by incrementing r20, it will always be 1 too large
addi    r_CHECKING_MINIGAME, r_CHECKING_MINIGAME, -1

# The duel minigames aren't side by side in index. They are located at 45-46, 50-54, 57-61.
.equ    r_MINIGAME_SET_THRESHOLD, r15
li      r_MINIGAME_SET_THRESHOLD, 2
cmplw   r_CHECKING_MINIGAME, r_MINIGAME_SET_THRESHOLD
blt     first_set           # select 45 or 46
li      r_MINIGAME_SET_THRESHOLD, 6
cmplw   r_CHECKING_MINIGAME, r_MINIGAME_SET_THRESHOLD
blt     second_set          # select 50-54

addi    r26, r_CHECKING_MINIGAME, 51        # r20 will be at least 6, so this will result in 57+
b       end

first_set:
addi    r_OUTPUT, r_CHECKING_MINIGAME, 45        # first minigame starts at 45
b       end

second_set:
addi    r_OUTPUT, r_CHECKING_MINIGAME, 48        # r20 will be between 2 and 5, so this will result in 50-54
b       end

default:
addi    r_OUTPUT, r_OUTPUT, 1

# go back to the callsite
end:
lis r19, 0x8022
ori r19, r19, 0x061C
mtctr r19
bctr
