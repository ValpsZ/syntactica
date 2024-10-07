from Syntactica_builtins_math import *



def _syn_builtins_getLogicVariablesCallables(val1:typing.Any,val2:typing.Any) -> tuple[typing.Any,typing.Any]:
    try:
        if callable(val1):
            val1=val1()
    except:pass
    try:
        if callable(val2):
            val2=val2()
    except:pass
    return val1,val2

def _syn_builtins_logicGtLtLogic(val1:typing.Any,val2:typing.Any,operator):
    val2,val2=_syn_builtins_getLogicVariablesCallables(val1,val2)
    if isnumeric(val1) and isnumeric(val2):
        return operator(float(val1),float(val2))
    try:
        return operator(val1,val2)
    except Exception:pass
    return operator(str(val1),str(val2))


def eq(val1:typing.Any,val2:typing.Any):
    val1,val2=_syn_builtins_getLogicVariablesCallables(val1,val2)
    if isnumeric(val1) and isnumeric(val2):
        return operator.eq(float(val1),float(val2))
    return operator.eq(val1,val2)

def lt(val1:typing.Any,val2:typing.Any):
    return _syn_builtins_logicGtLtLogic(val1,val2,operator.lt)

def gt(val1:typing.Any,val2:typing.Any):
    return _syn_builtins_logicGtLtLogic(val1,val2,operator.gt)


def lte(val1:typing.Any,val2:typing.Any):
    iseq=eq(val1,val2)
    if iseq:return True
    return lt(val1,val2)

def gte(val1:typing.Any,val2:typing.Any):
    iseq=eq(val1,val2)
    if iseq:return True
    return gt(val1,val2)

def not_(val1:bool): #add _ because not is a python keyword
    return not val1

def neq(val1:typing.Any,val2:typing.Any):
    return not eq(val1,val2)

def ltgt(val1:typing.Any,val2:typing.Any):
    return lt(val1,val2) or gt(val1,val2)