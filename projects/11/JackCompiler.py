
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
        self.function_type= ""
        self.is_unary = False

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
        count = 0
        #self.startNonTerm("parameterList")
        if self.function_type == "method":
            self.symbolTable.define("this","self","arg")
        while self.existParameter():
            self.writeParameter()
            count += 1
        #self.endNonTerm()

        return count

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
        self.writer.close()

   #compile variable declaration --completed
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



    #compile subroutine declaration --completed
    def compileSubroutineDec(self):
        print("subroutine dec")
        #self.startNonTerm("subroutineDec")
        if self.nextToken() == "constructor" or self.nextToken() == "function" or self.nextToken() == "method":
            self.function_type =    self.advance() # get constructor | method | function
        else:
            print("ERROR!!! keyword expected")
            return
        self.advance() # get type | void
        self.n = self.advance() # get subroutine name
        self.name = self.className+"."+self.n
        self.symbolTable.startSubroutine(self.name)
        self.symbolTable.setScope(self.name)
        self.eat("(")
        nArgs =self.compileParameterList()
        self.eat(")")
        self.compileSubroutineBody()
        #self.endNonTerm()

    #compiles subroutine body  --completed

    def compileSubroutineBody(self):
        print("subroutine body")
        ##self.startNonTerm("subroutineBody")
        self.eat("{")
        while(self.existVarDec()):
            self.compileVarDec()

        nLocals = self.symbolTable.varCount("var")
        self.writer.writeFunction(self.name,nLocals)
        #if subroutine is a method or constructor


        # for allocating space, handling both method and constructor

        if self.function_type == "method":
            #arg 0 is this.(of the method) , poping the method to THIS pointer
            self.writer.writePush("argument", 0)
            self.writer.writePop("pointer", 0)

        elif self.function_type == "constructor":
            nGlobals = self.symbolTable.globalCount("field")
            self.writer.writePush("constant", nGlobals)
            self.writer.writeCall("Memory.alloc", 1)
            self.writer.writePop("pointer", 0)

        self.compileStatements()
        self.eat("}")
        #self.endNonTerm()
        self.symbolTable.setScope("global")






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


    #compiles let statement   --completed

    def compileLet(self):
        print("let")
        #self.startNonTerm('letStatement')
        self.eat("let") # get 'let' keyword
        arr_name =self.advance() # get varName
        isArray = False
        if self.nextToken() == '[':
            isArray =True
            self.compileArrayIndex(arr_name)

        self.eat("=") # get '=' symbol

        self.compileExpression()


        if isArray:
            self.writer.writePop("temp", 0)
            self.writer.writePop("pointer",1)
            self.writer.writePush("temp",0)
            self.writer.writePop("that", 0)

        else:
            self.Pop(arr_name)
        self.eat(";") # get ';' symbol
        #self.endNonTerm()


    #compiles if statement --completed
    def compileIf(self):
        print("if")
        #self.startNonTerm('ifStatement')
        curr_if_counter = self.symbolTable.if_counter
        self.symbolTable.if_counter += 1
        self.eat("if") # get 'if' keyword
        self.eat("(") # get '(' symbol
        self.compileExpression()
        self.eat(")") # get ')' symbol
        #self.writer.writeArithmetic("not")
        self.writer.writeIf("IF_LABEL"+ str(curr_if_counter))
        self.writer.writeGoto("IF_FALSE" + str(curr_if_counter))
        self.writer.writeLabel("IF_LABEL" + str(curr_if_counter))
        self.eat("{")

        self.compileStatements()

        self.eat("}")

        if self.nextToken() == "else":
            self.eat("else")
            self.eat("{")
            self.writer.writeGoto("IF_END"+str(curr_if_counter))
            self.writer.writeLabel("IF_FALSE" + str(curr_if_counter))
            self.compileStatements()
            self.eat("}")
            self.writer.writeLabel("IF_END"+str(curr_if_counter))

        else:
            self.writer.writeLabel("IF_FALSE"+str(curr_if_counter))


        #self.endNonTerm()


    # compiles while statement(loop) --completed

    def compileWhile(self):
        print("while")
        #self.startNonTerm("whileStatement")
        curr_while_counter = self.symbolTable.while_counter
        self.symbolTable.while_counter += 1
        self.eat("while")
        self.eat("(")
        self.writer.writeLabel("WHILE_LABEL"+str(curr_while_counter))
        self.compileExpression()
        self.eat(")")
        self.writer.writeArithmetic("not")
        self.writer.writeIf("WHILE_END"+ str(curr_while_counter))
        self.eat("{")
        self.compileStatements()
        self.eat("}")
        self.writer.writeGoto("WHILE_LABEL"+str(curr_while_counter))
        self.writer.writeLabel("WHILE_END"+str(curr_while_counter))
        #self.endNonTerm()


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
            if firstName in self.symbolTable.current_scope or firstName in self.symbolTable.global_scope:
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
        self.writer.writePop("temp",0)
        self.eat(")")
        self.eat(";")
        #self.endNonTerm()


    #compiles return satement --completed
    def compileReturn(self):
        print("return")
        #self.startNonTerm("returnStatement")

        self.eat("return")
        if self.nextToken() != ";":
            self.compileExpression()
        else: # if there return type is void
            #self.writer.writePop("temp",0)
            self.writer.writePush("constant", 0)
        self.writer.writeReturn()
        self.eat(";")

        #self.endNonTerm()






    #compiles expression list --completed
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


    #compiles expressions --completed
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

            elif op == "&gt;":
                self.writer.writeArithmetic("gt")

            elif op == "&lt;":
                self.writer.writeArithmetic("lt")

            elif op == "&amp;":
                self.writer.writeArithmetic("and")

            elif op == "|":
                self.writer.writeArithmetic("or")

            elif op == "*":
                self.writer.writeCall("Math.multiply", 2)

            elif op == "/":
                self.writer.writeCall("Math.divide", 2)


        #self.endNonTerm()

    # compile subRoutine calls  --completed
    def compileSubroutinecall(self):
        print("subroutinecall")
        first_name = last_name = full_name = ""
        nArgs =0
        #self.startNonTerm("subroutineCall")
        first_name = self.advance() # get subroutine name  |  class | var name
        if self.nextToken() == ".": # if the above token is a class name
            self.eat(".")
            last_name = self.advance() # get subroutine name

            if first_name in self.symbolTable.local_scope or first_name in self.symbolTable.global_scope:
                self.Push(first_name)
                full_name = self.symbolTable.typeOf(first_name) + last_name #while using a method of an object
                nArgs += 1

            else:
                full_name = first_name+ last_name       # if the subroutine called is from a class

        else:
            self.writer.writePush("pointer", 0) #when the subroutine called is a method
            nArgs += 1

            full_name = self.className + first_name





        self.eat("(")
        nArgs += self.compileExpressionList()
        self.writer.writeCall(full_name,nArgs)
        self.eat(")")

        #self.endNonTerm()

    #compiles array index

    def compileArrayIndex(self, name):
        self.writeArrayIndex()
        if name in self.symbolTable.current_scope:
            if self.symbolTable.kindOf(name) == 'var':
                self.writer.writePush('local', self.symbolTable.indexOf(name))
            elif self.symbolTable.kindOf(name) == 'arg':
                self.writer.writePush('argument', self.symbolTable.indexOf(name))
        else:
            if self.symbolTable.kindOf(name) == 'static':
                self.writer.writePush('static', self.symbolTable.indexOf(name))
            else:
                self.writer.writePush('this', self.symbolTable.indexOf(name))
        self.writer.writeArithmetic('add')

    #compiles term  --completed

    def compileTerm(self):
        print("term")
        #Grammar : varname | constant
        #self.startNonTerm("term")# to start the new non terminal block

        #print("compiling term"+self.nextValue())

        isArray  = False
        if self.nextValue() == "integerConstant":
            const = self.advance() # to get the const
            self.writer.writePush("constant", const)

        elif self.nextValue() == "stringConstant":
            str_value = self.advance()
            self.writer.writePush("constant", len(str_value))
            self.writer.writeCall("String.new", 1)

            for s in str_value:
                self.writer.writePush("constant", ord(s))
                self.writer.writeCall("String.appendChar", 2)


        elif (self.nextToken() in self.keywordConsts):
            #handling keywords like "true" "false" "null" "this"
            keyword = self.advance()

            if keyword == "true":
                self.writer.writePush("constant", 0)
                self.writer.writeArithmetic("not")

            elif keyword == "false" or keyword == "null":
                self.writer.writePush("constant", 0)

            elif keyword == "this":
                self.writer.writePush("pointer", 0)


        elif self.nextValue() == "identifier":
            nArgs=0
            identif = self.advance()  # get varName or ClassName

            if self.nextToken() == "[":
                isArray = True
                self.compileArrayIndex(identif)

            if self.nextToken() == "(":
                nArgs+=1
                self.writer.writePush("pointer", 0)
                self.eat("(") # get "("
                nArgs += self.compileExpressionList()
                self.eat(")") # get ")"
                self.writer.writeCall(self.className+"."+identif, nArgs)

            elif self.nextToken() == ".": # handles with subroutine call
                self.eat(".") # get "."
                sub_name = self.advance() # get subRoutine name
                if identif in self.symbolTable.current_scope or identif in self.symbolTable.global_scope:
                    self.Push(identif)
                    name = self.symbolTable.typeOf(identif)+"."+ sub_name
                    nArgs+=1

                else:
                    name = identif + "."+ sub_name
                self.eat("(") # get "("
                nArgs+=self.compileExpressionList()
                self.eat(")") # get ")"
                self.writer.writeCall(name, nArgs)

            else:
                if isArray:
                    self.writer.writePop("pointer", 1)
                    self.writer.writePush("that", 0)

                elif identif in self.symbolTable.current_scope:
                    if self.symbolTable.kindOf(identif) == "var":
                        self.writer.writePush("local",self.symbolTable.indexOf(identif))

                    elif self.symbolTable.kindOf(identif) == "arg":
                        self.writer.writePush("argument",self.symbolTable.indexOf(identif))

                else:
                    if self.symbolTable.kindOf(identif) == "static":
                        self.writer.writePush("static", self.symbolTable.indexOf(identif))

                    else:
                        self.writer.writePush("this", self.symbolTable.indexOf(identif))


        elif (self.nextToken() in self.unaryOp):
            Uop = self.advance()# get op


            self.compileTerm()
            if (Uop == "-"):
                self.writer.writeArithmetic("neg")

            elif (Uop == "~"):
                self.writer.writeArithmetic("not")

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
