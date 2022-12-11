""" This module is used for compression. """

import math
from hyperoperation import second_tetration as tet2
from hyperoperation import super_sqrt as ssrt
from hyperoperation import factorial, inv_factorial

def squeeze(target: int) -> list:
        """ Finds a (hopefully) smaller representation of the argument.

            >>> squeeze(73)
            [3, 4, 2]
        """

        return frequency_vector(frequency_map(target))


def frequency_map(target: int) -> dict:
    """ Finds the frequency map (table) of the bases for the smallest sum of 2nd tetrations equal to the target.

        >>> frequency_map(73)
        {3: 2, 2: 4, 1: 3}
    """

    assert target >= 0, "Cannot squeeze negative numbers: violates context."

    frequency_map = {}
    remaining_distance = target
    
    # sum 2nd tetration until they equal 'target'
    largest_tet2_base = math.floor(ssrt(remaining_distance))

    for tet2_base in range(largest_tet2_base, 0, -1):        # not accurate, but an approximation for now
        tet2_value = tet2(tet2_base)

        # find how many times the this 2nd tetration goes into 'remaining_distance'
        frequency = math.floor(remaining_distance / tet2_value)

        # approximate this value with a factorial
        factorial_base = math.floor(inv_factorial(frequency))
        factorial_value = math.factorial(factorial_base)

        # store this pair in 'frequency_map' and recalculate remaining distance
        frequency_map[tet2_base] = factorial_base
        remaining_distance -= tet2_value * factorial_value

        print("tet", tet2_value)
        print("fac", factorial_value)
        print("rem", remaining_distance)
        print(tet2_base, factorial_base)
    # due to factorial approximations, there will be some remaining distance. Use 0 as the tetration base for this.
    # frequency_map[0] = remaining_distance

    print(f"fremap: {frequency_map}")
    print(remaining_distance)
    return frequency_map


def frequency_vector(frequency_map: dict) -> list:
    """ Converts the frequency map (table) to a vector, where the index of the value corresponds to its base.
    
        >>> frequency_vector({3: 2, 2: 4, 1: 3})
        [3, 4, 2]
    """

    largest_base = max(frequency_map.keys())
    frequency_vector = [None] * largest_base

    for base in range(1, largest_base + 1):   # bases index from 1, not 0
        frequency_vector[base - 1] = frequency_map.get(base, 0)

    return frequency_vector