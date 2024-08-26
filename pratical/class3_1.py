import matplotlib.pyplot as plt
import argparse
def ex1():
    def initialize():
        global x, result
        x=1.
        result=[x]
    def observe():
        global x,result
        result.append(x)
    def update():
        global x, result
        a=1.1
        x=a*x

    initialize()

    for t in range(30):
        
        update()
        observe()

    plt.plot(result)
    plt.show()
