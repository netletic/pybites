def positive_divide(numerator, denominator):
    try:
        result = numerator / denominator
    except ZeroDivisionError:
        return 0
    except TypeError:
        raise
    else:
        if result >= 0:
            return result
        else:
            raise ValueError
