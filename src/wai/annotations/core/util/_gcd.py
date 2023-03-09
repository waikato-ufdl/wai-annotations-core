from math import gcd as gcd2


def gcd(
        v1: int,
        *values: int
) -> int:
    """
    Calculates the greatest common divisor of multiple values.

    :param v1:
                The first value.
    :param values:
                Any additional values.
    :return:
                The greatest common divisor of all values.
    """
    # Reduce with any additional values
    for value in values:
        v1 = gcd2(v1, value)

    return v1
