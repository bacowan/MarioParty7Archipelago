# r19: completed minigame flags
# r16: number of 0s (uncompleted minigames) in the flags
# r26: output

# r23 will store the kind of minigame this is. If it is a 1v1 minigame r23 will be 6
cmpwi   r23, 6
bne     default

# r19 will hold what minigames have been completed. It's stored in memory at 0x81720003 and 0x81720004.
# They are bitflags where 1 is completed and 0 is not. Left aligned.
lis     r19, 0x8172
lhz     r19, 3(r19)

# if all minigames or no minigames have been beaten, just use the default behaviour.
# There are 12 minigames, so the flags will either be 0b1111 1111 1111 0000 or 0
cmpli   0, 1, r19, 0xFFF0
beq     default
cmpli   0, 1, r19, 0
beq     default

# count the 0s, then select a random one
li      r16, 0              # r16 holds the count of 0s
li      r20, 12             # we will check the leftmost 12 bits
mr      r15, r19            # copy the flags temporarily

loop_start:
andi.   r14, r15, 0x8000    # check the value of the leftmost bit to see if it's 1 or 0.

bne     loop_end            # if 1, don't count
addi    r16, r16, 1

loop_end:
slwi    r15, r15, 1         # shift the bits to check the next one
addic.  r20, r20, -1
bne     loop_start          # loop until r20 == 0

# get a "random" value by checking the time
mftb    r20

# take the modulus of that random number with the number of 0s we found. We will select that as the minigame
divwu   r15, r20, r16       # r15 = r20 / r16
mullw   r15, r15, r16       # r15 = r15 * r16
subf    r15, r15, r20       # r15 = r20 - r15

# select the nth 0 minigame
addi    r15, r15, 1
li      r20, 0              # r20 stores the index of the flags as we loop through, which will correspond to the selected game index

next_loop_start:
andi.   r14, r19, 0x8000    # check the most significant bit

bne     next_loop_end       # if 1, don't count
addi    r15, r15, -1

next_loop_end:
slwi    r19, r19, 1         # bit shift left to check the next bit
addi    r20, r20, 1         # increment the minigame index

cmpwi   r15, 0              # Once r16 hits 0 then we're done
bne     next_loop_start

# since the loop starts by incrementing r20, it will always be 1 too large
addi    r20, r20, -1

# The duel minigames aren't side by side in index. They are located at 45-46, 50-54, 57-61.
li      r15, 2
cmplw   r20, r15
blt     first_set           # select 45 or 46
li      r15, 6
cmplw   r20, r15
blt     second_set          # select 50-54

addi    r26, r20, 51        # r20 will be at least 6, so this will result in 57+
b       end

first_set:
addi    r26, r20, 45        # first minigame starts at 45
b       end

second_set:
addi    r26, r20, 48        # r20 will be between 2 and 5, so this will result in 50-54
b       end

default:
addi    r26, r26, 1

# go back to the callsite
end:
lis r19, 0x8022
ori r19, r19, 0x061C
mtctr r19
bctr
