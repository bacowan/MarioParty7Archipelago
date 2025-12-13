# set trampoline address
lis r17, 0x8000
ori r17, r17, 0x36B8

# put the address in the ctr and jump there
mtctr r17
bctr


# the entire chunk that we're replacing is 14 lines long, so fill the rest with noop

nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
