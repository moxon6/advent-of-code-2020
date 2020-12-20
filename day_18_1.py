def get_bracket_matcher(lexeme_sequence):
    opening_bracket_stack = []
    bracket_matcher = {}

    for index, lexeme in enumerate(lexeme_sequence):
        if lexeme == "(":
            opening_bracket_stack.append(index)
        if lexeme == ")":
            opening_index = opening_bracket_stack.pop()
            bracket_matcher[opening_index] = index
    return bracket_matcher

def build_tree(lexeme_sequence):
    bracket_matcher = get_bracket_matcher(lexeme_sequence)
    index = 0
    tree = []
    while index < len(lexeme_sequence):
        
        if lexeme_sequence[index] == "(":
            closing_bracket_index = bracket_matcher[index]
            subsequence = lexeme_sequence[index+1:closing_bracket_index]
            tree.append(build_tree(subsequence))
            index = closing_bracket_index + 1
        else:
            tree.append(lexeme_sequence[index])
            index += 1
    return tree 

def lex(expression):
    non_numeric = ("*", "+", "(", ")")
    lexemes = []
    partial_number = []
    for char in expression:
        if char in non_numeric:
            if len(partial_number) > 0:
                lexemes.append( int("".join(partial_number)) )
                partial_number = []
            lexemes.append(char)
        else:
            partial_number.append(char)
    if len(partial_number) > 0:
        lexemes.append( int("".join(partial_number)) )
    return lexemes

def parse_op(op):
    if op == "*":
        return lambda x,y: x * y
    if op == "+":
        return lambda x,y: x + y

def evaluate_tree(tree):
    if isinstance(tree, int):
        return tree
    else:
        accumulator, tree = evaluate_tree(tree[0]), tree[1:]
        while len(tree) > 0:
            op, value = parse_op(tree[0]), evaluate_tree(tree[1])
            accumulator = op(accumulator, value)
            tree = tree[2:]
        return accumulator

def evaluate_expression(expression):
    
    expression = expression.replace(" ", "").strip()
    lexemes = lex(expression)
    tree = build_tree(lexemes)
    
    result = evaluate_tree(tree)
    return result

def main():
    with open("inputs/day18.txt") as f:
        result = sum( evaluate_expression(line) for line in f.readlines() )
        print(result)

main()