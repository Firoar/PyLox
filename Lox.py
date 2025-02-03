import Token
import sys
from Scanner import Scanner
from Token import TokenType,Token
from Parser import Parser
from AstPrinter import AstPrinter
from Interpreter import Interpreter

class Lox:

    def __init__(self):
        self.hadError: bool = False
        self.hadRunTimeError:bool=False
        self.interpreter=Interpreter(self)

    # @staticmethod
    # def main(args):
    #     # note :  1st(args[0]) argument always name of file(ex:Lox.py)
    #     if len(args)>2:
    #         print("Usage: py_lox [script]")
    #         sys.exit(64) # incorrect command usage
    #     elif len(args)==2:
    #         # print(f"Arguments not passed.")
    #         # run file  (runFile(args[1])
    #         print()
    #         Lox.runFile(args[1])
    #
    #     else:
    #         # for running prompt or repl
    #         print()

    def runFile(self,path:str):
        with open(path,'r') as file:
            lines=file.readlines()
            # print(content,type(content))
        bytes=''.join(lines)
        print("content of file : ")
        print(bytes)
        print("length of file : ",len(bytes))
        # call run(bytes)
        self.run(bytes)


    def runPrompt(self):
        while True:
            line=input("> ")
            if line=="":
                break 
            # call run(line)
            self.run(line)


    def run(self, source:str):
        '''
        Scanner scanner = new Scanner(source);
        List<Token> tokens = scanner.scanTokens();

        // For now, just print the tokens.
        for (Token token : tokens) {
        System.out.println(token);
        }
        '''
        scanner=Scanner(source, self)
        tokens=scanner.scanTokens()
        parser= Parser(tokens=tokens,error_handler=self.error)
        expression_and_stmts_arr=parser.parse()
        print("\n\n################################\n\n")  
        print(expression_and_stmts_arr)        
        print("\n\n################################\n\n")  
        
        
        

        if self.hadError:
            sys.exit(65)
            return
        if self.hadRunTimeError:
            sys.exit(70)
        for t in tokens:
            print(t)
        
        
        
        # print("################################\n\n")  
        # for expression in expression_and_stmts_arr:
        #     print(AstPrinter().print(expression))
        
        print("\n\n################################\n\n")  
        self.interpreter.interpret(expression_or_stmts_arr=expression_and_stmts_arr)
        print("\n\n################################\n\n")  
     
        
              
        

    def error(self, line_or_token, message: str):
        if isinstance(line_or_token, int):  # Handle error with line number
           self.report(line_or_token, "", message)
        elif isinstance(line_or_token, Token):  # Handle error with a token
            if line_or_token.type == TokenType.EOF:
                self.report(line_or_token.line, " at end", message)
            else:
                self.report(line_or_token.line, f" at '{line_or_token.lexeme}'", message)
    
   


    def report(self,line:int,where:str,message:str):
        print(f"[line \"{line}\" ] Error {where} : {message} ")
         # hadError=true
        self.hadError=True
    def runtimeError(self,error):
        print(f"{error}\n[line {error.token.line}]")    
        self.hadRunTimeError=True
        
        


if __name__=="__main__":
    newLox=Lox()
    if len(sys.argv)>2:
        print("Usage: py_lox [script]")
        sys.exit(64)  # incorrect command usage
    elif len(sys.argv)==2:
        newLox.runFile(sys.argv[1]) # first is always file name
    else:
        # run prompt or repl
        newLox.runPrompt()
