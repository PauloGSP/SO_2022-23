import random
import math

def generate_lcg_params():
    # choose a large prime number for m
    m = 32416190071

    # choose a random integer a between 2 and m-1
    # such that a-1 is divisible by all prime factors of m
    prime_factors = set()
    d = 2
    while d * d <= m:
        if m % d == 0:
            prime_factors.add(d)
            m //= d
        else:
            d += 1
    if m > 1:
        prime_factors.add(m)
    a = 0
    while True:
        a = random.randint(2, m-1)
        if all([(a-1) % q == 0 for q in prime_factors]):
            break

    # choose a random integer c between 1 and m-1
    # such that c and m are co-prime
    c = 0
    while True:
        c = random.randint(1, m-1)
        if math.gcd(c, m) == 1:
            break

    return a, c, m

print(generate_lcg_params( ))
