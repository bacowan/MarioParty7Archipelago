.include "constants.inc"

.equ r_CURRENT_MINIGAME_DATA_POINTER, r31
.equ r_MINIGAME_MAX_SPEED, f1

.equ GIMME_A_SIGN_LOC_P1,   0x80b46be0
.equ MAD_PROPS_LOC_P1,      0x809cdd60
.equ BRIDGE_WORK_LOC_P1,    0x80b25420
.equ APES_OF_WRATH_LOC_P1,  0x808b0f40
.equ SPIN_DOCTOR_LOC_P1,    0x80924bc0
.equ ROYAL_RUMPUS_LOC_P1,   0x808cb8c0
.equ WEIGHT_FOR_IT_LOC_P1,  0x8091e780
.equ WARP_PIPE_DREAMS_P1,   0x809b82e0

.equ GIMME_A_SIGN_LOC_P2,   0x80b46de0
.equ MAD_PROPS_LOC_P2,      0x809cdf60
.equ BRIDGE_WORK_LOC_P2,    0x80b25620
.equ APES_OF_WRATH_LOC_P2,  0x808b1140
.equ SPIN_DOCTOR_LOC_P2,    0x80924dc0
.equ ROYAL_RUMPUS_LOC_P2,   0x808cbac0
.equ WEIGHT_FOR_IT_LOC_P2,  0x8091e980
.equ WARP_PIPE_DREAMS_P2,   0x809b84e0

# r31 seems to have a pointer to some player data. The offset depends on which player.
# Road the expected value into r15 and compare with that

# Check which player the human player is. Branch to the corresponding section depending on if the human player is p1 or p2
lis     r15, PLAYER_STRUCT_BASE_OFFSET@h
lbz     r15, PLAYER_STRUCT_BASE_OFFSET@l(r15)    # load the value from memory
andi.   r15, r15, IS_CPU_MASK_BIT      # this bit will be set for CPUs but not human players
bne     player2

# p1 for gimme a sign.
lis     r15, GIMME_A_SIGN_LOC_P1@h         # Load upper 16 bits
ori     r15, r15, GIMME_A_SIGN_LOC_P1@l    # OR in lower 16 bits
cmpw    r_CURRENT_MINIGAME_DATA_POINTER, r15                        # Compare r3 with r0
beq     fix_speed

# p1 for mad props.
lis     r15, MAD_PROPS_LOC_P1@h         # Load upper 16 bits
ori     r15, r15, MAD_PROPS_LOC_P1@l    # OR in lower 16 bits
cmpw    r_CURRENT_MINIGAME_DATA_POINTER, r15            # Compare r3 with r0
beq     fix_speed

# p1 for bridge work.
lis     r15, BRIDGE_WORK_LOC_P1@h         # Load upper 16 bits
ori     r15, r15, BRIDGE_WORK_LOC_P1@l    # OR in lower 16 bits
cmpw    r_CURRENT_MINIGAME_DATA_POINTER, r15            # Compare r3 with r0
beq     fix_speed

# p1 for apes of wrath.
lis     r15, APES_OF_WRATH_LOC_P1@h         # Load upper 16 bits
ori     r15, r15, APES_OF_WRATH_LOC_P1@l    # OR in lower 16 bits
cmpw    r_CURRENT_MINIGAME_DATA_POINTER, r15            # Compare r3 with r0
beq     fix_speed

# p1 for spin doctor.
lis     r15, SPIN_DOCTOR_LOC_P1@h         # Load upper 16 bits
ori     r15, r15, SPIN_DOCTOR_LOC_P1@l    # OR in lower 16 bits
cmpw    r_CURRENT_MINIGAME_DATA_POINTER, r15            # Compare r3 with r0
beq     fix_speed

# p1 for royal rumpus.
lis     r15, ROYAL_RUMPUS_LOC_P1@h         # Load upper 16 bits
ori     r15, r15, ROYAL_RUMPUS_LOC_P1@l    # OR in lower 16 bits
cmpw    r_CURRENT_MINIGAME_DATA_POINTER, r15            # Compare r3 with r0
beq     fix_speed

# p1 for weight for it.
lis     r15, WEIGHT_FOR_IT_LOC_P1@h         # Load upper 16 bits
ori     r15, r15, WEIGHT_FOR_IT_LOC_P1@l    # OR in lower 16 bits
cmpw    r_CURRENT_MINIGAME_DATA_POINTER, r15            # Compare r3 with r0
beq     fix_speed

# p1 for warp pipe dreams.
lis     r15, WARP_PIPE_DREAMS_P1@h         # Load upper 16 bits
ori     r15, r15, WARP_PIPE_DREAMS_P1@l    # OR in lower 16 bits
cmpw    r_CURRENT_MINIGAME_DATA_POINTER, r15            # Compare r3 with r0
beq     fix_speed

# default logic
lfs     f1, 0x4(r29)
b       end


# player 2 checks
player2:

# p2 for gimme a sign.
lis     r15, GIMME_A_SIGN_LOC_P2@h         # Load upper 16 bits
ori     r15, r15, GIMME_A_SIGN_LOC_P2@l    # OR in lower 16 bits
cmpw    r_CURRENT_MINIGAME_DATA_POINTER, r15            # Compare r3 with r0
beq     fix_speed

# p2 for mad props.
lis     r15, MAD_PROPS_LOC_P2@h         # Load upper 16 bits
ori     r15, r15, MAD_PROPS_LOC_P2@l    # OR in lower 16 bits
cmpw    r_CURRENT_MINIGAME_DATA_POINTER, r15            # Compare r3 with r0
beq     fix_speed

# p2 for bridge work.
lis     r15, BRIDGE_WORK_LOC_P2@h         # Load upper 16 bits
ori     r15, r15, BRIDGE_WORK_LOC_P2@l    # OR in lower 16 bits
cmpw    r_CURRENT_MINIGAME_DATA_POINTER, r15            # Compare r3 with r0
beq     fix_speed

# p2 for apes of wrath.
lis     r15, APES_OF_WRATH_LOC_P2@h         # Load upper 16 bits
ori     r15, r15, APES_OF_WRATH_LOC_P2@l    # OR in lower 16 bits
cmpw    r_CURRENT_MINIGAME_DATA_POINTER, r15            # Compare r3 with r0
beq     fix_speed

# p2 for spin doctor.
lis     r15, SPIN_DOCTOR_LOC_P2@h         # Load upper 16 bits
ori     r15, r15, SPIN_DOCTOR_LOC_P2@l    # OR in lower 16 bits
cmpw    r_CURRENT_MINIGAME_DATA_POINTER, r15            # Compare r3 with r0
beq     fix_speed

# p2 for royal rumpus.
lis     r15, ROYAL_RUMPUS_LOC_P2@h         # Load upper 16 bits
ori     r15, r15, ROYAL_RUMPUS_LOC_P2@l    # OR in lower 16 bits
cmpw    r_CURRENT_MINIGAME_DATA_POINTER, r15            # Compare r3 with r0
beq     fix_speed

# p2 for weight for it.
lis     r15, WEIGHT_FOR_IT_LOC_P2@h         # Load upper 16 bits
ori     r15, r15, WEIGHT_FOR_IT_LOC_P2@l    # OR in lower 16 bits
cmpw    r_CURRENT_MINIGAME_DATA_POINTER, r15            # Compare r3 with r0
beq     fix_speed

# p2 for warp pipe dreams.
lis     r15, WARP_PIPE_DREAMS_P2@h         # Load upper 16 bits
ori     r15, r15, WARP_PIPE_DREAMS_P2@l    # OR in lower 16 bits
cmpw    r_CURRENT_MINIGAME_DATA_POINTER, r15            # Compare r3 with r0
beq     fix_speed

# default logic
lfs     f1, 0x4(r29)
b       end

# speed is stored here, and the max speed is added to the minimum speed, so that a value of 0 is the minimum speed
fix_speed:
lis     r16, MINIGAME_MAX_SPEED_SAVE@h
ori     r16, r16, MINIGAME_MAX_SPEED_SAVE@l
lfs     r_MINIGAME_MAX_SPEED, 0x0(r16)        # get the base value


addi    r1, r1, -8                                              # allocate 8 bytes on the stack
lis     r16, 0x3f00                                             # this (float 0.5) is the base value
stw     r16, 0(r1)                                              # store the value on the stack
lfs     f21, 0(r1)                                              # load the value in the stack
fadd    r_MINIGAME_MAX_SPEED, r_MINIGAME_MAX_SPEED, f21         # add it to f1. To go full speed this should be 0x3f00 0000 (float 0.5)
addi    r1, r1, 8                                               # restore the stack



end:
# go back to the callsite
lis r16, 0x8008
ori r16, r16, 0x068C
mtctr r16
bctr
