from RuntimeError import MyRuntimeError

class Environment:
    def __init__(self,enclosing=None):
        self.values=dict()
        self.enclosing=enclosing
    
    def define(self,name,value):
        self.values[name]=value
        
    def get(self,name):    

        if name.lexeme in self.values:
            return self.values.get(name.lexeme)
        if self.enclosing is not None:
            return self.enclosing.get(name)
        raise MyRuntimeError(name,f"Undefined variable '{name.lexeme}'.")
    
    def assign(self,name,value):
        
        if self.values.get(name.lexeme) is not None:
            self.values[name.lexeme] =value
            return
        if self.enclosing is not None:
            self.enclosing.assign(name,value)
            return
        raise MyRuntimeError(name,f"Undefined variable '{name.lexeme}'.")    
    
        
            
    