
#based on Simulation Modeling and Analysis, Averil Law
import sys
import random

def count_area():
    
    global time_last_event
    global sim_time
    global time_arrival
    global queue_size
    global server_freq

    top=(sim_time-time_last_event)*num_in_q
    if server_status=='busy':
        top =(sim_time-time_last_event)
        server_freq+=(sim_time-time_last_event)
        
    
    queue_size.append(top)


def timing():
    global next_event_type 
    global time_next_event
    global sim_time
    
    min_time_next_event = 1e9

    next_event_type = ''

    for e in time_next_event:
        if time_next_event[e] < min_time_next_event:
            min_time_next_event = time_next_event[e]
            next_event_type = e

    if next_event_type == '':
        print('Event list is empty at time', sim_time)
        sys.exit()

    sim_time = min_time_next_event

def arrive():
    global time_next_event
    global server_status
    global num_custs_delayed
    global time_arrival
    global delay_each
    global counter
    global delay_sum
    global time_last_event

    time_next_event['arrive'] = sim_time + random.uniform(0,10)

    if server_status == 'busy':
        time_arrival.append(sim_time)
    else:
       num_custs_delayed += 1
       #make it 0
       delay_each[counter]=0
       delay_sum=+0
       counter+1
       server_status = 'busy'
       time_next_event['depart'] = sim_time + random.uniform(0,5)
    time_last_event=sim_time
    print('arrive event at {0:5.2f} size of queue is {1:2d}'.format(sim_time, len(time_arrival)))
 
def depart():
    global time_next_event
    global server_status
    global num_custs_delayed
    global time_arrival
    global delay_each
    global counter
    global delay_sum
    global time_last_event
    if len(time_arrival) == 0:
       server_status = 'idle'
       time_next_event['depart'] = 1e10
    else:
        print
        counter+=1
        num_custs_delayed +=1
        time_next_event['depart'] = sim_time + random.uniform(3,9)

        delay_each[counter]= sim_time-time_arrival[0]
        delay_sum+=sim_time-time_arrival[0]

        time_arrival.pop(0)
    time_last_event=sim_time    
    print('depart event at {0:5.2f} size of queue is {1:2d}'.format(sim_time, len(time_arrival)))


# main

# initialize

# simulation clock
sim_time = 0.0

# state variables
server_status   = 'idle'
num_in_q        = 0
time_last_event = 0.0

# statistics
num_custs_delayed = 0
delay_each={}
counter=0
delay_sum=0
server_freq=0
queue_size=[]
# event list
time_next_event = {}
time_next_event['arrive'] = sim_time + random.uniform(0,10)
time_next_event['depart'] = 1e10

next_event_type = ''

time_arrival = []

while num_custs_delayed < 5:
    timing()
    count_area()
    if next_event_type == 'arrive':
        arrive()
    elif next_event_type == 'depart':
        depart()

if counter!=0:
    print(f"AVG of delays amounted to {delay_sum/counter}")
    print("Each costumer delay")
    for i in delay_each.keys():
        print(f"Costumer {i} was delayed for {delay_each[i]}")
else:
    print("There were no queue")
 
print(f"The AVG queue size was {sum(queue_size)/sim_time}")
print(f"Server utilization frequency was {server_freq} from {sim_time}")   
