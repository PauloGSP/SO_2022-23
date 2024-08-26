import matplotlib.pyplot as plt
import math
from sympy import primefactors
# Choose LCG parameters
m = 9
c = 1
a = 10

# Choose seed value
seed = 13

def lcg(seed, a, c, m, n):
    """Generate n random numbers using the Linear Congruential Generator."""
    numbers = []
    for i in range(n):
        seed = (a * seed + c) % m
        numbers.append(seed / m)
    return numbers

def has_full_period(a, c, m):
    """Check if a Linear Congruential Generator with the given parameters has a full period."""
    if math.gcd(c, m) != 1:
        return False
    for q in primefactors(m):
        if (a-1) % q != 0:
            print("1")
            print(q)
            return False
    if m % 4 == 0 and (a-1) % 4 != 0:
        print("2")
        return False
    print("tamos safe")
    return True

# Generate random numbers
n = m - 1
numbers = lcg(seed, a, c, m, n)

# Verify if LCG provides full period
if has_full_period(a, c, m):
    print("LCG provides a full period")
else:
    print("LCG does not provide a full period")

# Plot histogram of generated values
plt.hist(numbers, bins=50)
plt.xlabel("Random Number")
plt.ylabel("Frequency")
plt.title("Histogram of LCG Generated Values")
plt.show()
