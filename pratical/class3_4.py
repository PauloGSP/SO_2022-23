import argparse
import matplotlib.pyplot as plt
def initialize():
    global x, result,r,k,delta_t
    x=0.1
    r=0.2
    k=1.
    delta_t=0.01
    result=[x]
def observe():
    global x,result
    
    result.append(x)
def update(m):
    global x, result,r,k,delta_t
    if m:
        x=x+r*x*delta_t*(1-(x/k))
    else:
        h=delta_t
        f1=delta_t
        
parser = argparse.ArgumentParser(
                prog = 'Exercise 4',
                description = 'Plots a function y=a.x+b with provided a and b',
                epilog = 'Play with it')

parser.add_argument('-m',"--method",type=int, choices=[0,1],help="run with 1 for euler, 0 for kutta")
args=parser.parse_args()
#initialize(args.method)
initialize()
for t in range(30):
    
    update(args.method)
    observe()
plt.plot(result)
plt.show()