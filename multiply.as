        add     0   0   1           reg1 = result = 0
        lw      0   2   mcand       reg2 = mcand
        lw      0   3   mplier      reg3 = mplier
        lw      0   4   one         reg4 = mask = 1
        lw      0   6   count       reg6 = counter = 15
loop    nand    3   4   5           reg5 = NOT(mplier AND mask)
        nand    5   5   5           reg5 = mplier AND mask
        beq     5   0   next        if bit = 0 then skip to next
        add     1   2   1           result = result + mcand
next    add     2   2   2           mcand = mcand * 2 (shift left)
        add     4   4   4           mask = mask * 2 (shift left)
        lw      0   7   neg1        reg7 = -1
        add     6   7   6           counter = counter - 1
        beq     6   0   done        counter == 0 -> finish
        beq     0   0   loop        otherwise next iteration
done    halt
mcand   .fill   32766
mplier  .fill   10383
one     .fill   1
count   .fill   15
neg1    .fill   -1			 