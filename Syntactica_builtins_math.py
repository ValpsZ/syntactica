import typing
import operator


def isnumeric(val):
    try:
        float(val)
        return True
    except Exception:
        return False
def isint(val):
    try:
        int(val)
        return True
    except Exception:
        return False
    




def _syn_builtins_getMathVariablesCallables(val1:typing.Any,val2:typing.Any) -> tuple[typing.Any,typing.Any]:
    try:
        if callable(val1):
            val1=val1()
    except:pass
    try:
        if callable(val2):
            val2=val2()
    except:pass
    return val1,val2

def _syn_builtins_getMathVariablesIfNumbers(val1:typing.Any,val2:typing.Any,operator):
    if isnumeric(str(val1)) and isnumeric(str(val2)):
        result:typing.Any=operator(float(val1), float(val2))
        if int(result)==result:
            return int(result)
        return result
    return None

def _syn_builtins_tryReprOriginalType(val1Type,val2Type,result:typing.Any):
    try:
        return val1Type.__repr__(result) #type: ignore[call-arg]
    except Exception:
        try:
            return val2Type.__repr__(result) #type: ignore[call-arg]
        except Exception:
            return result







def add(val1:typing.Any=None,val2:typing.Any=None):
    if val1 is None or val2 is None: return None
    val1,val2=_syn_builtins_getMathVariablesCallables(val1,val2)
        
    try:
        return val1+val2
    except TypeError:
        isNumbers=_syn_builtins_getMathVariablesIfNumbers(val1,val2,operator.add)
        if not isNumbers is None:
            return isNumbers

        val1Str=str(val1)
        val2Str=str(val2)
        result=val1Str+val2Str

        return _syn_builtins_tryReprOriginalType(type(val1),type(val2),result)


def sub(val1:typing.Any=None,val2:typing.Any=None):
    if val1 is None or val2 is None: return None
    return add(val1,f"-{val2}")


def mult(val1:typing.Any=None,val2:typing.Any=None):
    if val1 is None or val2 is None: return None
    val1,val2=_syn_builtins_getMathVariablesCallables(val1,val2)

        
    try:
        return val1*val2
    except TypeError:
        val1Str:int|str=str(val1)
        val2Str:int|str=str(val2)
        isNumbers=_syn_builtins_getMathVariablesIfNumbers(val1,val2,operator.mul)
        if not isNumbers is None:
            return isNumbers
        elif isint(str(val1)):
            val1Str=int(val1)
        elif isint(str(val2)):
            val2Str=int(val2)
            
        if isinstance(val1Str,str) and isinstance(val2Str,str): return None #can't multiply string by string

        result=val1Str*val2Str #type:ignore[operator]

        return _syn_builtins_tryReprOriginalType(type(val1),type(val2),result)


def divide(val1:typing.Any=None,val2:typing.Any=None):
    if val1 is None or val2 is None: return None
    val1,val2=_syn_builtins_getMathVariablesCallables(val1,val2)

    try:
        return val1/val2
    except TypeError:
        return _syn_builtins_getMathVariablesIfNumbers(val1,val2,operator.truediv)
