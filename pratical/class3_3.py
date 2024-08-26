import argparse
import matplotlib.pyplot as plt
def initialize():
    global x, xresult,y,yresult, a,b
    x=1.
    y=1.
    #a=in1
    #b=in2
    xresult=[x]
    yresult=[y]
def observe():
    global y,yresult,x,xresult
    yresult.append(y)
    xresult.append(x)
def update():
    global y,yresult,x, xresult,a,b
    curr=x
    x=0.5*x+y
    y=-0.5*curr+y
"""parser = argparse.ArgumentParser(
                prog = 'Exercise 2',
                description = 'Plots a function y=a.x+b with provided a and b',
                epilog = 'Play with it')

parser.add_argument('-a',"--asisse",type=float)
parser.add_argument('-b',"--besisse",type=float)
args=parser.parse_args()
initialize(args.asisse,args.besisse)"""
initialize()
for t in range(30):
    
    update()
    observe()
plt.plot(xresult)
plt.plot(yresult)
plt.show()