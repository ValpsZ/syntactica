def braket_checker(input: str):
    open_brakets = {"(": 0, "[": 0, "{": 0}
    close_brakets = {")": 0, "]": 0, "}": 0}
    open_to_close = {"(": ")", "[": "]", "{": "}"}
    braket_stack = []
    for line_idx, line in enumerate(input.split("\n")):
        for char in line:
            if char in open_brakets:
                open_brakets[char] += 1
                braket_stack.append(char)
            elif char in close_brakets:
                close_brakets[char] += 1
                val = open_to_close[braket_stack.pop()]
                if val != char:
                    raise SyntaxError(f"Error on line: {line_idx + 1}, Closed brakets in wrong order")
    if list(open_brakets.values()) != list(close_brakets.values()):
        raise SyntaxError(f"Error on line: {line_idx + 1}, Braket missmatch")