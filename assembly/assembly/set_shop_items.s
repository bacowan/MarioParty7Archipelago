.include "constants.inc"

.equ FAKE_ITEM_OFFSET, 0x80274898
.equ LOOP_BASE_OFFSET, PLAYER_STRUCT_BASE_OFFSET - 0x110

.equ FAKE_ITEM_1_ID,        0x1A
.equ FAKE_ITEM_2_ID,        0x1B
.equ FAKE_ITEM_3_ID,        0x1C

.equ EMPTY_ORB_MODEL_INDEX, 0x000F001D
.equ EMPTY_ORB_TEXT_INDEX,  0x0025

.equ STORE_1_SLOT_MODEL_ID_OFFSET, 0x03
.equ STORE_1_SLOT_COST_OFFSET,    0x04
.equ STORE_2_SLOT_MODEL_ID_OFFSET, 0x1F
.equ STORE_2_SLOT_COST_OFFSET,    0x20
.equ STORE_3_SLOT_MODEL_ID_OFFSET, 0x3B
.equ STORE_3_SLOT_COST_OFFSET,    0x3C

.equ ITEM_STRUCT_MODEL_OFFSET,  0x00
.equ ITEM_STRUCT_TEXT_OFFSET,   0x08
.equ ITEM_STRUCT_SIZE,          0x28

.equ r_SHOP_STRUCT_OFFSET,  r26
.equ r_PLAYER_NUMBER,       r17
.equ r_PLAYER_STRUCT_OFFSET, r18
.equ r_SHOP_MASK,           r19
.equ r_CURRENT_SPACE,       r18
.equ r_BOUGHT_ITEMS,        r18
.equ r_FAKE_ITEM_OFFSET,    r21
.equ r_ITEM_INDEX,          r22

# save registers
stwu    r1, -32(r1)

stw     r17,  8(r1)
stw     r18, 12(r1)
stw     r19, 16(r1)
stw     r20, 20(r1)
stw     r21, 24(r1)
stw     r22, 28(r1)

# r26 will store the location of the shop structure (set outside of this routine)

# Note that we don't bother checking whose turn it is, since CPUs don't actually view this.
# However, we do have to figure out which player the human is. r18 will temporarily represent
# the location of the player structure in memory.
lis     r18, LOOP_BASE_OFFSET@h
# player structure is at 0x80290C98; we add 0x110 at the start of every loop, so start at that value - 0x110
ori     r_PLAYER_STRUCT_OFFSET, r18, LOOP_BASE_OFFSET@l
li      r_PLAYER_NUMBER, 0                  # count how many players we have counted

player_check:
cmpwi   r_PLAYER_NUMBER, 4                  # break out if we've checked all players
beq     end

addi    r_PLAYER_STRUCT_OFFSET, r_PLAYER_STRUCT_OFFSET, PLAYER_STRUCT_SIZE        # prepare to check the next structure
addi    r_PLAYER_NUMBER, r_PLAYER_NUMBER, 1

lbz     r19, 0(r_PLAYER_STRUCT_OFFSET)             # load the value from memory

andi.   r19, r19, IS_CPU_MASK_BIT          # this bit will be set for CPUs but not human players
bne     player_check

# Check what the current shop is. The current space is stored in the player structure + 0x15
lbz     r_CURRENT_SPACE, CURRENT_SPACE_OFFSET(r_PLAYER_STRUCT_OFFSET)

# load the appropriate items into the shop. Leave vanilla items alone (represented by 1), and update
# archipelago items. This is a bit mask of 4 bytes (30 bits; the most significant 2 are ignored).
# 1 means that the item should be left alone.

# r19: mask of 1 bit that will correspond to the rightmost item of any given shop.
#   It will be shifted twice to the right to check the left and middle items.

li      r_SHOP_MASK, 0x1            # This is a mask that will check which shop items are available

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

# which shop items have been checked are stored at 0x81720009 - 0x8172000C
shop_selection_end:

# r18: bit flags for each collected shop item from all shops
lis     r18, BOUGHT_ITEMS_SAVE@h
lwz     r_BOUGHT_ITEMS, BOUGHT_ITEMS_SAVE@l(r18)

# r20: temp register for values to save.
# r21: offset for the capsule info array for item 1A. We will use the unused item ids of 1A, 1B, and 1C
# r22: index of current orb relative to all archipelago orbs
lis     r21, FAKE_ITEM_OFFSET@h
ori     r_FAKE_ITEM_OFFSET, r21, FAKE_ITEM_OFFSET@l
cntlzw  r22, r_SHOP_MASK                    # count leading zeros in r19
li      r20, 31
subf    r_ITEM_INDEX, r22, r20              # convert to trailing zeros


# leftmost shop item
and.    r20, r_SHOP_MASK, r_BOUGHT_ITEMS
bne     middle_shop_item

# store the new item id
li      r20, FAKE_ITEM_1_ID
stb     r20, STORE_1_SLOT_MODEL_ID_OFFSET(r_SHOP_STRUCT_OFFSET)

# set the cost for the orb
li      r20, 5                      # left item has a cost of 5
stw     r20, STORE_1_SLOT_COST_OFFSET(r_SHOP_STRUCT_OFFSET)

# set the model for an empty orb
lis     r20, EMPTY_ORB_MODEL_INDEX@h
ori     r20, r20, EMPTY_ORB_MODEL_INDEX@l
stw     r20, ITEM_STRUCT_MODEL_OFFSET(r_FAKE_ITEM_OFFSET)

# set the text for the orb
lis     r20, EMPTY_ORB_TEXT_INDEX
or      r20, r20, r_ITEM_INDEX               # r22 has the index of the current orb as an archipelago item
stw     r20, ITEM_STRUCT_TEXT_OFFSET(r_FAKE_ITEM_OFFSET)                 # the text of the item is at an offset of 8 bytes from the start



middle_shop_item:
slwi    r_SHOP_MASK, r_SHOP_MASK, 1         # increment the shop item ordinal
addi    r_ITEM_INDEX, r_ITEM_INDEX, 1         # as well as the index
and.    r20, r_SHOP_MASK, r_BOUGHT_ITEMS
bne     right_shop_item

# store the new item id
li      r20, FAKE_ITEM_2_ID
stb     r20, STORE_2_SLOT_MODEL_ID_OFFSET(r_SHOP_STRUCT_OFFSET)

# set the cost for the orb
li      r20, 10                      # middle item has a cost of 10
stw     r20, STORE_2_SLOT_COST_OFFSET(r_SHOP_STRUCT_OFFSET)

# set the model for an empty orb
.set    MODEL_OFFSET, ITEM_STRUCT_SIZE + ITEM_STRUCT_MODEL_OFFSET
lis     r20, EMPTY_ORB_MODEL_INDEX@h
ori     r20, r20, EMPTY_ORB_MODEL_INDEX@l
stw     r20, MODEL_OFFSET(r_FAKE_ITEM_OFFSET)

# set the text for the orb
.set    TEXT_OFFSET, ITEM_STRUCT_SIZE + ITEM_STRUCT_TEXT_OFFSET
lis     r20, EMPTY_ORB_TEXT_INDEX
or      r20, r20, r_ITEM_INDEX               # r22 has the index of the current orb as an archipelago item
stw     r20, TEXT_OFFSET(r_FAKE_ITEM_OFFSET)              # the text of the item is at an offset of 8 bytes from the start



right_shop_item:
slwi    r_SHOP_MASK, r_SHOP_MASK, 1                 # increment the shop item ordinal
addi    r_ITEM_INDEX, r_ITEM_INDEX, 1                 # as well as the index
and.    r20, r_SHOP_MASK, r_BOUGHT_ITEMS
bne     shop_item_end

# store the new item id
li      r20, FAKE_ITEM_3_ID
stb     r20, STORE_3_SLOT_MODEL_ID_OFFSET(r_SHOP_STRUCT_OFFSET)

# set the cost for the orb
li      r20, 20                     # right item has a cost of 20
stw     r20, STORE_3_SLOT_COST_OFFSET(r_SHOP_STRUCT_OFFSET)

# set the model for an empty orb
.set    MODEL_OFFSET, ITEM_STRUCT_SIZE * 2 + ITEM_STRUCT_MODEL_OFFSET
lis     r20, EMPTY_ORB_MODEL_INDEX@h
ori     r20, r20, EMPTY_ORB_MODEL_INDEX@l
stw     r20, MODEL_OFFSET(r_FAKE_ITEM_OFFSET)

# set the text for the orb
.set    TEXT_OFFSET, ITEM_STRUCT_SIZE * 2 + ITEM_STRUCT_TEXT_OFFSET
lis     r20, EMPTY_ORB_TEXT_INDEX
or      r20, r20, r_ITEM_INDEX               # r22 has the index of the current orb as an archipelago item
stw     r20, TEXT_OFFSET(r_FAKE_ITEM_OFFSET)              # the text of the item is at an offset of 8 bytes from the start

shop_item_end:
end:

# restore registers
lwz     r17,  8(r1)
lwz     r18, 12(r1)
lwz     r19, 16(r1)
lwz     r20, 20(r1)
lwz     r21, 24(r1)
lwz     r22, 28(r1)

addi    r1, r1, 32

# restore previous code
lwzx    r3, r26, r0

# jump back
lis r19, 0x8021
ori r19, r19, 0x7198
mtctr r19
bctr
