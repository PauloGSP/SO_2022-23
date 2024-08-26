import argparse
import matplotlib.pyplot as plt
def initialize(in1,in2):
    global x, result, a,b
    x=1.
    a=in1
    b=in2
    result=[x]
def observe():
    global x,result
    result.append(x)
def update():
    global x, result,a,b
    x=a*x+b
parser = argparse.ArgumentParser(
                prog = 'Exercise 2',
                description = 'Plots a function y=a.x+b with provided a and b',
                epilog = 'Play with it')

parser.add_argument('-a',"--asisse",type=float)
parser.add_argument('-b',"--besisse",type=float)
args=parser.parse_args()
initialize(args.asisse,args.besisse)
for t in range(30):
    
    update()
    observe()
plt.plot(result)
plt.show()