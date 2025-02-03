from Expr import Expr, Grouping, Literal
from Token import TokenType
import operator
from RuntimeError import MyRuntimeError
from Stmt import Stmt
from Environment import Environment




class Interpreter(Expr.Visitor,Stmt.Visitor):
    
    def __init__(self,lox):
        self.lox=lox
        self.environment=Environment()
        
    
    def visit_literal_expr(self, expr:Literal):
        return expr.value
    def visit_grouping_expr(self, expr:Grouping):
        return self.evaluate(expr.expression)
    def visit_unary_expr(self, expr):
        right=self.evaluate(expr.right)
        
        operator_type=expr.operator.type
        
        if operator_type==TokenType.MINUS:
            self.checkNumberOperand(expr.operator,right)
            return -float(right)
        elif operator_type==TokenType.BANG:
            return not self.isTruthy(right)
        
        return None
    def visit_binary_expr(self, expr):
        left=self.evaluate(expr.left)
        right=self.evaluate(expr.right)
        
        operator_type=expr.operator.type
        
        if operator_type==TokenType.MINUS:
            self.checkNumberOperand(expr.operator,left,right)
            return float(left)-float(right)
        elif operator_type==TokenType.SLASH:
            if right==0.0:
                return None
            try:
                return float(left)/float(right)
            except TypeError:
                raise MyRuntimeError(expr.operator,"Operands must be numbers for division")
        elif operator_type==TokenType.STAR:
            self.checkNumberOperand(expr.operator,left,right)
            return float(left)*float(right)
        elif operator_type==TokenType.PLUS:
            if isinstance(left,float) and isinstance(right,float):
                return float(left)+float(right)
            elif isinstance(left,str) and isinstance(right,str):
                return f"{left}{right}"
            else:
                #TODO - fixing "36"+4==364 and not 36.04
                if type(left) is str and isinstance(right,(int, float)):
                    return left+str(right)
                elif type(right) is str and isinstance(left,(int,float)):
                    return str(left)+right
                
                
        elif operator_type==TokenType.GREATER:
            self.checkNumberOperand(expr.operator,left,right)
            return operator.gt(float(left),float(right))    
        elif operator_type==TokenType.GREATER_EQUAL:
            self.checkNumberOperand(expr.operator,left,right)
            return operator.ge(float(left),float(right))
        elif operator_type==TokenType.LESS:
            self.checkNumberOperand(expr.operator,left,right)
            return operator.lt(float(left),float(right))
        elif operator_type==TokenType.LESS_EQUAL:
            self.checkNumberOperand(expr.operator,left,right)
            return operator.le(float(left),float(right))
        elif operator_type==TokenType.BANG_EQUAL:
            return not self.isEqual(left,right)
        elif operator_type==TokenType.EQUAL_EQUAL:
            return self.isEqual(left,right)
        
        return None
    
    def visit_expression_stmt(self, stmt):
        self.evaluate(stmt.expression)
        return None
    
    def visit_print_stmt(self, stmt):
        value=self.evaluate(stmt.expression)
        print(self.stringify(value))
        return None
    
    def visit_var_stmt(self, stmt):
        value=None
        if stmt.intializer is not None:
            value=self.evaluate(stmt.intializer)
        self.environment.define(stmt.name.lexeme,value)
        return None
    
    def visit_variable_expr(self, expr):
        return self.environment.get(expr.name)
    
    def visit_assign_expr(self, expr):
        value=self.evaluate(expr.value)
        self.environment.assign(expr.name,value)
        return value
    def visit_block_stmt(self, stmt):
        self.executeBlock(stmt.statements, Environment(self.environment))
    

    ##########################################
    
    def evaluate(self,expr):
        return expr.accept(self)
    def execute(self,stmt):
        return stmt.accept(self)
    def executeBlock(self,statements,envirnoment):
        previous=self.environment
        try:
            self.environment=envirnoment
            for statement in statements:
                self.execute(statement)
        finally:
            self.environment=previous        
        
    def isTruthy(self,obj):
        # following what ruby does => false and nil are falsey, and everything else is truthy.
        if obj is None:
            return False
        if isinstance(obj,bool):
            return obj
        return True
    def isEqual(self,a,b):
        if (a is None) and (b is None):
            return True
        if a is None:
            return False
        return operator.eq(a,b)
    def checkNumberOperand(self,operator,*operand):
        for op in operand:
            if isinstance(op,(int,float)):
                continue
            else :
                raise MyRuntimeError(operator,"Operand must be a number")
    
    def stringify(self,object):
        if object is None:
            return "nil"        
        if isinstance(object,float):
            text=str(object)
            if text.endswith(".0"):
                text=text[0:len(text)-2]
            return text
        return str(object)    
    
        
            
    #################################
    def interpret(self,expression_or_stmts_arr):
        if True:
            try:
                statements=expression_or_stmts_arr
                for statement in statements:
                    self.execute(statement)
            except MyRuntimeError as err:
                self.lox.runtimeError(err)
        
          
    
                        
            
            
                
        
            
            
        
            
        
    