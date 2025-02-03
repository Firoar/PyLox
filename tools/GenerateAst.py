import sys
from typing import  List,TextIO

from pathlib import Path

def imports():
    allImports=[
        "from abc import ABC, abstractmethod",
        "from Token import Token"
    ]
    return  allImports


def giveMeThis(field:str):
    return f"self.{field.split()[1]} = {field.split()[1]}"
def giveMeTypes(fieldlist:str):
    fields = fieldlist.split(", ")
    result = ",".join(f"{s.split()[1]}:'{s.split()[0]}'" for s in fields)
    return result
def addEmptyLines(file:TextIO,num:int):
    for i in range(num):
        print(file=file)

def ExprClass(file:TextIO,baseName:str,types:List[str]):
    print(f"class {baseName}(ABC):", file=file)
    print(" "*4+f"@abstractmethod",file=file)
    print(" "*4+"def accept(self,visitor):",file=file)
    print(" "*8+f"pass",file=file)
    addEmptyLines(file,1)

    print(" "*4+f"class Visitor:",file=file)
    for type in types:
        className=type.split()[0].strip()
        print(" "*8+"@abstractmethod",file=file )
        print(" "*8+f"def visit_{className.lower()}_{baseName.lower()}(self,expr: '{className}'):",file=file)
        print(" "*12+f"pass",file=file)
        addEmptyLines(file,1)



def defineType(file:TextIO,baseName:str,className:str,fieldList:str):
    fields:List[str]=fieldList.split(", ")

    print(f"class {className}({baseName}): ",file=file)
    print(" "*4+f"def __init__(self,{giveMeTypes(fieldList)}): ",file=file)
    for field in fields:
        print(" "*8+giveMeThis(field),file=file)
    addEmptyLines(file,1)
    print(" "*4+f"def accept(self,visitor):",file=file)
    print(" "*8+f"return visitor.visit_{className.lower()}_{baseName.lower()}(self)",file=file)
    addEmptyLines(file,2)


def defineAst(outputDir:str,baseName:str,types:List[str],extraImports=[]):
    path=outputDir+"/"+baseName+".py"
    allImports=imports()
    with open(path,"w",encoding="utf-8") as file:
        for import_name in allImports:
            print(import_name,file=file)
        for import_name in extraImports:
            print(import_name,file=file)    

        addEmptyLines(file,2)
        ExprClass(file,baseName,types)
        # i have to define Visitor here
        addEmptyLines(file,2)
        for type in types:
            className = type.split(":")[0].strip()
            fields = type.split(":")[1].strip()
            defineType(file,baseName,className,fields)


def main():
    if(len(sys.argv)!=2):
        print("Usage: generate_ast <output directory>")
        sys.exit(64)
    outputDir=sys.argv[1]
    print(outputDir,type(outputDir))
    defineAst(outputDir,"Expr",[
        "Assign   : Token name, Expr value",
        "Binary   : Expr left, Token operator, Expr right",
        "Grouping : Expr expression",
        "Literal  : Object value",
        "Unary    : Token operator, Expr right",
        "Variable : Token name"
    ])
    defineAst(outputDir, "Stmt", [
      "Expression : Expr expression",
      "Print      : Expr expression",
      "Var        : Token name, Expr intializer",
      "Block      : list statements"
    ],["from Expr import Expr"])
    

if __name__ == "__main__":
    main()



