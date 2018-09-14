
#!/usr/bin/python

import os,sys,glob,errno,shlex,re
import xml.etree.ElementTree as xml
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
        self.cursorAtEnd = False
        self.removeComments(self.tokens)
        self.tokenize(self.tokens)


        
    def hasMoreTokens(self):
        currentPosition = self.infile.tell()
        self.advance()
        self.infile.seek(currentPosition)
        return not self.cursorAtEnd


    def advance(self):
        if len(self.tokens) != 0:
            self.token =self.tokens[0]                
            print("token: " + str(self.token)+" type: " + self.tokenType())
            print( self.token)
            
            self.tokens = self.tokens[1:]
            
        else:
              
            self.cursorAtEnd = True
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

    def nextType(self):
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

    self.keywordConsts = {'true', 'false','null','this'}
    self.binaryOp = {'+','-','*','|','<','>','='}
    self.unaryOp = {'-','~'}


    
    def __init__(self, infile, outfile):
        self.tokenizer = JackTokenizer(infile)
        self.op = outfile
        self.indent = ""
        self.mStack =[] #a stack to store all non terminal blocks opened which have to be closed
    def addIndent(self):
        self.indent +="   "

    def removeIndent(self):
        self.indent = self.indent[:-4]
    

    def writeTerm(self, token, Ttype):
        self.op.write(self.indent+"<"+Ttype+">"+ token + "</"+Ttype+">\n")


    def startNonTerm(self, rule):
        self.op.write(self."<"+rule+">\n")
        self.addIndent()
        self.mStack.append(rule)


    def endNonTerm(self):
        rule = self.mStack.pop()
        self.removeIndent()
        self.op.write(self.indent+"</"+rule+">\n")
        
    
    def advance(self):
        token = self.tokenizer.advance()
        Ttype = self.tokenizer.tokenType()
        self.writeTerm(token, Ttype)

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
            


    def  eat(string):   # check for expected elements in the grammar
        if self.nextToken == string:
            self.advance()
        else:
            print("ERROR!! expected " + string)

    #API BEGINS

    #compiles let statement
    
    def compileLet(self):
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
        self.startNonTerm("whileStatement")

        self.eat("while")
        self.eat("(")
        self.compileExpression()
        self.eat(")")
        self.eat("{")
        self.compileStatements()
        self.eat("}")

        self.endNonTerm()


    #compiles do statements (subroutine call
    def compileDo(self):
        
    

        
    #compiles expression list
    def compileExpressionList(self):
        self.startNonTerm('expressionList')
        if self.existExpression():
            self.compileexpression()
        while self.nextToken() == ",":
            self.eat(",") #get the symbol ","
            if self.existExpression():
                self.compileExpression()
        
        self.endNonTerm()
        

    #compiles expressions
    def compileExpression(self):
        self.startNonTerm('expression')
        self.compileTerm()
        while (self.nextToken() in binaryOp):
            self.advance() # get the  binary op
            self.compileTerm()

        self.endNonTerm()

    #compiles term

    def compileTerm(self):
        #Grammar : varname | constant
        self.startNonTerm("term")# to start the new non terminal block

        
        if self.nextValue() == "integerConstant" or self.nextValue() == "stringConstant" or (self.nextValue() in self.keywordConsts):
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

        elif self.nextToken == "(":
            self.eat("(") # get "("
            self.compileExpressionList()
            self.eat(")") # get ")"

        self.endNonTerm()

    
        



    
        
        











        
        
def main(): 
    
    inFile = sys.argv[1]
    #If the  given argument is a file.

    def indent(elem, level=0):
         
         i = "\n" + level*"  "
         if len(elem):
           if not elem.text or not elem.text.strip():
             elem.text = i + "  "
           if not elem.tail or not elem.tail.strip():
             elem.tail = i
           for elem in elem:
             indent(elem, level+1)
           if not elem.tail or not elem.tail.strip():
             elem.tail = i
         else:
           if level and (not elem.tail or not elem.tail.strip()):
             elem.tail = i

    def Parser(inputFile):
        source = inputFile
        out_file = open(inputFile[:-5] + "_Tokenizertest.xml","wb")
        tokenizer = jackTokenizer(source)
        #writing tokenizer test file
        
        xml_out = xml.Element("tokens")
        while tokenizer.hasMoreTokens():
            
            tok_type = tokenizer.tokenType()
            xml_line = xml.SubElement(xml_out,tok_type)
            #alter string constant
            if tokenizer.token[0] == '"':
                xml_line.text = tokenizer.token[1:-1]
            else:
                xml_line.text = tokenizer.token
            
        indent(xml_out)
        tr = xml.ElementTree(xml_out)
        
        tr.write(out_file)

        out_file.close()

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
