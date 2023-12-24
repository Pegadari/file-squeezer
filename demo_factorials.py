__author__ = "Darcy O'Brien (Pegadari)"
__copyright__ = "Copyright 2023, File Squeezer"
__credits__ = ["Darcy O'Brien (Pegadari)"]
__license__ = "GPLv3.0"
__version__ = "0.1"
__status__ = "Incomplete"


# disable limit for integer literals
import sys
sys.set_int_max_str_digits(0)

import timeit
from targets import TARGET_CUSTOM, TARGET_1B, TARGET_16B, TARGET_500B, TARGET_1KB, TARGET_2KB, TARGET_10KB, TARGET_50KB, TARGET_100KB

# for squeezing and expanding
import math
from hyperoperation import factorial, inv_factorial, inv_factorial_lt


int_to_bits = lambda x: len(str(bin(x))) - 2   # -2 because formatted as "0b..."
int_to_bytes = lambda x: math.ceil(int_to_bits(x) / 8)


def factorial_sum_vector(target: int):
    remainder = target
    vector = []
    while remainder:
        largest_factorial_base = inv_factorial_lt(remainder)
        if largest_factorial_base <= 0:
            break
        largest_factorial_value = factorial(largest_factorial_base)
        remainder -= largest_factorial_value
        vector.append(largest_factorial_base)
    
    assert target == sum(list(map(factorial, vector)))
    return vector


def main():
    target = 476554
    target_bytes = int_to_bits(target)
    print(f"""Target: {target_bytes} bits""")

    epsilon = 100
    for i in range(target - epsilon, target + epsilon):
        if i == target: print()
        print(f"{i}: {factorial_sum_vector(i)}")
        if i == target: print()


if __name__ == "__main__":
    main()
