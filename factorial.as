        lw      0   1   n		reg1 = n
        lw      0   6   factAd	reg6 = factAd
        jalr    6   7			call subroutine fact
        halt				terminate program after complete
fact    sw      5   7   stack 	push return address to stack
        lw      0   6   one		reg6 = 1
        add     5   6   5		stack pointer = stack pointer + 1
        sw      5   1   stack	push parameter n to stack
        lw      0   6   one		reg6 = 1
        add     5   6   5		stack pointer = stack pointer + 1
        beq     1   0   base		if n == 0 jump to base case
        lw      0   6   neg1		reg6 = -1
        add     1   6   1 		n = n - 1
        lw      0   6   factAd    reg6 = facrAd
        jalr    6   7             recursive call: fact(n -1)
        lw      0   6   one		reg6 = 1
        add     1   6   1		restore original n: n = n + 1
        add     1   0   2		reg2 = n
        add     0   0   4		reg4 = 0
mloop   beq     2   0   mdone	if counter == 0, finish loop
        add     4   3   4		reg4 = reg4 + fact(n - 1)
        lw      0   6   neg1		reg6 = -1
        add     2   6   2		reg2 = reg2 - 1
        beq     0   0   mloop	repeat multiplication loop
mdone   add     4   0   3		reg3 = reg4 
        beq     0   0   ret		jump to return sequence
base    lw      0   3   one		base case: 0! = 1
ret     lw      0   6   neg1		reg6 = -1
        add     5   6   5		stack pointer = stack pointer - 1
        lw      5   1   stack	pop and restore reg1
        add     5   6   5		stack pointer = stack pointer - 1
        lw      5   7   stack	pop and restore reg7
        jalr    7   6			return to caller 
n       .fill   5				initial value of n 
one     .fill   1				constant 1
neg1    .fill   -1			constant -1
factAd  .fill   fact			entry point address of subroutine fact
stack   .fill   0       		temp storage area (stack)	
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