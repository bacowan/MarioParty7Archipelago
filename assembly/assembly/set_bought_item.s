.include "constants.inc"

.equ r_PLAYER_NUMBER,   r6
.equ r_CAPSULE_ID,      r5

.equ r_BOUGHT_ITEMS,    r2
.equ r_SHOP_MASK,       r4
.equ r_CURRENT_SPACE,   r7

# save registers
stwu    r1, -16(r1)

stw     r2, 4(r1)
stw     r4, 8(r1)
stw     r7, 12(r1)

# check if it was an archipelago item (1A, 1B, 1C), and set the initial shop bit mask accordingly
cmpwi   r_CAPSULE_ID, 0x1A
bne     second_capsule_check
li      r_SHOP_MASK, 0x1
b       check_shop

second_capsule_check:
cmpwi   r_CAPSULE_ID, 0x1B
bne     third_capsule_check
li      r_SHOP_MASK, 0x2
b       check_shop

third_capsule_check:
cmpwi   r_CAPSULE_ID, 0x1C
bne     default
li      r_SHOP_MASK, 0x4

check_shop:

# get the memory location for capsules
mulli   r2, r_PLAYER_NUMBER, PLAYER_STRUCT_SIZE     # offset from the start of player structures to this player structure
lis     r7, PLAYER_STRUCT_BASE_OFFSET@ha            # start of player structures
ori     r7, r7, PLAYER_STRUCT_BASE_OFFSET@l
add     r2, r2, r7                                  # start of this player's structure
lbz     r_CURRENT_SPACE, CURRENT_SPACE_OFFSET(r2)   # load the value of the current space

# grand canal left
cmpwi   r_CURRENT_SPACE, GRAND_CANAL_LEFT_ID
beq     shop_selection_end
slwi    r_SHOP_MASK, r_SHOP_MASK, 3          # move the 3 bits to the next shop

# grand canal right
cmpwi   r_CURRENT_SPACE, GRAND_CANAL_RIGHT_ID
beq     shop_selection_end
slwi    r_SHOP_MASK, r_SHOP_MASK, 3          # move the 3 bits to the next shop

# pagoda peak bottom
cmpwi   r_CURRENT_SPACE, PAGODA_PEAK_BOTTOM_ID
beq     shop_selection_end
slwi    r_SHOP_MASK, r_SHOP_MASK, 3          # move the 3 bits to the next shop

# pagoda peak top
cmpwi   r_CURRENT_SPACE, PAGODA_PEAK_TOP_ID
beq     shop_selection_end
slwi    r_SHOP_MASK, r_SHOP_MASK, 3          # move the 3 bits to the next shop

# neon heights left
cmpwi   r_CURRENT_SPACE, NEON_HEIGHTS_LEFT_ID
beq     shop_selection_end
slwi    r_SHOP_MASK, r_SHOP_MASK, 3          # move the 3 bits to the next shop

# neon heights right
cmpwi   r_CURRENT_SPACE, NEON_HEIGHTS_RIGHT_ID
beq     shop_selection_end
slwi    r_SHOP_MASK, r_SHOP_MASK, 3          # move the 3 bits to the next shop

# windmillville left
cmpwi   r_CURRENT_SPACE, WINDMILLVILLE_LEFT_ID
beq     shop_selection_end
slwi    r_SHOP_MASK, r_SHOP_MASK, 3          # move the 3 bits to the next shop

# windmillville right
cmpwi   r_CURRENT_SPACE, WINDMILLVILLE_RIGHT_ID
beq     shop_selection_end
slwi    r_SHOP_MASK, r_SHOP_MASK, 3          # move the 3 bits to the next shop

# pyramid park top
cmpwi   r_CURRENT_SPACE, PYRAMID_PARK_TOP_ID
beq     shop_selection_end
slwi    r_SHOP_MASK, r_SHOP_MASK, 3          # move the 3 bits to the next shop

# pyramid park bottom
cmpwi   r_CURRENT_SPACE, PYRAMID_PARK_BOTTOM_ID
beq     shop_selection_end
slwi    r_SHOP_MASK, r_SHOP_MASK, 3          # move the 3 bits to the next shop

# bowser bottom
cmpwi   r_CURRENT_SPACE, BOWSER_BOTTOM_ID
beq     shop_selection_end
slwi    r_SHOP_MASK, r_SHOP_MASK, 3          # move the 3 bits to the next shop

# bowser top
cmpwi   r_CURRENT_SPACE, BOWSER_TOP_ID
beq     shop_selection_end
b       end

shop_selection_end:

# load the flags for bought items
lis     r4, BOUGHT_ITEMS_SAVE@h
lwz     r_BOUGHT_ITEMS, BOUGHT_ITEMS_SAVE@l(r4)

# set the new flag
and.    r_BOUGHT_ITEMS, r_SHOP_MASK, r_BOUGHT_ITEMS

# save the updated flags
stw     r_BOUGHT_ITEMS, BOUGHT_ITEMS_SAVE@l(r4)
b       end

# restored code from callsite
default:
stb	r5, 0x0006 (r3)

end:

# set the return address
lis r4, 0x8016
ori r4, r4, 0x76aC
mtctr r4

# restore stack and return
lwz     r2, 4(r1)
lwz     r4, 8(r1)
lwz     r7, 12(r1)
addi    r1,  r1, 16

bctr
