//bootstrap

@256
D = A
@SP
M = D
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
//poppointer1
@1
D = A
@3
D = A + D
@R13
M = D
@SP
AM = M - 1
D = M
@R13
A = M
M = D
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
//popthat0
@0
D = A
@THAT
D = M + D
@R13
M = D
@SP
AM = M - 1
D = M
@R13
A = M
M = D
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
//popthat1
@1
D = A
@THAT
D = M + D
@R13
M = D
@SP
AM = M - 1
D = M
@R13
A = M
M = D
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 2
@2
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
//popargument0
@0
D = A
@ARG
D = M + D
@R13
M = D
@SP
AM = M - 1
D = M
@R13
A = M
M = D
(MAIN_LOOP_START)// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
//if statement
@SP
AM = M -1
D = M
@COMPUTE_ELEMENT
D;JGT
//goto
@END_PROGRAM
0;JMP
(COMPUTE_ELEMENT)// push that 0
@0
D = A
@THAT
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push that 1
@1
D = A
@THAT
A = M + D
D = M
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
//popthat2
@2
D = A
@THAT
D = M + D
@R13
M = D
@SP
AM = M - 1
D = M
@R13
A = M
M = D
// push pointer 1
@1
D = A
@3
A = A + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
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
//poppointer1
@1
D = A
@3
D = A + D
@R13
M = D
@SP
AM = M - 1
D = M
@R13
A = M
M = D
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
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
//popargument0
@0
D = A
@ARG
D = M + D
@R13
M = D
@SP
AM = M - 1
D = M
@R13
A = M
M = D
//goto
@MAIN_LOOP_START
0;JMP
(END_PROGRAM)