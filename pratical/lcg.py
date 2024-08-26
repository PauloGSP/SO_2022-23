
import matplotlib.pyplot as plt

# Choose LCG parameters
m = 1009
c = 1
a = 317

# Choose seed value
seed = 14

def find_cycle_length(numbers):
    # Use Floyd's cycle-finding algorithm to find the length of the cycle
    slow_ptr = 0
    fast_ptr = 0
    steps = 0
    while True:
        slow_ptr = (slow_ptr + 1) % len(numbers)
        fast_ptr = (fast_ptr + 2) % len(numbers)
        steps += 1
        if numbers[slow_ptr] == numbers[fast_ptr]:
            break
    return steps

def lcg(seed, a, c, m, n):
    result = []
    for i in range(n):
        seed = (a * seed + c) % m
        result.append(seed / m)
    return result

# Generate random numbers
n = 100000
numbers = lcg(seed, a, c, m, n)
# Check for cycle
cycle_length = find_cycle_length(numbers)
if cycle_length == n:
    print("LCG provides a full period")
else:
    print("LCG does not provide a full period. Cycle length:", cycle_length)

# Plot histogram
plt.hist(numbers, bins=50)
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.show()
