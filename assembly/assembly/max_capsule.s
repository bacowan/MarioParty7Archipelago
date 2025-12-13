# max capsule count is at 0x81720005
# 0b 0000 0000: 0 capsule max
# 0b 0000 0001: 1 capsule max
# 0b 0000 0010: 2 capsule max
# 0b 0000 0011: 3 capsule max

# r3 will also be the output
lis     r3, 0x8172
lbz     r3, 5(r3)

# the player number will act as an offset from p1's info structure address. Structures are offset by 0x110 bytes.
# r18 will now store the full offset.
# r21 stores the current player number (from code called before this)
mulli   r18, r21, 0x110

# load the cpu difficulty/is-player value into memory
lis     r17, 0x8029
add     r17, r17, r18           # add the offset to the base memory value
lbz     r17, 0x0C98(r17)        # 0x80290C98 is where the first difficulty/is-player value is stored

# if it is a computer player then set the max capsules to 3
andi.   r17, r17, 0x20          # this bit will be set for CPUs but not human players
beq     end

li      r3, 3

# go back to the callsite
end:
lis r17, 0x8016
ori r17, r17, 0x75BC
mtctr r17
bctr
