        lw      0   1   n
        lw      0   6   factAd
        jalr    6   7
        halt
fact    sw      5   7   stack
        lw      0   6   one
        add     5   6   5
        sw      5   1   stack
        lw      0   6   one
        add     5   6   5
        beq     1   0   base
        lw      0   6   neg1
        add     1   6   1
        lw      0   6   factAd
        jalr    6   7
        lw      0   6   one
        add     1   6   1
        add     1   0   2
        add     0   0   4
mloop   beq     2   0   mdone
        add     4   3   4
        lw      0   6   neg1
        add     2   6   2
        beq     0   0   mloop
mdone   add     4   0   3
        beq     0   0   ret
base    lw      0   3   one
ret     lw      0   6   neg1
        add     5   6   5
        lw      5   1   stack
        add     5   6   5
        lw      5   7   stack
        jalr    7   6
n       .fill   5
one     .fill   1
neg1    .fill   -1
factAd  .fill   fact
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