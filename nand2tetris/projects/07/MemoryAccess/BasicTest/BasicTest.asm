// push constant 10
@10
D = A
@SP
A = M
M = D
@SP
M = M + 1
//poplocal0
@0
D = A
@LCL
D = M + D
@R13
M = D
@SP
AM = M - 1
D = M
@R13
A = M
M = D
// push constant 21
@21
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 22
@22
D = A
@SP
A = M
M = D
@SP
M = M + 1
//popargument2
@2
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
//popargument1
@1
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
// push constant 36
@36
D = A
@SP
A = M
M = D
@SP
M = M + 1
//popthis6
@6
D = A
@THIS
D = M + D
@R13
M = D
@SP
AM = M - 1
D = M
@R13
A = M
M = D
// push constant 42
@42
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 45
@45
D = A
@SP
A = M
M = D
@SP
M = M + 1
//popthat5
@5
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
// push constant 510
@510
D = A
@SP
A = M
M = D
@SP
M = M + 1
//poptemp6
@6
D = A
@5
D = A + D
@R13
M = D
@SP
AM = M - 1
D = M
@R13
A = M
M = D
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push that 5
@5
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
//sub
@SP
AM = M - 1
D = M
@SP
AM = M - 1
M = M - D
@SP
M = M + 1
// push this 6
@6
D = A
@THIS
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push this 6
@6
D = A
@THIS
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
//sub
@SP
AM = M - 1
D = M
@SP
AM = M - 1
M = M - D
@SP
M = M + 1
// push temp 6
@6
D = A
@5
A = A + D
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
