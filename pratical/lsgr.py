import numpy as np
import matplotlib.pyplot as plt

# feedback polynomial: x^3 + x + 1
def feedback(x):
    return x[0] ^ x[2] 

def generate_lsr(seed, n):
    # initialize the shift register with the seed
    sr = np.array([int(x) for x in f'{seed:0>5b}'])
    # generate n bits
    result= np.zeros((n*len(sr),), dtype=int)

    count_ones=sum(sr)
    for i in range(n):
        
        # calculate the feedback bit
        fb = feedback(sr)
        # shift the register to the right

        sr=np.append(sr[1:],fb)
        count_ones+=sum(sr)
        print(sr)
    
    
    result[:count_ones]=np.ones((count_ones,), dtype=int)

    return result

# generate 10000 random bits with seed=1
bits = generate_lsr(10, 10000)

# convert the bits to integers between 0 and 1
values = [int(''.join(map(str, bits[i:i+8])), 2) / 255 for i in range(0, len(bits), 8)]

# plot a histogram of the generated values
plt.hist(values, bins=20)
plt.show()
