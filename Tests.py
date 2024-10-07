from Pre_syntax import *
from Syntactica_builtins_logic import *

def bracket_test1():
    input1: str = "([{}()])"
    try:
        bracket_checker(input1)
        return True
    except:
        return False

def bracket_test2():
    input2: str = "([{}()[]((){()}))"
    try:
        bracket_checker(input2)
        return False
    except:
        return True

def bracket_test3():
    input3: str = "([)]"
    try:
        bracket_checker(input3)
        return False
    except:
        return True

def eq_test1():
    val1 = 2
    val2 = 2
    try:
        return eq(val1, val2)
    except:
        return False

def eq_test2():
    val1 = 2
    val2 = 3
    try:
        return not eq(val1, val2)
    except:
        return False

def eq_test3():
    val1 = 2
    val2 = "2"
    try:
        return eq(val1, val2)
    except:
        return False

def eq_test4():
    val1 = "2"
    val2 = "2"
    try:
        return eq(val1, val2)
    except:
        return False

def eq_test5():
    val1 = lambda:2
    val2 = 2
    try:
        return eq(val1, val2)
    except:
        return False

def eq_test6():
    val1 =  int(2)
    val2 = "2.0"
    try:
        return eq(val1, val2)
    except:
        return False

def eq_test7():
    val1 =  "2"
    val2 = "2.0"
    try:
        return eq(val1, val2)
    except:
        return False

def lt_test1():
    val1 = 1
    val2 = 2
    try:
        return lt(val1, val2)
    except:
        return False

def lt_test2():
    val1 = 1
    val2 = "2"
    try:
        return lt(val1, val2)
    except:
        return False

def lt_test3():
    val1 = "1"
    val2 = "2"
    try:
        return lt(val1, val2)
    except:
        return False

def lt_test4():
    val1 = []
    val2 = [1]
    try:
        return lt(val1, val2)
    except:
        return False

def lt_test5():
    val1 = 2
    val2 = 1
    try:
        return not lt(val1, val2)
    except:
        return False

if __name__ == "__main__":
    tests: dict = {
        "bracket_test1": bracket_test1,
        "bracket_test2": bracket_test2,
        "bracket_test3": bracket_test3,
        "eq_test1": eq_test1,
        "eq_test2": eq_test2,
        "eq_test3": eq_test3,
        "eq_test4": eq_test4,
        "eq_test5": eq_test5,
        "eq_test6": eq_test6,
        "eq_test7": eq_test7,
        "lt_test1": lt_test1,
        "lt_test2": lt_test2,
        "lt_test3": lt_test3,
        "lt_test4": lt_test4,
        "lt_test5": lt_test5,
    }
    test_failed: int = 0
    for name, test in tests.items():
        if test():
            print(f"Test {name} passed")
        else:
            test_failed += 1
            print(f"Test {name} failed")

    print()
    print(f"{len(tests) - test_failed} / {len(tests)} Tests passed")