#!/usr/bin/env python3

lines = open("input", "r").readlines()


class Expression(object):
    def compute():
        raise NotImplementedError


class NumberExpression(Expression):
    value = None

    def __init__(self, value):
        self.value = value

    def compute(self):
        return int(self.value)
    
    def __repr__(self):
        return self.value


class AdditionExpression(Expression):
    lhs = None
    rhs = None

    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def compute(self):
        return self.lhs.compute() + self.rhs.compute()

    def __repr__(self):
        return repr([self.lhs, '+', self.rhs])


class MultiplicationExpression(Expression):
    lhs = None
    rhs = None

    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def compute(self):
        return self.lhs.compute() * self.rhs.compute()

    def __repr__(self):
        return repr([self.lhs, '*', self.rhs])


def tokenize(expression):
    token = ''
    for i in expression:
        if i.isnumeric():
            token += i
        else:
            if token:
                yield token
                token = ''
        if i in '()+*':
            yield i
    
    if token:
        yield token


def cleanup(expression):
    if isinstance(expression, list):
        expression = list(map(cleanup, expression))
        while '+' in expression:
            output = []
            for i in range(len(expression)):
                el = expression[i]
                if el == '+':
                    previous = output.pop()
                    expression = output + [[previous, '+', expression[i+1]]] + expression[i+2:]
                    break
                else:
                    output.append(el)

    return expression


def ast(expression):
    expressions = []
    current = expressions
    references = []
    for token in tokenize(expression):
        if token.isnumeric() or token in '*+':
            current.append(token)
        if token == '(':
            additional = []
            current.append(additional)
            references.append(current)
            current = additional
        if token == ')':
            current = references.pop()
    return cleanup(expressions)


def parse(ast):
    element = ast[0]
    if isinstance(element, list):
        lhs = parse(element)
    else:
        lhs = NumberExpression(element)

    operator = None
    rhs = None
    for i in range(len(ast[1:])):
        element = ast[i+1]
        if isinstance(element, list):
            rhs = parse(element)
        elif element in '+*':
            operator = element
        else:
            rhs = NumberExpression(element)
        
        if rhs:
            if operator == '+':
                lhs = AdditionExpression(lhs, rhs)
            if operator == '*':
                lhs = MultiplicationExpression(lhs, rhs)
            rhs = None

    return lhs


results = 0
for e in lines:
    tree = ast(e)
    parsed = parse(tree)
    #print(parsed)
    result = parsed.compute()
    #print(result)
    results += result

print(results)
