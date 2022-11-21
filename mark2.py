""" An algorithm that builds on the proof of concept.

    This algorithm uses tetration. For an explanation, see https://en.wikipedia.org/wiki/Tetration.

    TODO:
        - improve readability
        - implement functionality beyond factorial

"""

__author__ = "Darcy O'Brien"
__copyright__ = "Copyright 2022, File Squeezer"
__license__ = "GNU General Public License v3.0"
__version__ = "0.2.0"
__status__ = "Incomplete"

import logging
import math
from scipy.special import lambertw


def main() -> None:
    """ Entry point. """

    # logging.basicConfig(level=logging.INFO)     # comment this line to supress logging.info()

    target = 4382028402103984520845380238045780234  # unsigned int of a file's binary (this file is 16 bytes)
    print(squeeze(target))


def squeeze(target) -> list:
    """ The compression algorithm. Find an equation equal to 'target'.

    Args:
        target: the target number for the equation (>= 0)

    Returns:
        An abbreviated equation equal to 'target'

    Raises:
        AssertionError: violates context
    """

    assert target >= 0, "Cannot squeeze negative numbers: violates context."

    remaining_difference = target
    equation_abbr = []
    equation_full = ""

    while distance:
        fact_i = fact_term(distance)                        # index of closest factorial term to 'distance'
        fact_value = math.factorial(fact_i)                      # closest factorial term to 'distance'
        fact_sd = distance - fact_value                     # new signed distance using fact
        # fact_progress = progress                            # progress using fact
        fact_sign = "-" if fact_sd < 0 else "+"             # sign of fact_distance
        fact_str = f"{fact_i}!{fact_sign}"                  # equation term
        # fact_str = f"factorial({fact_i}){fact_sign}"                  # equation term



        # tet2_i = tet2_term(distance)
        # tet2_value = tet2_i ** tet2_i


        # if closest_ii > distance:
        #     sign =
        distance = abs(fact_sd)
        equation_full += fact_str


        # progress
        # print(distance)
        # print(fact_str)

    return equation_full


def fact_term(distance):
    """ Returns the closest factorial to distance. """

    base = 1
    fact = 1
    
    while abs(distance - math.factorial(base+1)) < abs(distance - math.factorial(base)):
    # while factorial(i+1) < distance:
        base += 1
        fact = math.factorial(base)

        # print(f"i, fact: {i}, {fact}")

    return base


def tet2_term(distance):
    i = 1
    tet2 = 1

    while (i+1)**(i+1) < distance:
        i += 1
        tet2 = i**i

        print(f"i, tet2: {i}, {tet2}")

    return i
    

if __name__ == "__main__":
    main()


