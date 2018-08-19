// push constant 17
@17
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 17
@17
D = A
@SP
A = M
M = D
@SP
M = M + 1
//eq
@SP
AM = M -1
D = M
@SP
A = M -1
D = M - D
M = -1
@equal0
D;JEQ
@SP
A = M - 1 
M = 0
(equal0)
// push constant 17
@17
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 16
@16
D = A
@SP
A = M
M = D
@SP
M = M + 1
//eq
@SP
AM = M -1
D = M
@SP
A = M -1
D = M - D
M = -1
@equal1
D;JEQ
@SP
A = M - 1 
M = 0
(equal1)
// push constant 16
@16
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 17
@17
D = A
@SP
A = M
M = D
@SP
M = M + 1
//eq
@SP
AM = M -1
D = M
@SP
A = M -1
D = M - D
M = -1
@equal2
D;JEQ
@SP
A = M - 1 
M = 0
(equal2)
// push constant 892
@892
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 891
@891
D = A
@SP
A = M
M = D
@SP
M = M + 1
//lt
@SP
AM = M -1
D = M
@SP
A = M -1
D = M - D
M = -1
@lessthan3
D;JLT
@SP
A = M - 1 
M = 0
(lessthan3)
// push constant 891
@891
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 892
@892
D = A
@SP
A = M
M = D
@SP
M = M + 1
//lt
@SP
AM = M -1
D = M
@SP
A = M -1
D = M - D
M = -1
@lessthan4
D;JLT
@SP
A = M - 1 
M = 0
(lessthan4)
// push constant 891
@891
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 891
@891
D = A
@SP
A = M
M = D
@SP
M = M + 1
//lt
@SP
AM = M -1
D = M
@SP
A = M -1
D = M - D
M = -1
@lessthan5
D;JLT
@SP
A = M - 1 
M = 0
(lessthan5)
// push constant 32767
@32767
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 32766
@32766
D = A
@SP
A = M
M = D
@SP
M = M + 1
//gt
@SP
AM = M -1
D = M
@SP
A = M -1
D = M - D
M = -1
@greater6
D;JGT
@SP
A = M - 1 
M = 0
(greater6)
// push constant 32766
@32766
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 32767
@32767
D = A
@SP
A = M
M = D
@SP
M = M + 1
//gt
@SP
AM = M -1
D = M
@SP
A = M -1
D = M - D
M = -1
@greater7
D;JGT
@SP
A = M - 1 
M = 0
(greater7)
// push constant 32766
@32766
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 32766
@32766
D = A
@SP
A = M
M = D
@SP
M = M + 1
//gt
@SP
AM = M -1
D = M
@SP
A = M -1
D = M - D
M = -1
@greater8
D;JGT
@SP
A = M - 1 
M = 0
(greater8)
// push constant 57
@57
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 31
@31
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 53
@53
D = A
@SP
A = M
M = D
@SP
M = M + 1
//add
@SP
AM = M - 1
D = M
@SP
AM = M - 1
M = D + M
@SP
M = M + 1
// push constant 112
@112
D = A
@SP
A = M
M = D
@SP
M = M + 1
//sub
@SP
AM = M - 1
D = M
@SP
AM = M - 1
M = M - D
@SP
M = M + 1
//neg
@SP
A = M -1
 M = -M
//and
@SP
AM = M - 1
 D = M
@SP
A = M - 1
M = D&M
// push constant 82
@82
D = A
@SP
A = M
M = D
@SP
M = M + 1
//or
@SP
AM = M - 1
 D = M
@SP
A = M - 1
M = D|M
//not
@SP
A = M -1
 M = !M
