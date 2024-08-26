import sys, getopt
import matplotlib.pyplot as plt


# Prey parameters
# x --> population density of prey
# alpha --> prey natural growth rate
# beta --> effect of the presence of predators on the prey growth rate

# Predator parameters
# y --> population density of predators
# gamma --> predator's natural death rate
# delta --> effect of the presence of prey on the predator's growth rate

def initialize():
    global x, y, x_result, y_result
    
    # x0 and y0
    x = X0
    y = Y0

    x_result = []
    y_result = []

def observe():
    global x, y, x_result, y_result
    x_result.append(x)
    y_result.append(y)

def update():
    global x, y
    new_x = x + (ALPHA*x - BETA*x*y) * DELTA_T
    new_y = y + (DELTA*x*y - GAMMA*y) * DELTA_T
    x = new_x
    y = new_y


if __name__ == "__main__":

    # Default Values
    ALPHA = 0.1
    BETA = 0.02
    GAMMA = 0.4
    DELTA = 0.02
    DELTA_T = 0.01
    T_FINAL = 300
    X0 = 10
    Y0 = 10

    # Remove 1st argument from the
    # list of command line arguments
    argumentList = sys.argv[1:]
    
    # Options
    options = "a:b:g:d:t:f:x:y:"

    # Long options
    long_options = ["Alpha=", "Beta=", "Gamma=", "Delta=", "D_Time=", "T_Final=", "X0=", "Y0="]
    
    try:
        # Parsing argument
        arguments, values = getopt.getopt(argumentList, options, long_options)
        
        # checking each argument
        for currentArgument, currentValue in arguments:
    
            if currentArgument in ("-a", "--Alpha"):
                ALPHA = float(currentValue)
                
            elif currentArgument in ("-b", "--Beta"):
                BETA = float(currentValue)
                
            elif currentArgument in ("-g", "--Gamma"):
                GAMMA = float(currentValue)

            elif currentArgument in ("-d", "--Delta"):
                DELTA = float(currentValue)

            elif currentArgument in ("-t", "--D_Time"):
                DELTA_T = float(currentValue)

            elif currentArgument in ("-f", "--T_Final"):
                T_FINAL = int(currentValue)

            elif currentArgument in ("-x", "--X0"):
                X0 = float(currentValue)

            elif currentArgument in ("-y", "--Y0"):
                Y0 = float(currentValue)
                
    except getopt.error as err:
        # output error, and return with an error code
        print (str(err))

    
    # Determine time vector
    num_steps = int(T_FINAL / DELTA_T)
    time_vector = [i * DELTA_T for i in range(0,num_steps)]
    initialize()

    for t in time_vector:
        observe()
        update()

    plt.plot(time_vector, x_result, 'b')
    plt.plot(time_vector, y_result, 'r-')
    plt.xlabel('Time')
    plt.ylabel('Population Size')
    plt.legend(('Prey', 'Predator'))
    plt.title('Lotka-Volterra - Euler Method')
    plt.show()

    plt.plot(x_result,y_result)
    plt.xlabel('Prey Population')
    plt.ylabel('Predator Population')
    plt.title('Prey VS Predator - Euler Method')
    plt.show()