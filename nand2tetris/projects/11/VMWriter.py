
class VMWriter:

    def __init__(self, opFile):
        self.op = opFile
        
    def writePush(self, segment, index):
        """ This handles the push command"""
        self.op.write("push "+ segement + " " + str(index) +"\n")

    def writePop(self, segment, index):
        """ This handles the pop command"""
        self.op.write("pop "+ segement + " " + str(index) +"\n")


    def writeArithmetic(self, command):
        """ This can handle all sort of VM commands such as
            ADD, SUB, NEG, EQ, GT, LT, AND, OR, NOT """
        self.op.write(command +"\n")
        
    def writeLabel(self, label):
        self.op.write("label "+ label +"\n")
        
    def writeGoto(self, label):
        self.op.write("goto "+ label +"\n")
        
    def writeIf(self, label):
        self.op.write("if-goto "+ label +"\n")
    
    def writeCall(self, name, nArgs):
        self.op.write("call "+ name + " " + nArgs +"\n")

    def writeFunction(self, name, nLocals):
        self.op.write("function " + name + " " + nLocals+"\n") 


    def writeReturn(self):
        self.write("return") 

    def close(self):
        self.op.close()

    
