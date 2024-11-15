from Pre_syntax import *

def braket_test1():
    input1: str = "([{}()])"
    try:
        braket_checker(input1)
        return True
    except:
        return False

def braket_test2():
    input2: str = "([{}()[]((){()}))"
    try:
        braket_checker(input2)
        return False
    except:
        return True

def braket_test3():
    input3: str = "([)]"
    try:
        braket_checker(input3)
        return False
    except:
        return True

if __name__ == "__main__":
    tests: dict = {
        "braket_test1": braket_test1,
        "braket_test2": braket_test2,
        "braket_test3": braket_test3,
    }
    test_failed: int = 0
    for name, test in tests.items():
        if test():
            print(f"Test {name} passed")
        else:
            test_failed += 1
            print(f"Test {name} failed")

    print()
    print(f"{len(tests) - test_failed} / {len(tests)} Tests succeded")