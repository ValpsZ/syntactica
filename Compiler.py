import json


def compile(ast:list[dict[str,str|list|dict]],_isChild=False,indentLength=0):
    indent=" "*indentLength
    def replace(token):
        if token=="import":
            token="importModule"
        return token
    code=""
    if not _isChild:
        for token in ast:
            if type(token)==dict:
                if token["type"]=="include":
                    with open(f"headers/{token["name"]}","r",encoding="utf8") as f:
                        code+=f.read()+"\n"
    for token in ast:
        if type(token)==dict:
            if token["type"]=="pipe":
                args=compile(token["args"],_isChild=True)
                code+=f"""{indent}pipe("{replace(token["to"])}",{args}),\n"""
            elif token["type"]=="functionDefinition":
                code+=f"{indent}def {token["name"]}({",".join(token["args"])}):\n{" "*(indentLength+4)}pass\n{compile(token["block"],_isChild=True,indentLength=indentLength+4)}\n"
            elif token["type"]=="return":
                code+=f"{indent}return {compile([token['val']],_isChild=True,indentLength=0).removesuffix("\n").removesuffix(",")}"
            elif token["type"]=="classDefinition":
                code+=f"{indent}class {token["name"]}:\n{" "*(indentLength+4)}pass\n{compile(token["block"],_isChild=True,indentLength=indentLength+4)}\n"
            elif token["type"]=="if":
                code+=f"{indent}if ({compile([token["condition"]],_isChild=True).removesuffix(",\n")}):\n{" "*(indentLength+4)}pass\n{compile(token["block"],_isChild=True,indentLength=indentLength+4)}\n"
            elif token["type"]=="for":
                code+=f"{indent}for {token["variable"]} in {compile(token["iterator"],_isChild=True).removesuffix(",\n")}:\n{" "*(indentLength+4)}pass\n{compile(token["block"],_isChild=True,indentLength=indentLength+4)}"
            elif token["type"]=="while":
                code+=f"{indent}while ({compile([token["condition"]],_isChild=True)}):\n{" "*(indentLength+4)}pass\n{compile(token["block"],_isChild=True,indentLength=indentLength+4)}\n"
            elif token["type"]=="string":
                code+=indent+token["value"]+","
        else:
            code+=indent+token+","
    return code

if __name__=="__main__":
    with open("ast.json","r",encoding="utf-8") as f:
        with open("compiled.py","w",encoding="utf-8") as f2:
            f2.write(compile(json.load(f)))