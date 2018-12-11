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
// push constant 6
@6
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 8
@8
D = A
@SP
A = M
M = D
@SP
M = M + 1
//call Class1.set 2
@Class1.set$ret.2
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
@7
D = D - A
@ARG
M = D
@Class1.set$label
0;JMP
(Class1.set$ret.2)
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
// push constant 23
@23
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 15
@15
D = A
@SP
A = M
M = D
@SP
M = M + 1
//call Class2.set 2
@Class2.set$ret.3
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
@7
D = D - A
@ARG
M = D
@Class2.set$label
0;JMP
(Class2.set$ret.3)
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
//call Class1.get 0
@Class1.get$ret.4
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
@Class1.get$label
0;JMP
(Class1.get$ret.4)
//call Class2.get 0
@Class2.get$ret.5
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
@Class2.get$label
0;JMP
(Class2.get$ret.5)
(WHILE)//goto
@WHILE
0;JMP
//bootstrap

@256
D = A
@SP
M = D
//call Sys.init 0
@Sys.init$ret.6
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
(Sys.init$ret.6)
(Class1.set$label)//function Class1.set 0
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
//popstatic0
@SP
AM = M - 1
D = M
@Class1.0
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
//popstatic1
@SP
AM = M - 1
D = M
@Class1.1
M = D
// push constant 0
@0
D = A
@SP
A = M
M = D
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
(Class1.get$label)//function Class1.get 0
// push static 0
@Class1.0
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push static 1
@Class1.1
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
//bootstrap

@256
D = A
@SP
M = D
//call Sys.init 0
@Sys.init$ret.7
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
(Sys.init$ret.7)
(Class2.set$label)//function Class2.set 0
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
//popstatic0
@SP
AM = M - 1
D = M
@Class2.0
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
//popstatic1
@SP
AM = M - 1
D = M
@Class2.1
M = D
// push constant 0
@0
D = A
@SP
A = M
M = D
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
(Class2.get$label)//function Class2.get 0
// push static 0
@Class2.0
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push static 1
@Class2.1
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
