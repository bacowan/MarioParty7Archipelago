.include "constants.inc"
.include "macros.inc"

.equ r_MAX_COINS, r20

# r20 will hold the max coin count (2 bytes)
lis     r_MAX_COINS, MAX_COINS@h
ori     r_MAX_COINS, r20, 0x0000
lhz     r_MAX_COINS, MAX_COINS@l(r20)

# the player number will act as an offset from p1's info structure address. Structures are offset by 0x110 bytes.
# r18 will now store the full offset.
# r30 stores the current player number (from code called before this)
BRANCH_IF_PLAYER r30, r18, r17, common

# set cpu coin max to 999
li      r20, 999

common:
extsh   r0, r31
cmpw    r0, r20 # added code
ble-    end
mr      r31, r20 # added code


# go back to the callsite
end:
lis r20, 0x8003
ori r20, r20, 0xEEA4
mtctr r20
bctr
