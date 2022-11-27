""" This module defines a set of functions that calculate hyperoperations and their inverses. """

import math
from scipy.special import lambertw


def second_tetration(base: int) -> int:
    """ Return the 2nd tetration of the argument (base ** base).
        For an explanation, see https://en.wikipedia.org/wiki/Tetration. """

    return base ** base


def super_sqrt(radicand: int) -> float:
    """ Return the super square-root of the argument (reverse of 2nd tetration).
        For an explanation, see https://en.wikipedia.org/wiki/Tetration#Square_super-root. """

    return math.exp(lambertw(math.log(radicand)).real)