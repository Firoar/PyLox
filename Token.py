from TokenType import  TokenType
class Token:
    def __init__(self,tokentype:TokenType,lexeme,literal:str,line:int):
        self.type=tokentype
        self.lexeme=lexeme
        self.literal=literal
        self.line=line

    def __str__(self):
        return f"{self.type} {self.lexeme} {self.literal}"

