from simpy import FilterStore, Environment

def is_even(item):
    return item % 2 == 0

env = Environment()
store = FilterStore(env, capacity=5)

# Add items to the store
for i in range(10):
    if is_even(i):
        store.put((i,env.now))

print(store.items)