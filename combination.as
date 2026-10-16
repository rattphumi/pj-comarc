        lw      0   1   n
        lw      0   2   r
        lw      0   6   combAd
        jalr    6   7
        halt
comb    sw      5   7   stack
        lw      0   6   one
        add     5   6   5
        sw      5   1   stack
        lw      0   6   one
        add     5   6   5
        sw      5   2   stack
        lw      0   6   one
        add     5   6   5
        beq     0   2   base
        beq     1   2   base
        lw      0   6   neg1
        add     1   6   1
        lw      0   6   combAd
        jalr    6   7
        sw      5   3   stack
        lw      0   6   one
        add     5   6   5
        lw      0   6   neg1
        add     2   6   2
        lw      0   6   combAd
        jalr    6   7
        lw      0   6   neg1
        add     5   6   5
        lw      5   4   stack
        add     3   4   3
        beq     0   0   ret
base    lw      0   3   one
ret     lw      0   6   neg1
        add     5   6   5
        lw      5   2   stack
        add     5   6   5
        lw      5   1   stack
        add     5   6   5
        lw      5   7   stack
        jalr    7   6
n       .fill   7
r       .fill   3
one     .fill   1
neg1    .fill   -1
combAd  .fill   comb
stack   .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0
        .fill   0