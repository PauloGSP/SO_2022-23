import matplotlib.pyplot as plt

def midsquare(seed, digits):
    result = []
    for i in range(digits):
        seed = int(seed) ** 2
        seed_str = str(seed)
        while len(seed_str) < digits * 2:
            seed_str = "0" + seed_str
        middle = int(digits / 2)
        seed_str = seed_str[middle:-middle].rstrip('.')
        seed = int(seed_str)
        result.append(seed / (10 ** digits))
    return result


# Generate 10,000 random numbers with 4 digits each
random_numbers = midsquare(1234, 4)
for i in range(1,10):
  random_numbers += midsquare(random_numbers[-1]*1000, 4)
print(random_numbers)

# Calculate the mean of the random numbers
mean = sum(random_numbers) / len(random_numbers)
print("Mean:", mean)
# Plot the histogram of the distribution
plt.hist(random_numbers, bins=50)
plt.show()
