def test1():
    return True

if __name__ == "__main__":
    tests: dict = {
        "test1": test1
    }
    for name, test in tests.items():
        if test():
            print(f"Test {name} passed")
        else:
            print(f"Test {name} failed")
    
    print()
    print("All tests passed")
