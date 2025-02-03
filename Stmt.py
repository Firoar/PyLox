from abc import ABC, abstractmethod
from Token import Token
from Expr import Expr


class Stmt(ABC):
    @abstractmethod
    def accept(self,visitor):
        pass

    class Visitor:
        @abstractmethod
        def visit_expression_stmt(self,expr: 'Expression'):
            pass

        @abstractmethod
        def visit_print_stmt(self,expr: 'Print'):
            pass

        @abstractmethod
        def visit_var_stmt(self,expr: 'Var'):
            pass

        @abstractmethod
        def visit_block_stmt(self,expr: 'Block'):
            pass



class Expression(Stmt): 
    def __init__(self,expression:'Expr'): 
        self.expression = expression

    def accept(self,visitor):
        return visitor.visit_expression_stmt(self)


class Print(Stmt): 
    def __init__(self,expression:'Expr'): 
        self.expression = expression

    def accept(self,visitor):
        return visitor.visit_print_stmt(self)


class Var(Stmt): 
    def __init__(self,name:'Token',intializer:'Expr'): 
        self.name = name
        self.intializer = intializer

    def accept(self,visitor):
        return visitor.visit_var_stmt(self)


class Block(Stmt): 
    def __init__(self,statements:'list'): 
        self.statements = statements

    def accept(self,visitor):
        return visitor.visit_block_stmt(self)


