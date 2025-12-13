# r20 will hold the max coin count (2 bytes)
lis     r20, 0x8172
ori     r20, r20, 0x0000
lhz     r20, 1(r20)

# the player number will act as an offset from p1's info structure address. Structures are offset by 0x110 bytes.
# r18 will now store the full offset.
# r30 stores the current player number (from code called before this)
mulli   r18, r30, 0x110

# load the cpu difficulty/is-player value into memory
lis     r17, 0x8029
ori     r17, r17, 0x0C98 # 0x80290C98 is where the first difficulty/is-player value is stored
add     r17, r17, r18 # add the offset to the base memory value
lbz     r17, 0(r17)

# if it is a computer player then set the max coin count to 999
andi.   r17, r17, 0x20 # this bit will be set for CPUs but not human players
beq     common

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
