.include "constants.inc"

.equ PLAYER_NUMBER_LOC,     0x80291522

# reg1 is output
# reg2 is just temporary register to use
.macro GET_CURRENT_PLAYER_DIFFICULTY reg1, reg2
    lis \reg1, PLAYER_NUMBER_LOC@h
    lbz \reg2, PLAYER_NUMBER_LOC@l(\reg1)

    # the player number will act as an offset from p1's info structure address. Structures are offset by 0x110 bytes.
    # r18 will now store the full offset.
    mulli \reg2, \reg2, PLAYER_STRUCT_SIZE

    # load the cpu difficulty/is-player value into memory
    lis \reg1, PLAYER_STRUCT_BASE_OFFSET@h
    ori \reg1, \reg1, PLAYER_STRUCT_BASE_OFFSET@l
    add \reg1, \reg1, \reg2 # add the offset to the base memory value
    lbz \reg1, 0(\reg1)
.endm

.macro BRANCH_IF_PLAYER in_r_player_number, tmp_r_offset, tmp_r_difficulty, branch
    # the player number will act as an offset from p1's info structure address. Structures are offset by 0x110 bytes.
    # \tmp_r_offset will now store the full offset.
    # \in_r_player_number stores the current player number
    mulli   \tmp_r_offset, \in_r_player_number, PLAYER_STRUCT_SIZE

    # load the cpu difficulty/is-player value into memory
    lis     \tmp_r_difficulty, PLAYER_STRUCT_BASE_OFFSET@h
    # add the offset to the base memory value
    add     \tmp_r_difficulty, \tmp_r_difficulty, \tmp_r_offset
    # 0x80290C98 is where the first difficulty/is-player value is stored
    lbz     \tmp_r_difficulty, PLAYER_STRUCT_BASE_OFFSET@l(\tmp_r_difficulty)

    andi.   \tmp_r_difficulty, \tmp_r_difficulty, IS_CPU_MASK_BIT          # this bit will be set for CPUs but not human players
    beq     \branch
.endm

.macro SET_REGISTER reg, val
    lis \reg, \val@h
    ori \reg, \reg, \val@l
.endm
