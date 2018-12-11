//bootstrap

@256
D = A
@SP
M = D
//call Sys.init 0
@Sys.init$ret.1
D = A
@SP
A = M
M = D
@SP
M = M + 1
@LCL
D = M
@SP
A = M
M = D
@SP
M = M + 1
@ARG
D = M
@SP
A = M
M = D
@SP
M = M + 1
@THIS
D = M
@SP
A = M
M = D
@SP
M = M + 1
@THAT
D = M
@SP
A = M
M = D
@SP
M = M + 1
@SP
D = M
@LCL
M = D
@5
D = D - A
@ARG
M = D
@Sys.init$label
0;JMP
(Sys.init$ret.1)
(Sys.init$label)//function Sys.init 0
// push constant 4000
@4000
D = A
@SP
A = M
M = D
@SP
M = M + 1
//poppointer0
@0
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
// push constant 5000
@5000
D = A
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
//call Sys.main 0
@Sys.main$ret.2
D = A
@SP
A = M
M = D
@SP
M = M + 1
@LCL
D = M
@SP
A = M
M = D
@SP
M = M + 1
@ARG
D = M
@SP
A = M
M = D
@SP
M = M + 1
@THIS
D = M
@SP
A = M
M = D
@SP
M = M + 1
@THAT
D = M
@SP
A = M
M = D
@SP
M = M + 1
@SP
D = M
@LCL
M = D
@5
D = D - A
@ARG
M = D
@Sys.main$label
0;JMP
(Sys.main$ret.2)
//poptemp1
@1
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
(LOOP)//goto
@LOOP
0;JMP
(Sys.main$label)//function Sys.main 5
D = 0
@SP
A = M
M = D
@SP
M = M + 1
D = 0
@SP
A = M
M = D
@SP
M = M + 1
D = 0
@SP
A = M
M = D
@SP
M = M + 1
D = 0
@SP
A = M
M = D
@SP
M = M + 1
D = 0
@SP
A = M
M = D
@SP
M = M + 1
// push constant 4001
@4001
D = A
@SP
A = M
M = D
@SP
M = M + 1
//poppointer0
@0
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
// push constant 5001
@5001
D = A
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
// push constant 200
@200
D = A
@SP
A = M
M = D
@SP
M = M + 1
//poplocal1
@1
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
// push constant 40
@40
D = A
@SP
A = M
M = D
@SP
M = M + 1
//poplocal2
@2
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
// push constant 6
@6
D = A
@SP
A = M
M = D
@SP
M = M + 1
//poplocal3
@3
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
// push constant 123
@123
D = A
@SP
A = M
M = D
@SP
M = M + 1
//call Sys.add12 1
@Sys.add12$ret.3
D = A
@SP
A = M
M = D
@SP
M = M + 1
@LCL
D = M
@SP
A = M
M = D
@SP
M = M + 1
@ARG
D = M
@SP
A = M
M = D
@SP
M = M + 1
@THIS
D = M
@SP
A = M
M = D
@SP
M = M + 1
@THAT
D = M
@SP
A = M
M = D
@SP
M = M + 1
@SP
D = M
@LCL
M = D
@6
D = D - A
@ARG
M = D
@Sys.add12$label
0;JMP
(Sys.add12$ret.3)
//poptemp0
@0
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
// push local 1
@1
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 2
@2
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 3
@3
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 4
@4
D = A
@LCL
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
//add
@SP
AM = M - 1
D = M
@SP
AM = M - 1
M = D + M
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
//add
@SP
AM = M - 1
D = M
@SP
AM = M - 1
M = D + M
@SP
M = M + 1
//return
@LCL
D = M
@R13
M = D
@R13
D = M
@5
D = D - A
A = D
D = M
@R14
M = D
@SP
AM = M - 1
D = M
@ARG
A = M
M = D
@ARG
D = M + 1
@SP
M = D
@R13
D = M
@1
D = D - A
A = D
D = M
@THAT
M = D
@R13
D = M
@2
D = D - A
A = D
D = M
@THIS
M = D
@R13
D = M
@3
D = D - A
A = D
D = M
@ARG
M = D
@R13
D = M
@4
D = D - A
A = D
D = M
@LCL
M = D
@R14
A = M
0;JMP
(Sys.add12$label)//function Sys.add12 0
// push constant 4002
@4002
D = A
@SP
A = M
M = D
@SP
M = M + 1
//poppointer0
@0
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
// push constant 5002
@5002
D = A
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
// push constant 12
@12
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
//return
@LCL
D = M
@R13
M = D
@R13
D = M
@5
D = D - A
A = D
D = M
@R14
M = D
@SP
AM = M - 1
D = M
@ARG
A = M
M = D
@ARG
D = M + 1
@SP
M = D
@R13
D = M
@1
D = D - A
A = D
D = M
@THAT
M = D
@R13
D = M
@2
D = D - A
A = D
D = M
@THIS
M = D
@R13
D = M
@3
D = D - A
A = D
D = M
@ARG
M = D
@R13
D = M
@4
D = D - A
A = D
D = M
@LCL
M = D
@R14
A = M
0;JMP
