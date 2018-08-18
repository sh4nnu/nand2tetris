#!/usr/bin/python

import os,sys

#Parser class
class Parser:
    def __init__(self, infile):
        self.infile = open(infile)
        self.command = [""]
        self.cursorAtEnd = False
        
        self.cType = {
            "add" : "C_ARITHMETIC",
            "sub" : "C_ARITHMETIC",
            "neg" : "C_ARITHMETIC",
            "eq" : "C_ARITHMETIC",
            "gt" : "C_ARITHMETIC",
            "lt" : "C_ARITHMETIC",
            "and" : "C_ARITHMETIC",
            "or" : "C_ARITHMETIC",
            "not" : "C_ARITHMETIC",
            "push" : "C_PUSH",
            "pop" : "C_POP",
            "EOF" : "C_EOF",
            }

        def hasMoreCommands(self):
            cursorPosition = self.infile.tell()
            self.advance()
            self.infile.seek(cursorPosition)
            return not self.cursorAtPos


        def advance(self):
            thisLine = self.inline.readline
            if thisLine == "":
                self.cursorAtEnd = True
            else:
                leximes = thisLine.split('/')[0].strip()
                if leximes == "":
                    self.advance()
                else:
                    self.command = leximes.split()
                    outfile.write(command[0])
            

        def commandType(self):
            return self.cType.get(self.command[0], "invalid command type")

        def arg1(self):
            return self.command[1]

        def arg2(self):
            return self.command[2]


    #Class for Code writer which translates the vm code to hack machine code.
    class CodeWriter:
        def __init__(self,dest):
            self.outfile = open(dest, "w")
            self.newLabel = 0 #we are going to create many labels here for push and pop, so we will be hav


        #translates the arithmetic implementations of the vm
        def writeArithmetic(self, command):
            text = ""
            if command == "add":
                text += "@SP\n" #pop first value from stack
                text += "AM = M - 1\n"
                text += "D = M\n"
                text += "@SP\n"
                text += "AM = M - 1\n"#popping second value from stack
                text += "M = D + M\n" #adding the two values
                text += "@SP\n" 
                text += "M = M + 1\n"# pushing back to stack

            elif command == "sub":
                text += "@SP\n"
                text += "AM = M - 1\n" # popping first element from the stack
                text += "D = M\n" #storing the value in D
                text += "@SP\n"
                text += "AM = M - 1\n"# popping second element 
                text += "M = D - M\n"# subtracting the two values
                text += "@SP\n"
                text += "M = M + 1\n" #pushing the result back to the stack

            elif command == "neg":
                text += "@SP\n"
                text += "A = M -1\n"#pop
                text += " M = -M\n"#negate
                
                
            elif command == "not":
                text += "@SP\n"
                text += "A = M -1\n"#pop
                text += " M = !M\n"#not !


            elif command == "and":
                text += "@SP\n"
                text += "AM = M - 1\n" #popping  the first element from the stack
                text += " D = M\n"#storing the first element
                text += "@SP\n"
                text += "A = M - 1\n"
                text += "M = D&M\n"#overwriting the second value with the result

            elif command == "or":
                text += "@SP\n"
                text += "AM = M - 1\n" #popping  the first element from the stack
                text += " D = M\n"#storing the first element
                text += "@SP\n"
                text += "A = M - 1\n"
                text += "M = D|M\n"#overwriting the second value with the result
                
            elif command == "eq":
                index = str(self.newLabel)
                self.newLabel += 1
                text += "@SP\n"
                text += "AM = M -1\n"#popping the latest value
                text += "D = M\n"
                text += "@SP\n"
                text += "A = M -1\n"
                text += "D = M - D\n"
                text += "M = -1\n"#setting result == true in before hand
                text += "@equal"+index+"\n"
                text += "D;JEQ\n" #if condition passes the true will be pushed to stack
                text += "@SP\n"
                text += "A = M - 1 \n"
                text += "M = 0\n"# else false  is pushed
                text += "(equal"+index+")\n"

            elif command == "gt":
                index = str(self.newLabel)
                self.newLabel += 1
                text += "@SP\n"
                text += "AM = M -1\n"
                text += "D = M\n"
                text += "@SP\n"
                text += "A = M -1\n"
                text += "D = M - D\n"
                text += "M = -1\n"
                text += "@greater"+index+"\n"
                text += "D;JGT\n"
                text += "@SP\n"
                text += "A = M - 1 \n"
                text += "M = 0\n"
                text += "(greater"+index+")\n"

            elif command == "lt":
                index = str(self.newLabel)
                self.newLabel += 1
                text += "@SP\n"
                text += "AM = M -1\n"
                text += "D = M\n"
                text += "@SP\n"
                text += "A = M -1\n"
                text += "D = M - D\n"
                text += "M = -1\n"
                text += "@lessthan"+index+"\n"
                text += "D;JLT\n"
                text += "@SP\n"
                text += "A = M - 1 \n"
                text += "M = 0\n"
                text += "(lessthan"+index+")\n"

            else:
                text = "command not yet implemented\n"
                self.outfile.write("//" + command +text)
                
                    
        def writePushPop(self, command, segment, index):
            text = ""
            if command == "push":
                if segement == "constant":
                    text += "@"+index+"\n"#take the constant in D reg                        
                    text += "D = A\n"                        
                    text += "@SP\n"                        
                    text += "A = M\n"                        
                    text += "M = D\n"#accesing *SP                      
                    text += "@SP\n"                        
                    text += "M = M + 1\n"# Incrementing SP pointer (SP++)                        

                elif segment == "static":
                    filename = self.infile[:-3]
                    text += "@"+filename+"."+index+"\n"                        
                    text += "D = M\n"                        
                    text += "@SP\n"                        
                    text += "A = M\n"                        
                    text += "M = D\n"                        
                    text += "@SP\n"                        
                    text += "M = M + 1\n"                        

                elif segment == "pointer":

                elif segment == "temp":

                elif segment == "local":

                elif segment == "argument":

                elif segment == "this":

                elif segment == "that":

                else:

            def Close(self):
                self.outfile = close()

text += "\n"                        
                    



#main function implementatin.

def main():
    source = sys.argv[1]
    parser = Parser(source + ".vm")
    codewriter = CodeWriter(source + ".asm")


if __name__ == "__main__":
    main()
