""" An algorithm that builds on the proof of concept.

    This algorithm uses tetration. For an explanation, see https://en.wikipedia.org/wiki/Tetration.

    TODO:
        - rename 'i' to 'base'
        - improve readability
        - implement functionality beyond factorial

"""

__author__ = "Darcy O'Brien"
__copyright__ = "Copyright 2022, File Squeezer"
__license__ = "GNU General Public License v3.0"
__version__ = "0.2.0"
__status__ = "Incomplete"                           # very incomplete

from math import factorial

target = 4382028402103984520845380238045780234
signed_distance = target
eqn = ""


print("start")


def fact_term(distance):
    """ Returns the closest factorial to distance. """

    i = 1
    fact = 1
    
    while abs(distance - factorial(i+1)) < abs(distance - factorial(i)):
    # while factorial(i+1) < distance:
        i += 1
        fact = factorial(i)

        # print(f"i, fact: {i}, {fact}")

    return i

def tet2_term(distance):
    i = 1
    tet2 = 1

    while (i+1)**(i+1) < distance:
        i += 1
        tet2 = i**i

        print(f"i, tet2: {i}, {tet2}")

    return i

while distance:
    fact_i = fact_term(distance)                        # index of closest factorial term to 'distance'
    fact_value = factorial(fact_i)                      # closest factorial term to 'distance'
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
    eqn += fact_str


    # progress
    # print(distance)
    # print(fact_str)

    
print(eqn)

