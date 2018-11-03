
#!/usr/bin/python

import os,sys,glob,errno,shlex,re
import xml.etree.ElementTree as xml




import SymbolTable
import VMWriter









class jackTokenizer:
  #regex for lexical elements
    re_integer = '\d+'
    re_symbol = '\{|\}|\(|\)|\[|\]|\.|\,|\;|\+|-|\*|/|&|\||\<|\>|=|_|~'
    re_string = '"[^"]*"'
    re_identifier = '[A-Z_]|[a-z]'

    
    #keywords
    keyword = {
            'class' : 'CLASS',
            'constructor' : 'CONSTRUCTOR',
            'function': 'FUNCTION',
            'method' : 'METHOD',
            'field' : 'FIELD',
            'static' : 'STATIC',
            'var' : 'VAR',
            'int' : 'INT',
            'char' : 'CHAR',
            'boolean' : 'BOOLEAN',
            'void' : 'VOID',
            'true' : 'TRUE',
            'false' : 'FALSE',
            'null' : 'NULL',
            'this' : 'THIS',
            'let' : 'LET',
            'do' : 'DO',
            'if' : 'IF',
            'else' : 'ELSE',
            'while' : 'WHILE',
            'return' : 'RETURN'
        }
    
    def __init__(self, inpfile):
        self.infile = open(inpfile)        
        self.tokens = self.infile.read()
        self.token = ""
        
        self.removeComments(self.tokens)
        self.tokenize(self.tokens)


        
    def hasMoreTokens(self):
        if len(self.tokens) != 0:
            return True
        return False

    def advance(self):
        if self.hasMoreTokens():
            self.token =self.tokens[0]                
            print("token: " + str(self.token)+" type: " + self.tokenType())
            print( self.token)
            
            self.tokens = self.tokens[1:]

        
        return self.token
            
        
    def removeComments(self, lines):
        
        uncommented = re.sub('//.*?\n', '\n', lines)
        uncommented = re.sub('/\*.*?\*/', '', uncommented, flags=re.DOTALL)
        self.tokens = uncommented
        #print uncommented

    def tokenize(self,l):
        
        reg = '('+'|'.join(exp for exp in[self.re_symbol,self.re_string]) + ')|\s+'
        split_codes = re.split(reg,l)

        split_codes = filter(None, split_codes)

        self.tokens = list(split_codes)
        
    def nextToken(self):
        if self.hasMoreTokens():
            return self.tokens[0]
        else:
            return ("ERROR!!!")
    #returns the type of the next token

    def nextValue(self):
        element = self.nextToken()
        if element in self.keyword.keys():
            return 'keyword'
        elif re.match(self.re_integer,element):
            return 'integerConstant'
        elif re.match(self.re_symbol, element):
            return 'symbol'
        elif re.match(self.re_identifier, element):
            return 'identifier'
        elif re.match(self.re_string, element):
            return 'stringConstant'
        else:
            return 'NONE'
    
    #-- API Routines Begin

    def tokenType(self):
        if self.token in self.keyword.keys():
            return 'keyword'
        elif re.match(self.re_integer,self.token):
            return 'integerConstant'
        elif re.match(self.re_symbol,self.token):
            return 'symbol'
        elif re.match(self.re_identifier,self.token):
            return 'identifier'
        elif re.match(self.re_string,self.token):
            return 'stringConstant'
        else:
            return 'NONE'
                
    #def keyWord(self):
        






class compilationEngine:

    

    spl_char = { '<':'&lt;', '>':'&gt;', '"':'&quot;','&':'&amp;'}
    
    def __init__(self, infile, outfile):
        self.className=""
        self.symbolTable = SymbolTable.SymbolTable()        
        self.tokenizer = jackTokenizer(infile)
        self.writer = VMWriter.VMWriter(outfile)
        self.indent = ""
##        self.mStack =[] #a stack to store all non terminal blocks opened which have to be closed
        self.keywordConsts = {'true', 'false','null','this'}
        self.binaryOp = {'+','-','*','|','<','>','=','/','&'}
        self.unaryOp = {'-','~'}

        
###    def addIndent(self):
###       self.indent +="    "
##
###    def removeIndent(self):
###        self.indent = self.indent[:-4]
##    
##
###    def writeTerm(self, token, Ttype):
###        self.op.write(self.indent+"<"+Ttype+">"+ token + "</"+Ttype+">\n")
##
##
##    def startNonTerm(self, rule):
###        self.op.write(self.indent+"<"+rule+">\n")
###        self.addIndent()
##        self.mStack.append(rule)
##
##
##    def endNonTerm(self):
##        rule = self.mStack.pop()
###        self.removeIndent()
###        self.op.write(self.indent+"</"+rule+">\n")
##        
##    #method for checking symbol table
####
####    #def sWrite(self, name):
####    #   self.op.write("## ["+name+" "+self.symbolTable.typeOf(name)+" "+\
####    #      self.symbolTable.kindOf(name)+ " " +str(self.symbolTable.indexOf(name))+ "] ##\n")
####


    def advance(self):
        token = self.tokenizer.advance()
        Ttype = self.tokenizer.tokenType()
        #handle string constant
        if Ttype == "stringConstant":
            token = token[1:-1]

        if token in self.spl_char.keys():
            token = self.spl_char[token]
        #self.writeTerm(token, Ttype)
        
            
        return token

    def nextValue(self):
        value = self.tokenizer.nextValue()
        return value
        
    def nextToken(self):
        return self.tokenizer.nextToken()

    def writeArrayIndex(self):
        self.advance()  #get "["
        self.compileExpression() # compile the expression in the indexholder
        self.advance() # get "]"

    def existExpression(self):
        return self.existTerm()

    def existTerm(self):
        token = self.nextToken()
        Ttype = self.nextValue()

        return (Ttype == "integerConstant" or Ttype == "stringConstant" \
            or Ttype == "identifier" or token in self.unaryOp \
            or token in self.keywordConsts or token == "(")
            

    def existStatement(self):
        return (self.nextToken() == "do") \
               or (self.nextToken() == "let") \
               or (self.nextToken() == "if") \
               or (self.nextToken() == "while") \
               or (self.nextToken() == "return") \

    
    def existVarDec(self):
        return (self.nextToken() == "var")

    def existClassVarDec(self):
        return (self.nextToken() == "static" or self.nextToken() == "field")

    def existSubroutineDec(self):
        return (self.nextToken() == "constructor" or self.nextToken() == "function" or self.nextToken() == "method")

    def existParameter(self):
        return not (self.nextValue() == "symbol")

    def writeParameter(self):
        
        typ = self.advance() # get type
        name = self.advance() # get var name
        self.symbolTable.define(name, typ, "arg")
        if (self.nextToken() == ","):
            self.advance() # get ","

    def  eat(self,string):   # check for expected elements in the grammar
        nextToken= self.nextToken()
        #print("!!"+nextToken+"!")
        if nextToken == string:
            self.advance()
        else:
            print("ERROR!! expected " + string+"got: "   + nextToken)
            exit()


    def Push(self, firstName):
        if firstName in self.symbolTable.current_scope:
            if self.symbolTable.kindOf(firstName) == "var":
                self.writer.writePush('local', self.symbolTable.indexOf(firstName))
            elif self.symbolTable.kindOf(firstName) == "arg":
                self.writer.writePush('argument', self.symbolTable.indexOf(firstName))
        
        else:
            if self.symbolTable.kindOf(firstName) == "static":
                self.writer.writePush('static', self.symbolTable.indexOf(firstName))
            else:
                self.writer.writePush('this', self.symbolTable.indexOf(firstName))


    def Pop(self, firstName):
        if firstName in self.symbolTable.current_scope:
            if self.symbolTable.kindOf(firstName) == "var":
                self.writer.writePop('local', self.symbolTable.indexOf(firstName))
            elif self.symbolTable.kindOf(firstName) == "arg":
                self.writer.writePop('argument', self.symbolTable.indexOf(firstName))

        else:
            if self.symbolTable.kindOf(firstName) == "static":
                self.writer.writePop('static', self.symbolTable.indexOf(firstName))
            else:
                self.writer.writePop('this', self.symbolTable.indexOf(firstName))

                
                
            












    #API BEGINS

    #compile parameter list

    def compileParameterList(self):
        print("parameterlist")
        #self.startNonTerm("parameterList")
        while self.existParameter():
            self.writeParameter()
        #self.endNonTerm()


#compile class variable declarations
    def compileClassVarDec(self):
        print("classvardec")
        #self.startNonTerm("classVarDec")
        kind =""
        if self.nextToken() == "static":
            kind = "static"
            self.eat("static")
        else:
            kind = "field"
            self.eat("field")

        typ = self.advance() #get varName type
        name = self.advance() #get varName
        self.symbolTable.define(name, typ, kind)

        #test for symbol table
        #self.sWrite(name)

        
        while self.nextToken() == ",":
            self.eat(",")
            name = self.advance() #get var Name
            self.symbolTable.define(name, typ, kind)
            
            #test for symbol table
            #self.sWrite(name)

        
        self.eat(";")

        #self.endNonTerm()

        
    
    #compiles class declaration
            
    def compileClass(self):
        print("class")
        #self.startNonTerm("class")
        self.eat("class") # get "class"
        self.className = self.advance() #get class name
        self.eat("{")
        while (self.existClassVarDec()):
            self.compileClassVarDec()

        while (self.existSubroutineDec()):
            self.compileSubroutineDec()

        self.eat("}")
        #self.endNonTerm()


   #compile variable declaration     
    def compileVarDec(self):
        print("vardec")
        #self.startNonTerm("varDec")
        self.eat("var")
        typ = str(self.advance()) #get var-type
        name = self.advance() #get varName
        self.symbolTable.define(name, typ, "var")
        
        #test for symbol table
        #self.sWrite(name)

        
        while (self.nextToken() == ","):
            self.eat(",")
            name = self.advance()
            self.symbolTable.define(name, typ, "var")
            
            #test for symbol table
            #self.sWrite(name)

        
        self.eat(";")
        #self.endNonTerm()

        
        
    #compile subroutine declaration
    def compileSubroutineDec(self):
        print("subroutine dec")
        #self.startNonTerm("subroutineDec")
        if self.nextToken() == "constructor" or self.nextToken() == "function" or self.nextToken() == "method":
            self.advance() # get constructor | method | function
        else:
            print("ERROR!!! keyword expected")
            return
        self.advance() # get type | void
        self.n = self.advance() # get subroutine name
        self.name = self.className+"."+self.n
        self.symbolTable.startSubroutine(self.name)
        self.symbolTable.setScope(self.name)
        self.eat("(")
        self.compileParameterList()
        self.eat(")")
        self.compileSubroutineBody()
        #self.endNonTerm()

    #compiles subroutine body

    def compileSubroutineBody(self):
        print("subroutine body")
        ##self.startNonTerm("subroutineBody")
        self.eat("{")
        while(self.existVarDec()):
            self.compileVarDec()
        
        self.compileStatements()
        self.eat("}")
        #self.endNonTerm()


    #

    
    #compile Statements
    def compileStatements(self):
        print("statements")
        #self.startNonTerm("statements")
        while self.existStatement():
            if self.nextToken() == "do":
                self.compileDo()
            elif self.nextToken() == "let":
                self.compileLet()
            elif self.nextToken() == "while":
                self.compileWhile()
            elif self.nextToken() == "if":
                self.compileIf()
            elif self.nextToken() == "return":
                self.compileReturn()
        #self.endNonTerm()    

    
    #compiles let statement
    
    def compileLet(self):
        print("let")
        self.startNonTerm('letStatement')
        self.eat("let") # get 'let' keyword
        self.advance() # get varName
        if self.nextToken() == '[':
            self.writeArrayIndex()
        self.eat("=") # get '=' symbol
        self.compileExpression()
        self.eat(";") # get ';' symbol
        self.endNonTerm()


    #compiles if statement
    def compileIf(self):
        print("if")
        self.startNonTerm('ifStatement')
        
        self.eat("if") # get 'if' keyword
        self.eat("(") # get '(' symbol
        self.compileExpression()
        self.eat(")") # get ')' symbol
        
        self.eat("{")

        self.compileStatements()
        self.eat("}")        

        if self.nextToken() == "else":
            self.eat("else")
            self.eat("{")

            self.compileStatements()
            self.eat("}")

        self.endNonTerm()


    # compiles while statement(loop)

    def compileWhile(self):
        print("while")
        self.startNonTerm("whileStatement")

        self.eat("while")
        self.eat("(")
        self.compileExpression()
        self.eat(")")
        self.eat("{")
        self.compileStatements()
        self.eat("}")

        self.endNonTerm()


    #compiles do statements (subroutine call  #completed ---
    def compileDo(self):
        print("do")
        firstName = lastName = doStatement = ''
        nLocals  = 0
        #self.startNonTerm("doStatement")
        self.eat("do")
        firstName = self.advance()#get subroutine/var/class name

        if self.nextToken() == ".":  #in case of className.subRoutineName
            self.eat(".")
            lastName = self.advance()#get subRoutineName
            if firstName in self.symbolTable.current_scope or firstName in self.symbolTable.local_scope:
                self.Push(firstName)
                fullName = self.symbolTable.typeOf(firstName)+"."+lastName;
                nLocals +=1
            else:
                fullName = firstName+"."+lastName

        else:
            self.writer.writePush('pointer', 0)
            nLocals += 1
            fullName = self.className +"."+firstName


        self.eat("(")
        nLocals += self.compileExpressionList()
        self.writer.writeCall(fullName, nLocals)
        self.eat(")")
        self.eat(";")
        #self.endNonTerm()


    #compiles return satement
    def compileReturn(self):
        print("return")
        #self.startNonTerm("returnStatement")

        self.eat("return")
        if self.nextToken() != ";":
            self.compileExpression()
        else: # if there return type is void
            self.writer.writePush("constant", 0)
        self.writer.writeReturn()
        self.eat(";")

        #self.endNonTerm()


    
    

        
    #compiles expression list
    def compileExpressionList(self):
        print("expression list")
        counter = 0
        #self.startNonTerm('expressionList')
        if self.existExpression():
            self.compileExpression()
            counter += 1
        while self.nextToken() == ",":
            self.eat(",") #get the symbol ","
            if self.existExpression():
                self.compileExpression()
                counter += 1
        return counter
        #self.endNonTerm()
        

    #compiles expressions
    def compileExpression(self):
        print("expression")
        #self.startNonTerm('expression')
        self.compileTerm()
        while (self.nextToken() in self.binaryOp):

            op = self.advance() # get the  binary op
            self.compileTerm()
            if op == "+":
                self.writer.writeArithmetic("add")

            elif op == "-":
                self.writer.writeArithmetic("sub")

            elif op == "=":
                self.writer.writeArithmetic("eq")

            elif op == ">":
                self.writer.writeArithmetic("gt")

            elif op == "<":
                self.writer.writeArithmetic("lt")

            elif op == "&":
                self.writer.writeArithmetic("and")

            elif op == "|":
                self.writer.writeArithmetic("or")


            elif op == "*":
                self.writer.writeCall("Math.multiply", 2)

            elif op == "/":
                self.writer.writeCall("Math.divide", 2)


        #self.endNonTerm()

    # compile subRoutine calls
    def compileSubroutinecall(self):
        print("subroutinecall")
        self.startNonTerm("subroutineCall")
        self.advance() # get subroutine name  |  class name
        if self.nextToken() == ".": # if the above token is a class name
            self.eat(".")
            self.advance() # get subroutine name
        self.eat("(")
        self.compileExpressionList()
        self.eat(")")

        self.endNonTerm()

        
    #compiles term

    def compileTerm(self):  
        print("term")
        #Grammar : varname | constant
        #self.startNonTerm("term")# to start the new non terminal block
    
        #print("compiling term"+self.nextValue())
        if self.nextValue() == "integerConstant" or self.nextValue() == "stringConstant" or (self.nextToken() in self.keywordConsts):
            self.advance() # to get the const
        elif self.nextValue() == "identifier":
            self.advance() # get varName or ClassName
            
            if self.nextToken() == "[":
                self.writeArrayIndex()

            if self.nextToken() == "(":
                self.eat("(") # get "("
                self.compileExpressionList()
                self.eat(")") # get ")"

            if self.nextToken() == ".": # handles with subroutine call
                self.eat(".") # get "."
                self.advance() # get subRoutine name
                self.eat("(") # get "("
                self.compileExpressionList()
                self.eat(")") # get ")"

        elif (self.nextToken() in self.unaryOp):
            self.advance()# get op
            self.compileTerm()

        elif self.nextToken() == "(":
            self.eat("(") # get "("
            self.compileExpression()
            self.eat(")") # get ")"

        #self.endNonTerm()

    
        



    
        
        











        
        
def main(): 
    
    inFile = sys.argv[1]
    

    def Parser(inputFile):
        source = inputFile
        out_file = open(inputFile[:-5] + ".vm","w+")
        cwrite = compilationEngine(source, out_file)
        cwrite.compileClass()
        
        out_file.close()

        
    #If the  given argument is a file.
        
    if os.path.isfile(inFile):
        Parser(inFile)



    elif os.path.isdir(inFile):
        path = "./"+inFile+"/*.jack"
        files = glob.glob(path)
        for name in files:
            try:
                Parser(name)

            
            except IOError as e:
                if e.errno != errno.EISDIR:
                    raise

    

              
if __name__ == "__main__":
    main()
