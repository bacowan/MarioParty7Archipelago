# code from the callsite
lwz     r0, 0x0004 (r4)

# check to see if the jump item was found (stored at 0x8172000D)
lis     r19, 0x8172
lbz     r19, 0xD(r19)

andi.   r19, r19, 1
bne+    end

# check the current minigame to see if we need to disable the A button
# current minigame is stored at 0x804ee8d1 (I think). It's set to 0x18 if there's no current minigame (I think)
lis     r19, 0x804E
ori     r19, r19, 0xE8D1
lbz     r19, 0(r19)

# Warp Pipe Dreams
cmplwi  r19, 0x2D
beq     mask_a

# Gimme a Sign
cmplwi  r19, 0x33
beq     mask_a

# Bridge Work
cmplwi  r19, 0x34
beq     mask_a

# Royal Rumpus
cmplwi  r19, 0x39
beq     mask_a

# Apes of Wrath
cmplwi  r19, 0x3B
beq     mask_a

# Camp Ukiki
cmplwi  r19, 0x3D
beq     mask_a

b       end

mask_a:
lis     r19, 0xFEFF
ori     r19, r19, 0xFFFF   # r19 = 0xFEFFFFFF
and     r0, r0, r19

end:

# go back to the callsite
lis r19, 0x800C
ori r19, r19, 0x7E30
mtctr r19
bctr
