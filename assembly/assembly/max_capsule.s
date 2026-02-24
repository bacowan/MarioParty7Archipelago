.include "constants.inc"
.include "macros.inc"

.equ r_MAX_CAPSULES, r3
.equ r_DIFFICULTY, r17

# 0b 0000 0000: 0 capsule max
# 0b 0000 0001: 1 capsule max
# 0b 0000 0010: 2 capsule max
# 0b 0000 0011: 3 capsule max

# r3 will also be the output
lis     r3, MAX_CAPSULE_SAVE@h
lbz     r_MAX_CAPSULES, MAX_CAPSULE_SAVE@l(r3)

# the player number will act as an offset from p1's info structure address. Structures are offset by 0x110 bytes.
# r18 will now store the full offset.
# r21 stores the current player number (from code called before this)
BRANCH_IF_PLAYER r21, r18, r_DIFFICULTY, end

# just set the max capsules to 3 for the cpu
li      r_MAX_CAPSULES, 3

# go back to the callsite
end:
lis r17, 0x8016
ori r17, r17, 0x75BC
mtctr r17
bctr
