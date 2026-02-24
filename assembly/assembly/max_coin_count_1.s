.include "constants.inc"
.include "macros.inc"

.equ r_MAX_COINS, r20

# r20 will hold the max coin count (2 bytes). It's stored in memory at 0x81720001 - 0x81720002
lis     r_MAX_COINS, MAX_COINS@h
ori     r_MAX_COINS, r20, 0x0000
lhz     r_MAX_COINS, MAX_COINS@l(r20)

# the player number will act as an offset from p1's info structure address. Structures are offset by 0x110 bytes.
# r18 will now store the full offset.
# r30 stores the current player number (from code called before this)
BRANCH_IF_PLAYER r30, r18, r17, common

# set cpu coin max to 999
li      r_MAX_COINS, 999

common:
cmpwi   r30, 0
ble-    end # new code
lha     r0, 0x002A(r3)
cmpw    r0, r20 # new code
bge-    end
add     r0, r0, r30
extsh   r0, r0
sth     r0, 0x002A(r3)
lha     r0, 0x002A(r3)
cmpw    r0, r20 # new code
ble-    end
mr      r0, r29 # new code
sth     r0, 0x002A(r3)

end:
addi    r29, r3, 14

# go back to the callsite
lis r20, 0x8016
ori r20, r20, 0x6D08
mtctr r20
bctr
