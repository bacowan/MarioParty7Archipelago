# when a minigame ends, set the current minigame to 0. The game seems to keep it at the original value for some reason,
# but if we do this then we can tell if we're in a minigame or not.
# This code appears to be called when a scene change happens. When a minigame ends, the value in r29
# appears to be 0x804F2440
lis         r3, 0x804F
ori         r3, r3, 0x2440

cmpw        r3, r29
bne         end

# the value at this memory address stores the id of the current minigame:
lis         r3, 0x8029
ori         r3, r3, 0x1559
li          r15, 0
stb         r15, 0(r3)

end:

# restore the code from the callsite
addi        r3, r29, 0

# go back to the callsite
lis         r15, 0x800A
ori         r15, r15, 0x2734
mtctr       r15
bctr
