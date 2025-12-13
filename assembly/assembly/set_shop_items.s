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
lis     r18, 0x8029
ori     r18, r18, 0x0B88        # player structure is at 0x80291522; we add 0x110 at the start of every loop, so start at that value - 0x110
li      r17, 0                  # count how many players we have counted

player_check:
cmpwi   r17, 4                  # break out if we've checked all players
beq     end

addi    r18, r18, 0x110         # prepare to check the next structure
addi    r17, r17, 1

lbz     r19, 0(r18)             # load the value from memory

andi.   r19, r19, 0x20          # this bit will be set for CPUs but not human players
bne     player_check

# Check what the current shop is. The current space is stored in the player structure + 0x15
lbz     r18, 0x15(r18)

# load the appropriate items into the shop. Leave vanilla items alone (represented by 0), and update
# archipelago items. This is a bit mask of 4 bytes (30 bits; the most significant 2 are ignored).
# 0 means that the item should be left alone.

# r19: mask of 1 bit that will correspond to the rightmost item of any given shop.
#   It will be shifted twice to the right to check the left and middle items.

li      r19, 0x1            # This is a mask that will check which shop items are available

# grand canal left
cmpwi   r18, 0x65
beq     shop_selection_end
slwi    r19, r19, 3          # move the 3 bits to the next shop

# grand canal right
cmpwi   r18, 0x67
beq     shop_selection_end
slwi    r19, r19, 3          # move the 3 bits to the next shop

# pagoda peak bottom
cmpwi   r18, 0x10
beq     shop_selection_end
slwi    r19, r19, 3          # move the 3 bits to the next shop

# pagoda peak top
cmpwi   r18, 0x46
beq     shop_selection_end
slwi    r19, r19, 3          # move the 3 bits to the next shop

# neon heights left
cmpwi   r18, 0x0F
beq     shop_selection_end
slwi    r19, r19, 3          # move the 3 bits to the next shop

# neon heights right
cmpwi   r18, 0x77
beq     shop_selection_end
slwi    r19, r19, 3          # move the 3 bits to the next shop

# windmilleville left
cmpwi   r18, 0x5C
beq     shop_selection_end
slwi    r19, r19, 3          # move the 3 bits to the next shop

# windmilleville right
cmpwi   r18, 0x18
beq     shop_selection_end
slwi    r19, r19, 3          # move the 3 bits to the next shop

# bowser bottom
cmpwi   r18, 0x3B
beq     shop_selection_end
slwi    r19, r19, 3          # move the 3 bits to the next shop

# bowser top
cmpwi   r18, 0x85
beq     shop_selection_end
b       end

# which shop items have been checked are stored at 0x81720009 - 0x8172000C
shop_selection_end:

# r18: bit flags for each collected shop item from all shops
lis     r18, 0x8172
lwz     r18, 0x9(r18)

# r20: temp register for values to save.
# r21: offset for the capsule info array for item 1A. We will use the unused item ids of 1A, 1B, and 1C
# r22: index of current orb relative to all archapelago orbs
lis     r21, 0x8027
ori     r21, r21, 0x4898
cntlzw  r22, r19                    # count leading zeros in r19
li      r20, 31
subf    r22, r22, r20               # convert to trailing zeros


# leftmost shop item
and.    r20, r19, r18
beq     middle_shop_item

# store the new item id
li      r20, 0x1A
stb     r20, 3(r26)

# set the cost for the orb
li      r20, 5                      # left item has a cost of 5
stw     r20, 0x04(r26)

# set the model for an empty orb
lis     r20, 0x000F
ori     r20, r20, 0x001D
stw     r20, 0(r21)

# set the text for the orb
lis     r20, 0x0025
or      r20, r20, r22               # r22 has the index of the current orb as an archipelago item
stw     r20, 8(r21)                 # the text of the item is at an offset of 8 bytes from the start



middle_shop_item:
slwi    r19, r19, 1         # increment the shop item ordinal
addi    r22, r22, 1         # as well as the index
and.    r20, r19, r18
beq     right_shop_item

# store the new item id
li      r20, 0x1B
stb     r20, 0x1F(r26)

# set the cost for the orb
li      r20, 10                      # middle item has a cost of 10
stw     r20, 0x20(r26)

# set the model for an empty orb
lis     r20, 0x000F
ori     r20, r20, 0x001D
stw     r20, 0x28(r21)

# set the text for the orb
lis     r20, 0x0025
or      r20, r20, r22               # r22 has the index of the current orb as an archipelago item
stw     r20, 0x30(r21)              # the text of the item is at an offset of 8 bytes from the start



right_shop_item:
slwi    r19, r19, 1                 # increment the shop item ordinal
addi    r22, r22, 1                 # as well as the index
and.    r20, r19, r18
beq     shop_item_end

# store the new item id
li      r20, 0x1C
stb     r20, 0x3B(r26)

# set the cost for the orb
li      r20, 20                     # right item has a cost of 20
stw     r20, 0x3C(r26)

# set the model for an empty orb
lis     r20, 0x000F
ori     r20, r20, 0x001D
stw     r20, 0x50(r21)

# set the text for the orb
lis     r20, 0x0025
or      r20, r20, r22               # r22 has the index of the current orb as an archipelago item
stw     r20, 0x58(r21)              # the text of the item is at an offset of 8 bytes from the start

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
