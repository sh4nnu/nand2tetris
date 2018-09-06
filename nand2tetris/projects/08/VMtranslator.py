#!/usr/bin/python

import os,sys,glob,errno

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
            "goto" : "C_BRANCH",
            "if-goto" : "C_BRANCH",
            "label" : "C_BRANCH",
            "call" : "C_CALL",
            "function" : "C_FUNCTION",
            "return" : "C_RETURN"
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
        self.functionCall = 0
    #set file name
    def set_file_name(self,fileName):
        self.source = fileName.replace(".vm","").split('/')[-1]    


    def close(self):
        self.outfile.close()

#bootstrap code
    def writeInit(self):
        text = "//bootstrap\n\n"
        text += "@256\n"
        text += "D = A\n"
        text += "@SP\n"
        text += "M = D\n"
        
        self.outfile.write(text)
        self.writeCall('Sys.init','0')

        
#creates a label (LABEL) in assembly         
    def writeLabel(self,string):
        text = "("+string+")"
        self.outfile.write(text)

#goto command to jum to any label
    def writeGoto(self,string):
        text = ""
        text += "@"+string+"\n"
        text += "0;JMP\n"
        self.outfile.write("//goto\n"+text)
        
#imlementing if conitional branching
    def writeIf(self,string):
        text = ""
        text += "@SP\n"
        text += "AM = M -1\n"
        text += "D = M\n"
        text += "@"+string+"\n"
        text += "D;JNE\n"
        self.outfile.write("//if statement\n"+text)
        
        
        
#function to handle all the  three branching commands
    def writeBranching(self, command, location):
        if command == "label":
            self.writeLabel(location)
        elif command == "goto":
            self.writeGoto(location)
        elif command == "if-goto":
            self.writeIf(location)
        else:
            self.outfile.write("this implementation is not found yet:"+ command)

#implementing function handling
    def writeFunction(self, funcName, nVar):
        
        self.writeLabel(funcName+"$label")
        text = ""
        for i in range(int(nVar)):             
            text += "D = 0\n"                        
            text += "@SP\n"                        
            text += "A = M\n"                        
            text += "M = D\n"#accesing *SP                      
            text += "@SP\n"                        
            text += "M = M + 1\n"# Incrementing SP pointer (SP++)
        self.outfile.write("//function "+funcName+" "+nVar+"\n"+text)
    def writeCall(self, funcName, nVar):
        
        text = ""
        self.functionCall+=1
        text += "@"+funcName+"$ret."+str(self.functionCall)+"\n"#label the return address.
        text += "D = A\n"
        text += "@SP\n"
        text += "A = M\n"
        text += "M = D\n"
        text += "@SP\n"
        text += "M = M + 1\n"

       ##
        text += "@LCL\n"# push LCL
        text += "D = M\n"
        text += "@SP\n"
        text += "A = M\n"
        text += "M = D\n"
        text += "@SP\n"
        text += "M = M + 1\n"

        text += "@ARG\n"# push ARG
        text += "D = M\n"
        text += "@SP\n"
        text += "A = M\n"
        text += "M = D\n"
        text += "@SP\n"
        text += "M = M + 1\n"

        text += "@THIS\n"# push THIS
        text += "D = M\n"
        text += "@SP\n"
        text += "A = M\n"
        text += "M = D\n"
        text += "@SP\n"
        text += "M = M + 1\n"

        text += "@THAT\n"# push THAT
        text += "D = M\n"
        text += "@SP\n"
        text += "A = M\n"
        text += "M = D\n"
        text += "@SP\n"
        text += "M = M + 1\n"

        
        text += "@SP\n"#LCL = SP
        text += "D = M\n"
        text += "@LCL\n"
        text += "M = D\n"

        
       #ARG = SP - nVar - 5
        text += "@"+str(5+int(nVar))+"\n"
        text += "D = D - A\n"
        text += "@ARG\n"
        text += "M = D\n"
        

        
        #go to function
        text += "@"+funcName+"$label\n"#goto function name.
        text += "0;JMP\n"
        
        ##
        
        text += "("+funcName+"$ret."+str(self.functionCall) +")\n"

        self.outfile.write("//call "+funcName+" "+nVar+"\n"+text)
#implementing returning a function
    def writeReturn(self):
        endFrame = 'R13'
        retAddr = 'R14' 
        text = ""
        text += "@LCL\n"#endFrame = LCL
        text += "D = M\n"
        text += "@"+endFrame+"\n"
        text += "M = D\n"

        text += "@"+endFrame+"\n"#*(endFrame-5)
        text += "D = M\n"
        text += "@5\n"
        text += "D = D - A\n"
        text += "A = D\n"
        text += "D = M\n"
        #retAddr = *(endFrame)
        text += "@"+retAddr+"\n"
        text += "M = D\n"

        text += "@SP\n"#replacing ARG with return value
        text += "AM = M - 1\n"#*ARG = pop()
        text += "D = M\n"
        text += "@ARG\n"
        text += "A = M\n"
        text += "M = D\n"

        text += "@ARG\n"#SP = ARG + 1
        text += "D = M + 1\n"
        text += "@SP\n"
        text += "M = D\n"

        retset = 1
        for addr in ["@THAT", "@THIS", "@ARG", "@LCL"]:
            
            text += "@"+endFrame+"\n"#THAT = *(endFrame -1)
            text += "D = M\n"
            text += "@"+str(retset)+"\n"
            text += "D = D - A\n"
            text += "A = D\n"
            text += "D = M\n"
            text += addr+"\n"
            text += "M = D\n"
            retset += 1

        #goto return
        text += "@"+retAddr+"\n"
        text += "A = M\n"
        text += "0;JMP\n"

        self.outfile.write("//return\n"+text)


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
                text += "AM = M - 1\n"#pop value into D
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
    
    coreInFile = sys.argv[1]
    if coreInFile[-3:] == ".vm":
        out = coreInFile[:-3]
    else:
        out = coreInFile
    codewriter = CodeWriter(out + ".asm")

    
#function which handles writing of all code.
    def writer(file):
        source = file    
        
        if source[-3:] == ".vm":
            source = source[:-3]
        parser = Parser(source + ".vm")
        
        codewriter.writeInit()
        while parser.hasMoreCommands():
            parser.advance()
            cType = parser.commandType()
            if cType =="push" or cType == "pop":
                codewriter.writePushPop(cType, parser.arg1(), parser.arg2())
            elif cType == "C_ARITHMETIC":
                codewriter.writeArithmetic(parser.command[0])
            elif cType == "C_BRANCH":
                codewriter.writeBranching(parser.command[0], parser.arg1())
            elif cType == "C_FUNCTION":
                codewriter.writeFunction(parser.arg1(),parser.arg2())

            elif cType == "C_CALL":
                codewriter.writeCall(parser.arg1(),parser.arg2())

            elif cType == "C_RETURN":
                codewriter.writeReturn()
        
        

#If the  given argument is a file.

    if os.path.isfile(coreInFile):
        writer(coreInFile)



    elif os.path.isdir(coreInFile):
        path = "./"+coreInFile+"/*.vm"
        files = glob.glob(path)
        for name in files:
            try:
                codewriter.set_file_name(name)
                writer(name)
            
            except IOError as e:
                if e.errno != errno.EISDIR:
                    raise
            
        
        
    codewriter.close()

if __name__ == "__main__":
    main()
