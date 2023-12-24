""" This module defines a set of functions that calculate hyperoperations and their inverses. """

from math import exp, log, sqrt, pi, e, floor, ceil
from scipy.special import lambertw


def second_tetration(base: int) -> int:
    """ Return the 2nd tetration of the argument (base ** base).
        For an explanation, see https://en.wikipedia.org/wiki/Tetration. """

    return base ** base


def super_sqrt(radicand: int) -> float:
    """ Return the super square-root of the argument (reverse of 2nd tetration).
        For an explanation, see https://en.wikipedia.org/wiki/Tetration#Square_super-root. """

    return exp(lambertw(log(radicand)).real)


def factorial(x):
    return factorial_approx(x)

def inv_factorial(x):
    return factorial_inverse_approx(x)

def inv_factorial_lt(x):
    """The base for the largest factorial that is less than the target."""
    base =  inv_factorial(x)
    lower = floor(base)
    upper = ceil(base)
    if round(factorial(upper)) > x:
        return lower
    return upper


ONE_THIRTIETH = 1/30.
def factorial_approx(x):
    """ Ramanujan approximation """
    fact = (sqrt(pi) * (x * INV_E) ** x) * (((8 * x + 4) * x + 1) * x + ONE_THIRTIETH)**(1./6.)
    return int(fact)


INV_SQRT_2PI = 1 / sqrt(2*pi)
INV_E = 1 / e
ONE_HALF = 1 / 2.
def factorial_inverse_approx(x):
    """ Rearranged Stirling's approximation.
        https://math.stackexchange.com/questions/430167/is-there-an-inverse-to-stirlings-approximation """
    log_ = log(x * INV_SQRT_2PI)
    return log_ / (lambertw(INV_E * log_).real) - ONE_HALF

    # to find the lowest factorial base that goes into x, first try rounding the output, then rounding the other way
    # OR just round both ways and take the correct one
    # https://core.ac.uk/download/pdf/215383011.pdf


FIBONACCI_PHI = (1+sqrt(5)) / 2
FIBONACCI_PSI = 1 - FIBONACCI_PHI       # (1-sqrt(5)) / 2
INV_SQRT_5 = 1 / sqrt(5)
def fibonacci(n):
    """ Return the nth Fibonacci number.
        For an explanation, see https://en.wikipedia.org/wiki/Fibonacci_number#Closed-form_expression
    """

    return int((FIBONACCI_PHI**n - FIBONACCI_PSI**n) * INV_SQRT_5)

def inv_fibonacci(x):
    """ TODO:
            - Find closed form algorithm """
    n = 0
    while True:
        if fibonacci(n) > x:
            return n - 1
        n += 1