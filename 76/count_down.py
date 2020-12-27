from functools import singledispatch


@singledispatch
def count_down(arg):
    """
    Default behavior
    """
    raise ValueError


@count_down.register
def _(arg: str):
    while arg:
        print(arg)
        arg = arg[:-1]


@count_down.register(int)
@count_down.register(float)
def _(arg):
    count_down(str(arg))


@count_down.register(list)
@count_down.register(range)
@count_down.register(set)
@count_down.register(tuple)
def _(arg):
    count_down("".join(str(c) for c in arg))


@count_down.register(dict)
def _(arg):
    count_down(list(arg.keys()))


if __name__ == "__main__":
    count_down("1234")