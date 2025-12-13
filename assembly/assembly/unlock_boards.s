# This function starts at 0x804ed7a0 and goes until 0x804ed7fc.
# Loop through and copy each board's "unlocked" value.
# Base save location is at 0x80529ec2 with an offset of one byte.
# Loaded into 0x8052a604 with an offset of 2 bytes.

li      r3, 0               # r3 is the current stage index
lis     r4, 0x8052          # r4 is the location in the save values
ori     r4, r4, 0x9EC2
lis     r31, 0x8052         # r31 is the store location
ori     r31, r31, 0xA605

# Loop through each location
loop_start:
lbzx    r5, r4, r3          # r5 is whether or not the stage is unlocked
xori    r5, r5, 1           # unlocked/locked is inversed in the save file
stb     r5, 0(r31)

nop
nop

addi    r3, r3, 1
addi    r31, r31, 2         # the store location is 2 bytes each and the load location is 1 byte each
cmpwi   cr0, r3, 6          # check all 6 stages
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
nop

end:
