# r31 seems to have a pointer to some player data. The offset depends on which player
# load the expected value into r15 and compare with that

# Check which player the human player is. Branch to the corresponding section depending on if the human player is p1 or p2
lis     r15, 0x8029
lbz     r15, 0x0C98(r15)    # load the value from memory
andi.   r15, r15, 0x20      # this bit will be set for CPUs but not human players
bne     player2

# p1 for gimme a sign.
lis     r15, 0x80b4         # Load upper 16 bits
ori     r15, r15, 0x6be0    # OR in lower 16 bits
cmpw    r31, r15            # Compare r3 with r0
beq     fix_speed

# p1 for gimme a sign.
lis     r15, 0x809c         # Load upper 16 bits
ori     r15, r15, 0xdd60    # OR in lower 16 bits
cmpw    r31, r15            # Compare r3 with r0
beq     fix_speed

# p1 for bridge work.
lis     r15, 0x80b2         # Load upper 16 bits
ori     r15, r15, 0x5420    # OR in lower 16 bits
cmpw    r31, r15            # Compare r3 with r0
beq     fix_speed

# p1 for apes of wrath.
lis     r15, 0x808b         # Load upper 16 bits
ori     r15, r15, 0x0f40    # OR in lower 16 bits
cmpw    r31, r15            # Compare r3 with r0
beq     fix_speed

# p1 for spin doctor.
lis     r15, 0x8092         # Load upper 16 bits
ori     r15, r15, 0x4bc0    # OR in lower 16 bits
cmpw    r31, r15            # Compare r3 with r0
beq     fix_speed

# p1 for royal rumpus.
lis     r15, 0x808c         # Load upper 16 bits
ori     r15, r15, 0xb8c0    # OR in lower 16 bits
cmpw    r31, r15            # Compare r3 with r0
beq     fix_speed

# p1 for weight for it.
lis     r15, 0x8091         # Load upper 16 bits
ori     r15, r15, 0xe780    # OR in lower 16 bits
cmpw    r31, r15            # Compare r3 with r0
beq     fix_speed

# p1 for warp pipe dreams.
lis     r15, 0x809b         # Load upper 16 bits
ori     r15, r15, 0x82e0    # OR in lower 16 bits
cmpw    r31, r15            # Compare r3 with r0
beq     fix_speed

# default logic
lfs     f1, 0x4(r29)
b       end


# player 2 checks
player2:

# p2 for gimme a sign.
lis     r15, 0x80b4         # Load upper 16 bits
ori     r15, r15, 0x6de0    # OR in lower 16 bits
cmpw    r31, r15            # Compare r3 with r0
beq     fix_speed

# p2 for gimme a sign.
lis     r15, 0x809c         # Load upper 16 bits
ori     r15, r15, 0xdf60    # OR in lower 16 bits
cmpw    r31, r15            # Compare r3 with r0
beq     fix_speed

# p2 for bridge work.
lis     r15, 0x80b2         # Load upper 16 bits
ori     r15, r15, 0x5620    # OR in lower 16 bits
cmpw    r31, r15            # Compare r3 with r0
beq     fix_speed

# p2 for apes of wrath.
lis     r15, 0x808b         # Load upper 16 bits
ori     r15, r15, 0x1140    # OR in lower 16 bits
cmpw    r31, r15            # Compare r3 with r0
beq     fix_speed

# p2 for spin doctor.
lis     r15, 0x8092         # Load upper 16 bits
ori     r15, r15, 0x4dc0    # OR in lower 16 bits
cmpw    r31, r15            # Compare r3 with r0
beq     fix_speed

# p2 for royal rumpus.
lis     r15, 0x808c         # Load upper 16 bits
ori     r15, r15, 0xbac0    # OR in lower 16 bits
cmpw    r31, r15            # Compare r3 with r0
beq     fix_speed

# p2 for weight for it.
lis     r15, 0x8091         # Load upper 16 bits
ori     r15, r15, 0xe980    # OR in lower 16 bits
cmpw    r31, r15            # Compare r3 with r0
beq     fix_speed

# p2 for warp pipe dreams.
lis     r15, 0x809b         # Load upper 16 bits
ori     r15, r15, 0x84e0    # OR in lower 16 bits
cmpw    r31, r15            # Compare r3 with r0
beq     fix_speed

# default logic
lfs     f1, 0x4(r29)
b       end

# speed is stored here, and the max speed is added to the minimum speed, so that a value of 0 is the minimum speed
fix_speed:
lis     r16, 0x8172
ori     r16, r16, 0x0008
lfs     f1, 0x0(r16)        # get the base value


addi    r1, r1, -8          # allocate 8 bytes on the stack
lis     r16, 0x3f00         # this (float 0.5) is the base value
stw     r16, 0(r1)          # store the value on the stack
lfs     f21, 0(r1)          # load the value in the stack
fadd    f1, f1, f21         # add it to f1. To go full speed this should be 0x3f00 0000 (float 0.5)
addi    r1, r1, 8           # restore the stack



end:
# go back to the callsite
lis r16, 0x8008
ori r16, r16, 0x068C
mtctr r16
bctr
