from Expr import  Expr,Binary,Unary,Grouping,Literal
from Token import  TokenType,Token

class AstPrinter(Expr.Visitor):
    def print(self,expr:'Expr')->str:
        
        return  expr.accept(self)
            
    def visit_binary_expr(self,expr: 'Binary'):
        return  self.parenthesize(expr.operator.lexeme,expr.left,expr.right)
    def visit_grouping_expr(self,expr: 'Grouping'):
        return  self.parenthesize("group",expr.expression)
    def visit_literal_expr(self,expr: 'Literal'):
        if expr.value is None:
            return "nil"
        return str(expr.value)
    def visit_unary_expr(self,expr: 'Unary'):
        return  self.parenthesize(expr.operator.lexeme,expr.right)
    
    def parenthesize(self, name, *exprs):
        print(f"name :  {name}")
        print(f"exprs : {exprs}, size : {len(exprs)}")
        st = ""
        st += "("
        
        if len(exprs)==2:
            print("jod: ",exprs[0],exprs[1])
            st+=exprs[0].accept(self)
            st += name
            st+=exprs[1].accept(self)
            
        elif len(exprs)==1:
            if name=="group":
                st+=exprs[0].accept(self)  
            else :
                st+=name
                st+=exprs[0].accept(self)  
        # st+=name          
        # for expr in exprs:
        #     st += " "
        #     st += expr.accept(self)
        st += ")"
        return st
   
    # def parenthesize(self, name, *exprs):
    #     return f"({name} " + " ".join(expr.accept(self) for expr in exprs) + ")"
    


def main():
    expression=Binary(
        Unary(
            Token(TokenType.MINUS,"-",None,1),
            Literal(123),
        ),
        Token(TokenType.STAR,"*",None,1),
        Grouping(Literal(45.67)),
    )
    print(AstPrinter().print(expression))

if __name__=="__main__":
    main()



