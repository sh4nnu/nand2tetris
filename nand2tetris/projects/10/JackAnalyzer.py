
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
