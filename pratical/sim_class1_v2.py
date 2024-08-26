import sys
import random

def count_area():
    
    global time_last_event
    global sim_time
    global time_arrival
    global queue_size
    global server_freq

    top=(sim_time-time_last_event)*num_in_q
    if server_status[0] == 'busy' or server_status[1] == 'busy':
        top = (sim_time-time_last_event)
        if server_status[0] == 'busy':
            server_freq[0] += (sim_time-time_last_event)
        if server_status[1] == 'busy':
            server_freq[1] += (sim_time-time_last_event)
        
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

    if server_status== 'busy':
        time_arrival.append(sim_time)

    elif server_status[0] == 'idle':
        num_custs_delayed += 1
        delay_each[counter] = 0
        delay_sum += 0
        counter += 1
        server_status[1] = 'busy'
        time_next_event['depart2'] = sim_time + random.uniform(0,5)
    else:
        num_custs_delayed += 1
        delay_each[counter] = 0
        delay_sum += 0
        counter += 1
        server_status[0] = 'busy'
        time_next_event['depart1'] = sim_time + random.uniform(0,5)
        
    time_last_event = sim_time
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
        server_status[0] == 'idle'
        server_status[1] == 'idle'
        time_next_event['depart1'] = 1e10
        time_next_event['depart2'] = 1e10
    elif server_status[0] == 'idle' and server_status[1] == 'idle':
        time_next_event['depart1'] = 1e10
        time_next_event['depart2'] = 1e10
    elif server_status[0] == 'busy' and server_status[1] == 'idle':
        counter += 1
        num_custs_delayed += 1
        time_next_event['depart1'] = sim_time + random.uniform(3,9)

        delay_each[counter] = sim_time-time_arrival[0]
        delay_sum+=sim_time-time_arrival[0]
        server_status[0] = 'idle'
        time_arrival.pop(0)
    elif server_status[0] == 'idle' and server_status[1] == 'busy':
        counter += 1
        num_custs_delayed += 1
        time_next_event['depart2'] = sim_time + random.uniform(3,9)

        delay_each[counter] = sim_time-time_arrival[0]
        delay_sum += sim_time-time_arrival[0]

        server_status[1] = 'idle'
        time_arrival.pop(0)
    elif server_status[0] == 'busy' and server_status[1] == 'busy':
        counter += 1
        num_custs_delayed += 1

        if time_next_event['depart1'] < time_next_event['depart2']:
            time_next_event['depart1'] = sim_time + random.uniform(3,9)

            delay_each[counter] = sim_time-time_arrival[0]
            delay_sum += sim_time-time_arrival[0]

            server_status[0] = 'idle'
            time_arrival.pop(0)
        else:
            time_next_event['depart2'] = sim_time + random.uniform(3,9)

            delay_each[counter] = sim_time-time_arrival[0]
            delay_sum += sim_time-time_arrival[0]
            print(len(time_arrival))
            server_status[1] = 'idle'
            time_arrival.pop(0)

    time_last_event = sim_time
    print('depart event at {0:5.2f} size of queue is {1:2d}'.format(sim_time, len(time_arrival)))


def report():
    global delay_each
    global num_custs_delayed
    global delay_sum
    global server_freq

    avg_delay = delay_sum/num_custs_delayed
    avg_server_util = sum(server_freq)/sim_time/2
    
    print('\nAverage delay in queue:', avg_delay)
    print('Average number of customers in queue:', sum(queue_size)/sim_time)
    print('Average number of customers served per unit time:', num_custs_delayed/sim_time/2)
    print('Average server utilization:', avg_server_util)
    print('Time simulation ended:', sim_time)

#para ser possivel reproduzir ehhe
random.seed(42)
#há 2 tipos de eventos 
num_events = 2
num_in_q = 0
num_custs_delayed = 0
delay_sum = 0
server_freq = [0, 0]
queue_size = []
time_arrival = []
#this and num cuts delayed should be same
delay_each = [0]*10000
counter = 0
sim_time = 0
time_last_event = 0

server_status = ['idle', 'idle']  # status of servers

time_next_event = {
    'arrive': random.expovariate(1/5), 
    'depart1': 1e10, 
    'depart2': 1e10
}

while num_custs_delayed < 10000:
    timing()

    count_area()

    if next_event_type == 'arrive':
        arrive()
    elif next_event_type == 'depart1' or next_event_type == 'depart2':
        depart()

report()
