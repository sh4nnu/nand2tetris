
""" SYMBOL  TABLE"""
class SymbolTable:
    def __init__(self):

        self.global_scope = {}
        self.local_scope = {}
        self.current_scope = self.global_scope
        self.arg_counter =  0
        self.var_counter = 0
        self.static_counter = 0
        self.field_counter = 0
        self.if_counter = 0
        self.while_counter = 0

    def startSubroutine(self, name):
        """ resets the local symbol table"""
        self.local_scope[name] = {}
        self.arg_counter = 0
        self.var_counter = 0
        self.if_counter = 0
        self.while_counter = 0
        

    def define(self, name, type, kind):
        """defines (or) adds new entry to the symbol table field and static have class
            level scope while var, arg have subRoutine level scope."""
        if( kind == "field"):
            self.global_scope[name] = (type, kind, self.field_counter)

            self.field_counter += 1

        elif (kind == "static"):
            self.global_scope[name] = (type, kind, self.static_counter)
            self.static_counter += 1

        elif (kind == "var"):
            self.current_scope[name] = (type, kind, self.var_counter)
            self.var_counter += 1

        elif (kind == "arg"):
            self.current_scope[name] = (type, kind, self.arg_counter)
            self.arg_counter +=1
        
            
        
        

    def varCount(self, kind):
        #prints the number of variables defined in the current scope
        
        return len([v for (k,v) in self.current_scope.items() if (v[1] == kind)])

    def globalCount(self, kind):
        return len([v for (k,v) in self.global_scope.items() if (v[1] == kind)])

    def kindOf(self, name):
        """If the given variable is found in local scope it returns its kind,
        if it is found in gobal scope it returns its respective kind else
        returns NONE"""
        
        if name in self.current_scope:
            
            return self.current_scope[name][1]
        elif name in self.global_scope:
            return self.global_scope[name][1]

        else:
            return "NONE" 

    def  typeOf(self, name):
        if name in self.current_scope:
            return self.current_scope[name][0]
        elif name in self.global_scope:
            return self.global_scope[name][0]

        else:
            return "NONE"

    def indexOf(self, name):
        if name in self.current_scope:
            return self.current_scope[name][2]
        elif name in self.global_scope:
            return self.global_scope[name][2]

        else:
            return "NONE"


        
    def setScope(self, name):
        if (name == "global"):
            self.current_scope = self.global_scope
        else:
            self.current_scope = self.local_scope[name]


def main():
    st = SymbolTable()
    st.define("manikishan", "int" , "field")
    print(st.kindOf("manikishan"))
    

if __name__ == "__main__":
    main()

