import copy
import json
from pprint import pprint
import re

import colorama


KEYWORDS=["S","P","PF","Adv","Ag","Attr","IO","DO","(",")",".",","]




class ASTNode:
    def __init__(self) -> None:
        pass

class FunctionNode(ASTNode):
    def __init__(self,args,funcName) -> None:
        super().__init__()
        self.args=args
        self.funcName=funcName
    
    def __str__(self) -> str:
        return f"args: {self.args}, name: {self.funcName}"
    def __repr__(self):
        return str(self)


def ast(tokens) -> list[dict[str,str|list|dict]]:
    def parseTokens(tokens:list[str]):
        tree:list=[]
        if not (tokens[0]=="DO" and tokens[-1]=="Ag"):
            raise ValueError("Tokens must start with \"DO\" and end with \"Ag\"")
        

        i=1 #skip do


        def getBlockEnd(doIdx:int) -> int:
            i:int=doIdx
            level=0
            if tokens[i]!="DO": raise ValueError("getBlockEnd recieved invalid doIdx")
            while i < len(tokens):
                if tokens[i]=="DO":
                    level+=1
                elif tokens[i]=="Ag":
                    level-=1
                if level==0:
                    return i
                i+=1
            
            raise SyntaxError("")
        def getParenthesesEnd(startIdx:int) -> int:
            i:int=startIdx
            level=0
            if tokens[i]!="(": raise ValueError("getParenthesesEnd recieved invalid startIdx")
            while i < len(tokens):
                if tokens[i]=="(":
                    level+=1
                elif tokens[i]==")":
                    level-=1
                if level==0:
                    return i
                i+=1
            raise SyntaxError("")
        
        def getParenthesesStart(endIdx:int) -> int:
            i:int=endIdx
            level=0
            if tokens[i]!=")": raise ValueError("getParenthesesStart recieved invalid endIdx")
            while i < len(tokens):
                if tokens[i]==")":
                    level+=1
                elif tokens[i]=="(":
                    level-=1
                if level==0:
                    return i
                i-=1
            raise SyntaxError("")
        def getVariable(startIdx:int) -> tuple[str,int]:
            i:int=startIdx
            variable=""
            KEYWORDS2=copy.copy(KEYWORDS)
            KEYWORDS2.remove(".")
            while i<len(tokens)-2:
                variable+=tokens[i]+"."
                if tokens[i+2] in KEYWORDS2+[",",")","("] or tokens[i+1]!=".":
                    return variable[:-1],i-startIdx+1
                
                i+=2
            variable+=tokens[i]+"."
            return variable[:-1],i-startIdx+1
        
        currentBlockEnd=getBlockEnd(i-1)

        while i<currentBlockEnd:
            if tokens[i]=="(":
                i=getParenthesesEnd(i)
            if i>=currentBlockEnd:
                return tree

            if tokens[i]=="DO":
                blockEnd=getBlockEnd(i)
                tree.append(parseTokens(tokens[i:blockEnd+1]))
                i=blockEnd

            elif tokens[i]=="Adv":
                if tokens[i+2]=="DO": # class definition
                    block:dict[str,str|list]={"type":"classDefinition","name":tokens[i+1]}
                    i+=2 #doindex

                    blockEnd=getBlockEnd(i)
                    
                    block["block"]=parseTokens(tokens[i:blockEnd+1])
                    tree.append(block)
                    i=blockEnd

                elif tokens[i+1]=="(":
                    
                    i+=1 #( index
                    pEnd=getParenthesesEnd(i)
                    args=[]
                    i+=1
                    while i < pEnd:
                        args.append(tokens[i])
                        i+=2
                    i=pEnd

                    block={"type":"functionDefinition","args":args,"name":tokens[i+2]} #i+1: IO idx,i+2:name idx
                    i+=3 #+3: DO idx

                    blockEnd=getBlockEnd(i)
                    
                    block["block"]=parseTokens(tokens[i:blockEnd+1])
                    tree.append(block)
                    i=blockEnd
            
            elif tokens[i]=="IO":
                args=[]
                if tokens[i-1]!=")":
                    args=[tokens[i-1]]
                else:
                    pStart=getParenthesesStart(i-1)
                    #print(["DO"]+tokens[pStart+1:i-1]+["Ag"])
                    args=parseTokens(["DO"]+tokens[pStart+1:i-1]+["Ag"])
                to,length=getVariable(i+1)

                if to in KEYWORDS or to.startswith("#") or to.startswith("\"") or to.startswith("'"):
                    to="print"

                tree.append({"type":"pipe","to":to,"args":args})
                i+=length
                if to == "print": i-=1
            elif tokens[i]=="P":
                pEnd=getParenthesesEnd(i+1)
                condition=parseTokens(["DO"]+tokens[i+2:pEnd]+["Ag"])[0]

                i=pEnd+1
                blockEnd=getBlockEnd(i)
                
                block={"type":"while","condition":condition,"block":parseTokens(tokens[i:blockEnd+1])}
                tree.append(block)
            elif tokens[i]=="PF":
                if tokens[i+1]=="(":
                    val=parseTokens(["DO"]+tokens[i+2:getParenthesesEnd(i+1)]+["Ag"])
                    val=val[0]
                else:
                    val,length=getVariable(i+1)
                    i+=length
                    
                tree.append({"type":"return","val":val})
            elif tokens[i]=="Attr":
                if tokens[i+1]!="(": raise SyntaxError("Token after \"Attr\" must be \"(\"")

                pEnd=getParenthesesEnd(i+1)
                condition=parseTokens(["DO"]+tokens[i+2:pEnd]+["Ag"])[0]

                i=pEnd+1

                
                blockEnd=getBlockEnd(i)
                tree.append({"type":"if","condition":condition,"block":parseTokens(tokens[i:blockEnd+1])})
                i=blockEnd
            elif tokens[i]=="S":
                if tokens[i+1]=="(":
                    ioIdx=getParenthesesEnd(i+1)+1
                    iterator=parseTokens(["DO"]+tokens[i+2:ioIdx-1]+["Ag"])
                else:
                    iterator,length=getVariable(i+1)
                    ioIdx=i+length

                variable,length=getVariable(ioIdx+1)
                doIdx=ioIdx+length+1

                blockEnd=getBlockEnd(doIdx)
                tree.append({"type":"for","iterator":iterator,"variable":variable,"block":parseTokens(tokens[doIdx:blockEnd+1])})
                i=blockEnd
            elif not tokens[i] in KEYWORDS and not tokens[i].startswith("#"):
                if not tokens[i+1]=="IO":
                    if (tokens[i].startswith("\"") and tokens[i].endswith("\"")) or (tokens[i].startswith("'") and tokens[i].endswith("'")):
                        tree.append({"type":"string","value":tokens[i]})
                    else:
                        val,length=getVariable(i)
                        tree.append(val)
                        i+=length
            elif tokens[i].startswith("#include"):
                tree.append({"type":"include","name":tokens[i].split(" ")[1]})

            i+=1
        return tree


    return parseTokens(["DO"]+tokens+["Ag"])



def tokenizer(input: str):
    # Full tokenizer

    tokens=[]
    i=0
    for token in re.finditer(r'(#.*|(?<!\\)"""([^"]|")*?"""|(?<!\\)"([^"\\]*(\\["\\]|[^"\\])*)*"|\'[^\']*\'|[^,\s().]+|\.|,|\(|\))',input):
        tokens.append(token.group(0))
        i+=1
    return tokens




if __name__=="__main__":
    with open("Game.syn","r",encoding="utf-8") as f:
        with open("ast.json","w",encoding="utf8") as f2:json.dump(ast(tokenizer(f.read())),f2,indent=4)