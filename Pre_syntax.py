def bracket_checker(input: str):
    open_brackets = {"(": 0, "[": 0, "{": 0}
    close_brackets = {")": 0, "]": 0, "}": 0}
    open_to_close = {"(": ")", "[": "]", "{": "}"}
    bracket_stack = []
    for line_idx, line in enumerate(input.split("\n")):
        for char in line:
            if char in open_brackets:
                open_brackets[char] += 1
                bracket_stack.append(char)
            elif char in close_brackets:
                close_brackets[char] += 1
                val = open_to_close[bracket_stack.pop()]
                if val != char:
                    raise SyntaxError(f"Error on line: {line_idx + 1}, Closed brackets in wrong order")
    if list(open_brackets.values()) != list(close_brackets.values()):
        raise SyntaxError(f"Error on line: {line_idx + 1}, Bracket missmatch")