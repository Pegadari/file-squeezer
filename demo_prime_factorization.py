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
import sympy
from hyperoperation import factorial, inv_factorial


int_to_bits = lambda x: len(str(bin(x))) - 2   # -2 because formatted as "0b..."
int_to_bytes = lambda x: math.ceil(int_to_bits(x) / 8)


def prime_factors_full(n: int):
    prime_factors = sympy.primefactors(n)
    prime_factors_full = []
    remainder = n
    for prime in prime_factors:
        while remainder % prime == 0:
            remainder /= prime
            prime_factors_full.append(prime)
    return prime_factors_full

def main():
    target = 476554
    # target = 1103
    # target = 6619
    # target = 23
    target_bytes = int_to_bits(target)
    print(f"""Target: {target_bytes} bits""")
    print(list(sympy.primerange(100)))

    epsilon = 1
    for i in range(target - epsilon, target + epsilon):
        if i == target: print()
        print(f"{i}: {prime_factors_full(i)}")
        if i == target: print()

if __name__ == "__main__":
    main()
