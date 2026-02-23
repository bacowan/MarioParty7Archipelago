.include "constants.inc"

.equ r_UNLOCK_FOUND, r19
.equ r_CURRENT_MINIGAME, r19
.equ r_OUTPUT, r0
.equ MASK_A, 0xFEFFFFFF

# code from the callsite
lwz     r0, 0x0004 (r4)

# check to see if the jump item was found (stored at 0x8172000D)
lis     r19, LOCK_JUMP_SAVE@h
lbz     r_UNLOCK_FOUND, LOCK_JUMP_SAVE@l(r19)

andi.   r19, r_UNLOCK_FOUND, 1
bne+    end

# check the current minigame to see if we need to disable the A button
# current minigame is stored at 0x80291559 (I think). It's set to 0x18 if there's no current minigame (I think)
lis     r19, CURRENT_MINIGAME_OFFSET@h
ori     r19, r19, CURRENT_MINIGAME_OFFSET@l
lbz     r_CURRENT_MINIGAME, 0(r19)

# Warp Pipe Dreams
cmplwi  r_CURRENT_MINIGAME, 0x2D
beq     mask_a

# Gimme a Sign
cmplwi  r_CURRENT_MINIGAME, 0x33
beq     mask_a

# Bridge Work
cmplwi  r_CURRENT_MINIGAME, 0x34
beq     mask_a

# Royal Rumpus
cmplwi  r_CURRENT_MINIGAME, 0x39
beq     mask_a

# Apes of Wrath
cmplwi  r_CURRENT_MINIGAME, 0x3B
beq     mask_a

# Camp Ukiki
cmplwi  r_CURRENT_MINIGAME, 0x3D
beq     mask_a

b       end

mask_a:
.equ r_MASK_A, r19
lis     r_MASK_A, MASK_A@h
ori     r_MASK_A, r_MASK_A, MASK_A@l   # r19 = 0xFEFFFFFF
and     r_OUTPUT, r_OUTPUT, r_MASK_A

end:

# go back to the callsite
lis r19, 0x800C
ori r19, r19, 0x7E30
mtctr r19
bctr
