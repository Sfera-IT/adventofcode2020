def load_input(fname):
    with open(fname, 'r') as f:
        return f.read()


def memoize(f):
    memo = {}

    def helper(index, *args):
        if index not in memo:
            memo[index] = f(index, *args)
        return memo[index]
    return helper
