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
            "push" : "push",
            "pop" : "pop",
            "EOF" : "C_EOF",
            }

    def hasMoreCommands(self):
        cursorPosition = self.infile.tell()
        self.advance()
        self.infile.seek(cursorPosition)
        return not self.cursorAtEnd


    def advance(self):
        thisLine = self.infile.readline()
	
        if thisLine == "":
            self.cursorAtEnd = True
        else:
            leximes = thisLine.strip()
		    
            if leximes == "":
                self.advance()
            else:
                self.command = leximes.split()
				
        

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
        self.source = dest[:-3]       

#translates the arithmetic implementations of the vm
    def close(self):
        self.outfile.close()
    
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
            text += "M = M - D\n"# subtracting the two values
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
        self.outfile.write("//" + command +"\n"+text)
            
                
    def writePushPop(self, command, segment, index):
        text = ""
        
        if command == "push":
            
            text += "// push " + segment + " "+index+"\n"
            if segment == "constant":
                text += "@"+index+"\n"#take the constant in D reg                        
                text += "D = A\n"                        
                text += "@SP\n"                        
                text += "A = M\n"                        
                text += "M = D\n"#accesing *SP                      
                text += "@SP\n"                        
                text += "M = M + 1\n"# Incrementing SP pointer (SP++)
                

            elif segment == "static":
                
                text += "@"+self.source+"."+index+"\n"                        
                text += "D = M\n"                        
                text += "@SP\n"                        
                text += "A = M\n"                        
                text += "M = D\n"                        
                text += "@SP\n"                        
                text += "M = M + 1\n"                        

            elif segment == "pointer":
                text += "@"+index+"\n"
                text += "D = A\n"
                text += "@3\n"
                text += "A = A + D\n"
                text += "D = M\n"
                text += "@SP\n"
                text += "A = M\n"
                text += "M = D\n"
                text += "@SP\n"
                text += "M = M + 1\n"
                
                
            elif segment == "temp":
                text +="@"+index+"\n"
                text += "D = A\n"
                text += "@5\n"
                text += "A = A + D\n"
                text += "D = M\n"
                text += "@SP\n"
                text += "A = M\n"
                text += "M = D\n"
                text += "@SP\n"
                text += "M = M + 1\n"
                

            elif segment == "local":
                text += "@"+index+"\n"
                text += "D = A\n"
                text += "@LCL\n"
                text += "A = M + D\n"
                text += "D = M\n"
                text += "@SP\n"
                text += "A = M\n"
                text += "M = D\n"
                text += "@SP\n"
                text += "M = M + 1\n"
                

            elif segment == "argument":
                text += "@"+index+"\n"
                text += "D = A\n"
                text += "@ARG\n"
                text += "A = M + D\n"
                text += "D = M\n"
                text += "@SP\n"
                text += "A = M\n"
                text += "M = D\n"
                text += "@SP\n"
                text += "M = M + 1\n"
                

            elif segment == "this":
                text += "@"+index+"\n"
                text += "D = A\n"
                text += "@THIS\n"
                text += "A = M + D\n"
                text += "D = M\n"
                text += "@SP\n"
                text += "A = M\n"
                text += "M = D\n"
                text += "@SP\n"
                text += "M = M + 1\n"
                


            elif segment == "that":
                text += "@"+index+"\n"
                text += "D = A\n"
                text += "@THAT\n"
                text += "A = M + D\n"
                text += "D = M\n"
                text += "@SP\n"
                text += "A = M\n"
                text += "M = D\n"
                text += "@SP\n"
                text += "M = M + 1\n"
                


            else:
                text += segment + "not implemented yet please wait till we develop it!\n"

        elif command == "pop":
            text += "//pop" + segment + index+ "\n"
            if segment == "static":
                
                text += "@SP\n"
                text += "AM = M -1\n"#pop value into D
                text += "D = M\n"
                text += "@"+self.source+"."+index+"\n"#storing the popped value in static variable
                text += "M = D\n"

            elif segment == "this":
                text += "@"+index+"\n" #get the address
                text += "D = A\n"
                text += "@THIS\n"
                text += "D = M + D\n"
                text += "@R13\n"
                text += "M = D\n"# store the address in R13
                text += "@SP\n"
                text += "AM = M - 1\n"
                text += "D = M\n"#pop value into D
                text += "@R13\n"#address back in R13
                text += "A = M\n"
                text += "M = D\n"

            elif segment == "that":
                text += "@"+ index + "\n"
                text += "D = A\n"
                text += "@THAT\n"
                text += "D = M + D\n"
                text += "@R13\n"
                text += "M = D\n"
                text += "@SP\n"
                text += "AM = M - 1\n"
                text += "D = M\n"
                text += "@R13\n"
                text += "A = M\n"
                text += "M = D\n"
                
                
            elif segment == "argument":
                text += "@"+ index + "\n"
                text += "D = A\n"
                text += "@ARG\n"
                text += "D = M + D\n"
                text += "@R13\n"
                text += "M = D\n"
                text += "@SP\n"
                text += "AM = M - 1\n"
                text += "D = M\n"
                text += "@R13\n"
                text += "A = M\n"
                text += "M = D\n"

            

            elif segment == "local":

                text += "@"+ index + "\n"
                text += "D = A\n"
                text += "@LCL\n"
                text += "D = M + D\n"
                text += "@R13\n"
                text += "M = D\n"
                text += "@SP\n"
                text += "AM = M - 1\n"
                text += "D = M\n"
                text += "@R13\n"
                text += "A = M\n"
                text += "M = D\n"
            
            elif segment == "pointer":
                text += "@"+ index + "\n"
                text += "D = A\n"
                text += "@3\n"
                text += "D = A + D\n"
                text += "@R13\n"
                text += "M = D\n"
                text += "@SP\n"
                text += "AM = M - 1\n"
                text += "D = M\n"
                text += "@R13\n"
                text += "A = M\n"
                text += "M = D\n"
                
                
            elif segment == "temp":
                text += "@"+ index + "\n"
                text += "D = A\n"
                text += "@5\n"
                text += "D = A + D\n"
                text += "@R13\n"
                text += "M = D\n"
                text += "@SP\n"
                text += "AM = M - 1\n"
                text += "D = M\n"
                text += "@R13\n"
                text += "A = M\n"
                text += "M = D\n"

            else:
                text += segment + "not implemented yet, Can't pop."
                self.outfile.write("//" + command +text)                                
        self.outfile.write(text)
#	def writeError(self):
#		self.outfile.write("ERROR:  Command Not Recognized")



#main function implementatin.

def main():
    source = sys.argv[1]
    parser = Parser(source + ".vm")
    codewriter = CodeWriter(source + ".asm")

    while parser.hasMoreCommands():
        parser.advance()
        cType = parser.commandType()

        if cType =="push" or cType == "pop":
            codewriter.writePushPop(cType, parser.arg1(), parser.arg2())
        elif cType == "C_ARITHMETIC":
            codewriter.writeArithmetic(parser.command[0])
#        else:
#            codewriter.writeError()
    
    codewriter.close()

if __name__ == "__main__":
    main()
