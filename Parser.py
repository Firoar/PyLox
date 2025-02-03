from Expr import Assign, Binary, Expr, Grouping, Literal, Unary, Variable
from TokenType import TokenType
from Stmt import Block, Expression, Print, Stmt, Var



class Parser:
    
    class ParseError(RuntimeError):
        pass
    
    def __init__(self,tokens: list,error_handler):
        self.tokens=tokens
        self.current=0
        self.error_handler=error_handler
    
    def parse(self):
        jod=[]
        try:
            while not self.isAtEnd():
                jod.append(self.declaration())

            return jod
        except self.ParseError as error:
            return None    
    
    def declaration(self):
        try:
            if self.match(TokenType.VAR):
                return self.varDeclaration()    
            return self.statement()
        except self.ParseError as error:
            self.synchronize()
            return None
            
    def expression(self)->Expr:
        return self.assignment() 
    def assignment(self):
        expr=self.equality()
        
        if self.match(TokenType.EQUAL):
            equals=self.previous()
            value=self.assignment()
            
            if isinstance(expr,Variable):
                name=expr.name
                return Assign(name,value)
            self.error(equals,"Invalid assignment operator")
        return expr    
    
    def statement(self)->Stmt:
        if self.match(TokenType.PRINT):
            return self.printStatement() 
        if self.match(TokenType.LEFT_BRACE):
            return Block(self.block())
        return self.expressionStatement()
    
    def varDeclaration(self):
        name=self.consume(TokenType.IDENTIFIER,"Expect variable name")
        
        intializer=None
        if self.match(TokenType.EQUAL):
            intializer=self.expression()
        self.consume(TokenType.SEMICOLON,"Except ';' after variable declaration")    
        return Var(name,intializer)
            
    
    def printStatement(self):
        value=self.expression()
        self.consume(TokenType.SEMICOLON, "Except ';' after value.")
        return Print(value)
    
    def block(self):
        statements=list()
        while (not self.check(TokenType.RIGHT_BRACE)) and (not self.isAtEnd()):
            statements.append(self.declaration())
        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block")    
        return statements
    
    def expressionStatement(self):
        expr=self.expression()
        self.consume(TokenType.SEMICOLON, "Except ';' after value.")
        return Expression(expr)

    
    def equality(self)->Expr:
        expr=self.comparison()
        
        while self.match(TokenType.BANG_EQUAL,TokenType.EQUAL_EQUAL):
            operator=self.previous()
            right=self.comparison()
            expr =Binary(expr,operator,right)
        return expr
    
    def comparison(self):
        expr=self.term()
        
        while self.match(TokenType.GREATER,TokenType.GREATER_EQUAL,TokenType.LESS,TokenType.LESS_EQUAL):
            operator=self.previous()
            right=self.term()
            expr=Binary(expr,operator,right)
        return expr    
    
    def term(self):
        expr=self.factor()
        
        while self.match(TokenType.PLUS,TokenType.MINUS):
            operator=self.previous()
            right=self.factor()
            expr=Binary(expr,operator,right)
        return expr
    
    def factor(self):
        expr=self.unary()    
        
        while self.match(TokenType.SLASH,TokenType.STAR):
            operator=self.previous()
            right=self.unary()
            expr=Binary(expr,operator,right)
        return expr
    
    def unary(self):
        if self.match(TokenType.BANG,TokenType.MINUS):
            operator=self.previous()    
            right=self.unary()
            return Unary(operator,right)
        return self.primary()
    
    def primary(self):
        if self.match(TokenType.FALSE):
            return Literal(False)
        if self.match(TokenType.TRUE):
            return Literal(True)
        if self.match(TokenType.NIL):
            return Literal(None)
        if self.match(TokenType.NUMBER,TokenType.STRING):
            return Literal(self.previous().literal)
        if self.match(TokenType.IDENTIFIER):
            return Variable(self.previous())
        if self.match(TokenType.LEFT_PAREN):
            expr=self.expression()
            self.consume(TokenType.RIGHT_PAREN,"Expect ')' after expression")
            return Grouping(expr)
        
        self.error(self.peek(),"Expect expression")
    
    def match(self,*types)->bool:
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False
    def check(self,type)->bool:
        if self.isAtEnd():
            return False
        # jod=self.peek()
        # print(f"{jod.type} == {type} => {jod.type==type} {jod==type} {jod}")
        return self.peek().type==type
    def advance(self):
        if not self.isAtEnd():
            self.current+=1
        return self.previous()    
    def isAtEnd(self):
        return self.peek().type==TokenType.EOF 
    def peek(self):
        
        print(f"Type => {self.tokens[self.current]}")
        return self.tokens[self.current]
    def previous(self):
        return self.tokens[self.current-1]
    
    def error(self,token,message):
        self.error_handler(token,message)
        raise self.ParseError()
    
    def consume(self,type,message):
        if self.check(type):
            return self.advance()
        self.error(self.peek(),message=message) ####
        
    
    def synchronize(self):
        self.advance()    
        
        while not self.isAtEnd():
            if self.previous().type==TokenType.SEMICOLON:
                return
            
            type=self.peek().type
            
            if type==TokenType.CLASS:
                pass
            elif type==TokenType.FUN:
                pass
            elif type==TokenType.VAR:
                pass
            elif type==TokenType.FOR:
                pass
            elif type==TokenType.IF:
                pass
            elif type==TokenType.WHILE:
                pass
            elif type==TokenType.PRINT:
                pass
            elif type==TokenType.RETURN:
                return
            
            self.advance()
            
                
            
            
        
        
                