# The dice display value is set to r0, so that's our output register.
# r17 doesn't seem to be in use, so we'll hijack that.
# We will use register r18 from the call-site too.

.include "constants.inc"
.equ PLAYER_NUMBER_LOC,     0x80291522
.equ RETURN_LINE,           0x8018CC94

# Overwritten code from the callsite that will handle the default case
rlwinm r0, r3, 1, 0, 30
addi r3, r1, 44
lhax r0, r3, r0

# load the current player number into r18
lis r17, PLAYER_NUMBER_LOC@h
lbz r18, PLAYER_NUMBER_LOC@l(r17)

# the player number will act as an offset from p1's info structure address. Structures are offset by 0x110 bytes.
# r18 will now store the full offset.
mulli r18, r18, PLAYER_STRUCT_SIZE

# load the cpu difficulty/is-player value into memory
lis r17, PLAYER_STRUCT_BASE_OFFSET@h
ori r17, r17, PLAYER_STRUCT_BASE_OFFSET@l
add r17, r17, r18 # add the offset to the base memory value
lbz r17, 0(r17)

# if it is a computer player, then skip to the end
andi. r17, r17, IS_CPU_MASK_BIT # this bit will be set for CPUs but not human players
bne end

# dice values are as follows:
# 0b 0000 0000 # can only roll 1
# 0b 0000 0001 # can roll 1 or 2
# 0b 0000 0010 # can roll 1-5
# 0b 0000 0011 # can roll normally

# load the max dice roll value
lis r17, MAX_DICE_ROLL_SAVE@h
ori r17, r17, MAX_DICE_ROLL_SAVE@l
lbz r17, 0(r17)

# can only roll 1
cmpwi r17, 0
bne roll2
li r0, 0
b end

# can only roll 1 or 2
roll2:
cmpwi r17, 1
bne roll5
li r19, 1
and r0, r0, r19 # only take the last bit so that we get 0 or 1 (which gets one added to it)
b end

# can only roll 1-5
roll5:
cmpwi r17, 2
bne end
li r19, 1
srw r0, r0, r19 # bit shift right to divide by 2

end:

# set the value in memory (this is copied from the callsite)
sth r0, 0x0054(r29)

# go back to the callsite
lis r18, RETURN_LINE@h
ori r18, r18, RETURN_LINE@l
mtctr r18
bctr
