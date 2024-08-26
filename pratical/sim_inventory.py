#s (reorder point) is inventory level at which a new order should be placed  if it drops below we should bring the inventory back up to the reorder quantity, S.
import sys
import random

def count_area():
    global time_last_event, sim_time, time_arrival, queue_size, server_freq, inventory_level, holding_cost, backorder_cost
    
    top = (sim_time - time_last_event) * num_in_q
    if server_status == 'busy':
        top = (sim_time - time_last_event)
        server_freq += (sim_time - time_last_event)
        
    queue_size.append(top)
    holding_cost.append((sim_time - time_last_event) * inventory_level)
    backorder_cost.append(max(0, (num_in_q - inventory_level)) * 5 * (sim_time - time_last_event))
    
def timing():
    global next_event_type, time_next_event, sim_time
    
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
    global time_next_event, server_status, num_custs_delayed, time_arrival, inventory_level, num_in_q, big_S, server_freq, holding_cost, backorder_cost
    
    time_next_event['arrive'] = sim_time + random.uniform(0,10)


    time_arrival.append(sim_time)
    
    if inventory_level <= big_S:
        inventory_level += 1
        num_custs_delayed += 1
        delay = random.expovariate(1.0 / 5.0)
        time_next_event['depart'] = sim_time + delay
        server_status = 'busy'
    else:
        num_in_q += 1
        
    time_last_event = sim_time
    server_freq += (sim_time - time_last_event)
    
def depart():
    global time_next_event, server_status, num_custs_delayed, time_arrival, inventory_level, num_in_q, s, big_S, server_freq, holding_cost, backorder_cost
    
    if num_in_q == 0:
        server_status = 'idle'
        time_next_event['depart'] = 1e9
    else:
        num_in_q -= 1
        num_custs_delayed += 1
        delay = random.expovariate(1.0 / 5.0)
        time_next_event['depart'] = sim_time + delay
        backorder = max(0, (num_in_q - inventory_level))
        if backorder > 0:
            inventory_level = 0
        else:
            inventory_level -= 1
        
    time_last_event = sim_time
    server_freq += (sim_time - time_last_event)

def evaluation():
    global s
    global big_S
    global order_size
    global backorder_cost

    if inventory_level>=s:
        time_next_event["evaluation"]+=1
        return
    order_size =big_S-inventory_level
    


# initialize
random.seed(98474)
# simulation clock
sim_time = 0.0
MAX_SIM=120
# state variables
server_status = 'idle'
num_in_q = 0
time_last_event = 0.0
inventory_level = 60
time_arrival = []
order_size=0

# statistics
num_custs_delayed = 0
server_freq = 0
queue_size = []
holding_cost = []
backorder_cost = []
# event list
time_next_event = {}
time_next_event['arrive'] = sim_time + random.uniform(0,10)
time_next_event['depart'] = 1e10


s_policies = [20, 40, 60]
S_policies = [40, 60, 80, 100]

# run simulation for each S and s combination
for big_S in S_policies:
    for s in s_policies:
        if big_S!=s:
            # reset statistics for each simulation run
            num_custs_delayed = 0
            server_freq = 0
            queue_size = []
            holding_cost = []
            backorder_cost = []
            time_arrival = []
            # initialize state variables for each simulation run
            server_status = 'idle'
            sim_time=0
            num_in_q = 0
            time_last_event = 0.0
            inventory_level = big_S
            
            # set initial event
            time_next_event['arrive'] = sim_time + random.uniform(0,10)
            time_next_event['depart'] = 1e10
            # run simulation until ending condition is met
            while sim_time < MAX_SIM:
                # determine next event type and time
                timing()
                
                # update statistics and state variables
                count_area()
                
                # process event
                if next_event_type == 'arrive':
                    arrive()
                elif next_event_type == 'depart':
                    depart()
            # calculate total cost, ordering cost, handling cost, and shortage cost
            total_cost = (sum(holding_cost) + sum(backorder_cost))/MAX_SIM
            ordering_cost = (num_custs_delayed * 50)/MAX_SIM
            handling_cost = sum(holding_cost)/MAX_SIM
            shortage_cost = sum(backorder_cost)/MAX_SIM

            # print results
            print(f"\nResults for S={big_S} and s={s}:")
            print(f"Total cost per month: {total_cost:.2f}")
            print(f"Ordering cost per month: {ordering_cost:.2f}")
            print(f"Handling cost per month: {handling_cost:.2f}")
            print(f"Shortage cost per month: {shortage_cost:.2f}")

   

