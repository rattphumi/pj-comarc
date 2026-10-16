        lw      0   1   n		reg1 = n 		
        lw      0   2   r		reg2 = r 
        lw      0   6   combAd	reg6 = combAd 	
        jalr    6   7			call subroutine comb 
        halt				terminate program 	
comb    sw      5   7   stack	push return address (reg7) to stack 
        lw      0   6   one		reg6 = 1 
        add     5   6   5		stack pointer = stack pointer + 1 
        sw      5   1   stack	push parameter n (reg1) to stack 
        lw      0   6   one		reg6 = 1 
        add     5   6   5		stack pointer = stack pointer + 1 
        sw      5   2   stack	push parameter r (reg2) to stack 	
        lw      0   6   one		reg6 = 1 
        add     5   6   5		stack pointer = stack pointer + 1 
        beq     0   2   base		if r == 0, branch to base case
        beq     1   2   base		if n == r, branch to base case 
        lw      0   6   neg1		reg6 = -1 
        add     1   6   1		n = n-1prepare argument for C(n-1,r)
        lw      0   6   combAd	reg6 = combAd 
        jalr    6   7			recursive call 1:compute comb(n-1, r) 
        sw      5   3   stack	push result of comb(n-1, r) from reg3 to stack 
        lw      0   6   one		reg6 = 1 
        add     5   6   5		stack pointer = stack pointer + 1 
        lw      0   6   neg1		reg6 = -1 
        add     2   6   2		r = r - 1prepare argument for C(n-1, r-1)) 
        lw      0   6   combAd	reg6 = combAd 
        jalr    6   7			recursive call 2:compute comb(n-1, r-1)   
        lw      0   6   neg1		reg6 = -1 
        add     5   6   5		stack pointer = stack pointer -1
        lw      5   4   stack	pop result of comb(n-1, r) into reg4 
        add     3   4   3		reg3 = comb(n-1, r-1) + comb(n-1, r)
        beq     0   0   ret		unconditional branch to return epilogue
base    lw      0   3   one		base case: set return value reg3 = 1
ret     lw      0   6   neg1		reg6 = -1
        add     5   6   5		stack pointer  = stack pointer - 1
        lw      5   2   stack	pop and restore reg2 from stack
        add     5   6   5		stack pointer  = stack pointer - 1
        lw      5   1   stack	pop and restore reg1 from stack
        add     5   6   5		stack pointer  = stack pointer - 1
        lw      5   7   stack	pop and restore reg7 from stack
        jalr    7   6			return to caller
n       .fill   7				input parameter n = 7
r       .fill   3				input parameter r = 3
one     .fill   1				constant 1
neg1    .fill   -1			    constant -1
combAd  .fill   comb			address pointer to subroutine comb	
stack   .fill   0				temp storage area (stack)
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