.include "macros.inc"

.equ RETURN_ADDRESS, 0x800A2734
.equ MINIGAME_ENDED_VALUE, 0x804F2440
.equ CURRENT_MINIGAME_OFFSET, 0x80291559
.equ r_MINIGAME_ENDED_VALUE, r3
.equ r_MINIGAME_END_FLAG, r29
.equ r_CURRENT_MINIGAME_OFFSET, r3
.equ r_ZERO, r15

# when a minigame ends, set the current minigame to 0. The game seems to keep it at the original value for some reason,
# but if we do this then we can tell if we're in a minigame or not.
# This code appears to be called when a scene change happens. When a minigame ends, the value in r29
# appears to be 0x804F2440
SET_REGISTER r_MINIGAME_ENDED_VALUE, MINIGAME_ENDED_VALUE

cmpw        r_MINIGAME_ENDED_VALUE, r_MINIGAME_END_FLAG
bne         end

# the value at this memory address stores the id of the current minigame:
SET_REGISTER r_CURRENT_MINIGAME_OFFSET, CURRENT_MINIGAME_OFFSET
li          r_ZERO, 0
stb         r_ZERO, 0(r_CURRENT_MINIGAME_OFFSET)

end:

# restore the code from the callsite
addi        r3, r29, 0

# go back to the callsite
lis         r15, RETURN_ADDRESS@h
ori         r15, r15, RETURN_ADDRESS@l
mtctr       r15
bctr
