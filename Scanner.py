from Token import Token
from TokenType import TokenType

KEYWORDS={
    "and": "AND",
    "class": "CLASS",
    "else": "ELSE",
    "false": "FALSE",
    "for": "FOR",
    "fun": "FUN",
    "if": "IF",
    "nil": "NIL",
    "or": "OR",
    "print": "PRINT",
    "return": "RETURN",
    "super": "SUPER",
    "this": "THIS",
    "true": "TRUE",
    "var": "VAR",
    "while": "WHILE"
}

class Scanner :

    def __init__ (self,source:str,lox):
        self.source:str=source
        self.tokens=[]
        self.start:int=0
        self.current:int=0
        self.line:int=1
        self.lox=lox
        self.Keywords={
         "and":self.get_token_type("AND"),
         "class":self.get_token_type("CLASS"),
         "else":self.get_token_type("ELSE"),
         "false":self.get_token_type("FALSE"),
         "for":self.get_token_type("FOR"),
         "fun":self.get_token_type("FUN"),
         "if":self.get_token_type("IF"),
         "nil":self.get_token_type("NIL"),
         "or":self.get_token_type("OR"),
         "print":self.get_token_type("PRINT"),
         "return":self.get_token_type("RETURN"),
         "super":self.get_token_type("SUPER"),
         "this":self.get_token_type("THIS"),
         "true":self.get_token_type("TRUE"),
         "var":self.get_token_type("VAR"),
         "while":self.get_token_type("WHILE")
        }

    def isAtEnd(self)->bool:
        return self.current>=len(self.source)

    def get_token_type(self,name:str):
        token_type=getattr(TokenType,name,None)
        if token_type is not None:
            return token_type
        else:
            raise ValueError(f"{name} is not valid token type {self.line}")

    # def get_token_type_identifier(self,name:str):
    #     newName=KEYWORDS.get(name,"DBOSS")
    #     # print("new u : ",newName,type(name),type(newName))
    #     token_type = getattr(TokenType, name,"IDENTIFIER")
    #     print(token_type, " : hu ",name,newName)
    #     if token_type is not TokenType.IDENTIFIER:
    #         return token_type
    #     else:
    #         return TokenType.IDENTIFIER
    def get_token_type_identifier(self, name: str):
        newName = KEYWORDS.get(name, "IDENTIFIER")  # Default to "IDENTIFIER" if not found
        token_type = getattr(TokenType, newName, TokenType.IDENTIFIER)  # Use newName here
        return token_type


    def advance(self):
        self.current+=1
        return self.source[self.current-1]

    def match(self,expected):
        if self.isAtEnd():
            return False
        if self.source[self.current] != expected:
            return False
        self.current+=1
        return True


    def addToken_s(self,type:str):
        if isinstance(type,str):
            token_type = self.get_token_type(type)
            self.addToken_b(token_type, None)
        elif isinstance(type,TokenType):
            self.addToken_b(type, None)

    def addToken_b(self,type:TokenType,literal):
        text=self.source[self.start:self.current]
        x=Token(type,text,literal,self.line)
        self.tokens.append(x)

    def peek(self):
        if(self.isAtEnd()):
            return "\0"
        return self.source[self.current]

    def handleString(self):
        while(1):
            a = self.peek() != '"'
            b = not self.isAtEnd()
            if a and b:
                if self.peek()=="\n":
                    self.line += 1
                self.advance()
            else:
                break
        if self.isAtEnd():
            self.lox.error(self.line,"Unterminated string")
            return
        self.advance()
        str_value=self.source[self.start+1:self.current-1]
        self.addToken_b(TokenType.STRING,str_value)
        return

    def isDigit(self,c:str):
        return c>="0" and c<="9"

    def peekNext(self):
        if self.current+1>=len(self.source):
            return "\0"
        return self.source[self.current+1]

    def handleNumber(self):
        while(1):
            a=self.isDigit(self.peek())
            if not a:
                break
            self.advance()

        if self.peek()=="." and self.isDigit(self.peekNext()):
            self.advance()

        while(1):
            a = self.isDigit(self.peek())
            if not a:
                break
            self.advance()

        a_number=float(self.source[self.start:self.current])
        token_type=self.get_token_type("NUMBER")
        self.addToken_b(token_type,a_number)
        return

    def ide(self):
        print("**************************")
    def isAlpha(self,c:str):
        return (c>='a' and c<='z') or (c>="A" and c<="Z") or (c=="_")

    def isAlphaNumeric(self,c:str):
        return self.isAlpha(c) or self.isDigit(c)

    def handleIdentifier(self):
        while(1):
            a=self.isAlphaNumeric(self.peek())
            if not a:
                break
            self.advance()

        text=self.source[self.start:self.current]
        token_type=self.get_token_type_identifier(text)
        self.addToken_s(token_type)


    def scanToken(self):
        c=self.advance()
        if c=='(':
            self.addToken_s("LEFT_PAREN")
        elif c==")":
            self.addToken_s("RIGHT_PAREN")
        elif c=="{":
            self.addToken_s("LEFT_BRACE")
        elif c=="}":
            self.addToken_s("RIGHT_BRACE")
        elif c==",":
            self.addToken_s("COMMA")
        elif c==".":
            self.addToken_s("DOT")
        elif c=="-":
            self.addToken_s("MINUS")
        elif c=="+":
            self.addToken_s("PLUS")
        elif c==";":
            self.addToken_s("SEMICOLON")
        elif c=="*":
            self.addToken_s("STAR")

        elif c == "!":

            if self.match("="):
                self.addToken_s("BANG_EQUAL")
            else:

                self.addToken_s("BANG")
        elif c == "=":
            if self.match("="):
                self.addToken_s("EQUAL_EQUAL")
            else:
                self.addToken_s("EQUAL")
        elif c == "<":
            if self.match("="):
                self.addToken_s("LESS_EQUAL")
            else:
                self.addToken_s("LESS")
        elif c == ">":
            if self.match("="):
                self.addToken_s("GREATER_EQUAL")
            else:
                self.addToken_s("GREATER")
        elif c=="/":
            if self.match("/"):
                while(1):
                    one=self.peek()!="\n"
                    two=not self.isAtEnd()
                    if one and two:
                        self.advance()
                    else:
                        break
            elif self.match("*"):
                while(1):
                    if self.peek()=="*" and self.peekNext()=="/":
                        self.advance()
                        self.advance()
                        break
                    elif self.isAtEnd():
                        self.lox.error(self.line,"unterminated multi-line comment")
                        return
                    else:
                        if self.peek()=="\n":
                            self.line+=1
                        self.advance()


            else:
                self.addToken_s("SLASH")
        elif c==" ":
            pass
        elif c=="\r":
            pass
        elif c=="\t":
            while False:
                print("Will do nothing, Haha!!")
        elif c=="\n":
            self.line+=1
            pass
        elif c=='"':
            self.handleString()
        else:
            if self.isDigit(c):
                self.handleNumber()
            elif self.isAlpha(c):
                self.handleIdentifier()
            else:
                self.lox.error(self.line,f"Unexpected character  {c}.")
    def scanTokens(self):
        while not self.isAtEnd():
            self.start=self.current
            self.scanToken()

        EOF_type=self.get_token_type("EOF")
        self.tokens.append(Token(EOF_type,"","",self.line))
        return self.tokens





