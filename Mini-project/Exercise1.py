import simpy
import random

# Set up parameters
SEED=42
ARRIVAL_RATE = 1/1.0
SERVICE_RATE_TYPE1 = 1/0.8
SERVICE_TIME_TYPE2_MIN = 0.5
SERVICE_TIME_TYPE2_MAX = 0.7
NUM_TYPE1_CUSTOMERS = 0
NUM_TYPE2_CUSTOMERS = 0
NUM_TYPEA_SERVERS = 2
NUM_TYPEB_SERVERS = 1
SIMULATION_TIME = 1000

# Set up random seed
random.seed(SEED)

# Create the environment
env = simpy.Environment()


# Create the queues (Stores in SimPy are FIFO queues)
queue_type1 = simpy.Store(env,capacity =1000)
queue_type2 = simpy.Store(env, capacity=1000)

# Create the servers (Resources in SimPy are servers that can serve one customer at a time)
servers_type_A = simpy.Resource(env, capacity=NUM_TYPEA_SERVERS)
servers_type_B = simpy.Resource(env, capacity=NUM_TYPEB_SERVERS)
servers_type_A.requested = [False] * (NUM_TYPEA_SERVERS)
servers_type_B.requested = [False] * (NUM_TYPEB_SERVERS)

#Cute trick that will help us to know if a server is type A or B this list will be accessed by a flag :D
servers = [servers_type_A, servers_type_B]

# Create a dictionary to keep track of server usage(can be used to calculate utilization) 
# each server is a list where the first element is the total time the server was used by type 1 customers
#  and the second element is the total time the server was used by type 2 customers

#Use in normal scenario
server_usage = {'A1': [0,0], 'A2': [0,0],   'B1': [0,0]}

#add type A server
#server_usage = {'A1': [0,0], 'A2': [0,0],  'A3': [0,0] , 'B1': [0,0]}

#add type B server
#server_usage = {'A1': [0,0], 'A2': [0,0],  'B1': [0,0] , 'B2': [0,0]}


# Variables to keep track of the number of customers in each queue, total customers and waiting times in general and at each queue
count_type1_queue=0
count_type2_queue=0
count=0
waiting_times = []
waiting_times_type1 = []
waiting_times_type2 = []
# Define the arrival process
def customer_arrival(env, servers_type_A, servers_type_B):
    global NUM_TYPE1_CUSTOMERS, NUM_TYPE2_CUSTOMERS
    global count
    while True:

        # Determine the type of customer
        if random.uniform(0, 1) < 0.8:
            customer_type = 1
            NUM_TYPE1_CUSTOMERS += 1
        else:
            customer_type = 2
            NUM_TYPE2_CUSTOMERS += 1
        count+=1

        # Add the customer to the appropriate queue
        if customer_type == 1:
            arrival_time = env.now
            print("[A] type1 customer arrived at time %f" % arrival_time)
            env.process(type1_customer(queue_type1, env, servers_type_A, servers_type_B,server_usage,waiting_times, arrival_time,waiting_times_type1,None))
            yield env.timeout(random.expovariate(ARRIVAL_RATE))
        else:
            arrival_time = env.now
            print("[A] type2 customer arrived at time %f" % arrival_time)

            env.process(type2_customer(queue_type2, env, servers_type_A, servers_type_B,server_usage,waiting_times, arrival_time,waiting_times_type2,None))
            yield env.timeout(random.expovariate(ARRIVAL_RATE))

def queue_manager(env,queue_type1, queue_type2):
    server=None
    server_A=None
    server_B=None

    while True:

        # Check if there are customers in the queue 2 because it's the priority queue
        if len(queue_type2.items) > 0:

            # Check if there are available servers type A
            for i in range(0, NUM_TYPEA_SERVERS):
                if not servers_type_A.requested[i]:
                    server_A = i
                    break
            
            # Check if there are available servers type B
            for i in range(0, NUM_TYPEB_SERVERS):
                if not servers_type_B.requested[i]:
                    server_B = NUM_TYPEA_SERVERS + i
                    break

            # If there are available servers type A and B
            if server_A is not None and server_B is not None:

                # Get the customer from the queue
                customer = queue_type2.get()

                # Request a server to serve the customer
                env.process(type2_customer(queue_type2, env, servers_type_A, servers_type_B,server_usage,waiting_times, env.now,waiting_times_type2,customer.value))
                print("[Q] customer %s was released from queue 2" % customer.value)
        
        # Check if there are customers in the queue 1
        if len(queue_type1.items) > 0:

            # Check if there are available servers
            for i in range(0, NUM_TYPEA_SERVERS):
                if not servers_type_A.requested[i]:
                    server = i
                    break

            # If no Type A server is available, check for available Type B servers
            if server is None:
                for i in range(0, NUM_TYPEB_SERVERS):
                    if not servers_type_B.requested[i]:
                        server = NUM_TYPEA_SERVERS + i
                        break     

            # If there are available servers
            if server is not None:     
                # Get the customer from the queue
                customer = queue_type1.get()

                # Request a server to serve the customer
                env.process(type1_customer(queue_type1, env, servers_type_A, servers_type_B,server_usage,waiting_times, env.now,waiting_times_type1,customer.value))
                print("[Q] Customer %s was released from queue 1" % customer.value)
    
        yield env.timeout(0.1)

# Define the service process for type 1 customers
def type1_customer(queue, env, servers_type_A, servers_type_B, server_usage,waiting_times, arrival_time,waiting_times_type1,customer):
    
    #Count the number of customers in queue 1 at any given time    
    global count_type1_queue
    count_type1_queue+=len(queue.items)

    server = None

    #just to make sure we request the right server type this flag will be 0 if we request type A server and 1 if we request type B server
    flag=0

   #create customer
    if customer == None:
        customer = {'type': 'Type 1', 'arrival_time': arrival_time}
    
    #System status
    print("[S] Current systems status: \n \t Servers Type A -> %s \n \t Servers Type B -> " % servers_type_A.requested, servers_type_B.requested)
    print(f"[S] Number of customers in queue 1 : {len(queue.items)}")

    # First, check for available Type A servers
    for i in range(0, NUM_TYPEA_SERVERS):
        if not servers_type_A.requested[i]:
            server = i
            break

    # If no Type A server is available, check for available Type B servers
    if server is None:
        for i in range(0, NUM_TYPEB_SERVERS):
            if not servers_type_B.requested[i]:
                server = NUM_TYPEA_SERVERS + i
                flag=1
                break
    
    # If no server is available, server remains None and the customer joins the queue
    if server is None:
        queue.put(customer)
        print("[Q] type1 customer joined the queue at time %f" % arrival_time)
        yield env.timeout(0)

    else:
    
        # Wait for service
        with servers[flag].request() as req:
            yield req
            
            # Request the server
            if server <= NUM_TYPEA_SERVERS-1:
                servers_type_A.requested[i] = True
                print("[W] Customer of type 1 that arrived at %f is being served by server A%d at time %f" % (customer['arrival_time'],server+1, env.now))
            
            else:
                servers_type_B.requested[i] = True
                print("[W] Customer of type 1 that arrived at %f is being served by server B%d at time %f" % (customer['arrival_time'],server - NUM_TYPEA_SERVERS+1, env.now))
            
            # Record server usage and waiting time
            server_name = 'A' + str(server+1) if server <= NUM_TYPEA_SERVERS-1 else 'B' + str(server - NUM_TYPEA_SERVERS+1)
            waiting_times.append(env.now - customer['arrival_time'])
            waiting_times_type1.append(env.now - customer['arrival_time'])
            serving_time=random.expovariate(SERVICE_RATE_TYPE1)
            server_usage[server_name][0] += serving_time

            yield env.timeout(serving_time)
            
            # Release the server
            if server <= NUM_TYPEA_SERVERS-1:
                print("[R] Released server A%d at time %f" % (server+1, env.now))
                servers_type_A.requested[server] = False
            else:
                print("[R] Released server B%d at time %f" % (server - NUM_TYPEA_SERVERS+1, env.now))
                servers_type_B.requested[server - NUM_TYPEA_SERVERS] = False
       

# Define the service process for type 2 customers
def type2_customer(queue, env, servers_type_A, servers_type_B, server_usage,waiting_times, arrival_time,waiting_times_type2,customer):
    
    #Count the number of customers in queue 2 at any given time
    global count_type2_queue
    count_type2_queue+=len(queue.items)
    
    server_A = None
    server_B = None
    
    #create customer
    if customer == None:
        customer = {'type': 'Type 2', 'arrival_time': arrival_time}
    
    #System status
    print("[S] Current systems status: \n \t Servers Type A -> %s \n \t Servers Type B -> " % servers_type_A.requested, servers_type_B.requested)
    print(f"[S] Number of customers in queue 2: {len(queue.items)}")
    
    # Request available Type A server
    for i in range(0, NUM_TYPEA_SERVERS):
        if not servers_type_A.requested[i]:
            server_A = i
            break
    
    # Request available Type B server
    for i in range(0, NUM_TYPEB_SERVERS):
        if not servers_type_B.requested[i]:
            server_B = NUM_TYPEA_SERVERS + i
            break
    
    # If either Type A or Type B server is not available, join queue
    if server_A is None or server_B is None:
        queue.put(customer)
        print("[Q] type2 customer joined the queue at time %f" % arrival_time)
        yield env.timeout(0)

    else:

        # Wait for both servers to become available
        with servers_type_A.request() as req_A, servers_type_B.request() as req_B:
            yield simpy.AllOf(env, [req_A, req_B])
            
            # Request the servers
            servers_type_A.requested[server_A] = True
            servers_type_B.requested[server_B - NUM_TYPEA_SERVERS] = True
            print("[W] Customer of type 2 is being served by server A%d and server B%d at time %f" % (server_A+1, server_B-NUM_TYPEA_SERVERS+1, env.now))
            
            # Record server usage and waiting time
            server_name_A = 'A' + str(server_A+1)
            server_name_B = 'B' + str(server_B - NUM_TYPEA_SERVERS+1)
            waiting_times.append(env.now - customer['arrival_time'])
            waiting_times_type2.append(env.now - customer['arrival_time'])
            service_time = random.uniform(SERVICE_TIME_TYPE2_MIN, SERVICE_TIME_TYPE2_MAX)
            server_usage[server_name_A][1] += service_time
            server_usage[server_name_B][1] += service_time
            
            yield env.timeout(service_time)
            
            # Release the servers
            servers_type_A.requested[server_A] = False
            servers_type_B.requested[server_B - NUM_TYPEA_SERVERS-1] = False
            print("[R] Released servers A%d and B%d at time %f" % (server_A+1,server_B - NUM_TYPEA_SERVERS+1, env.now))
            
#Start the simulation           
env.process(customer_arrival(env,servers_type_A,servers_type_B))
env.process(queue_manager(env,queue_type1,queue_type2))
env.run(until=SIMULATION_TIME)

#Calculate statistics
avg_delay_type1 = sum(waiting_times_type1) / len(waiting_times_type1)
avg_delay_type2 = sum(waiting_times_type2) / len(waiting_times_type2)
max_avg_delay = max(avg_delay_type1, avg_delay_type2)

# Print out statistics
print("\n\n----- Results -----\n\n")
print("Simulation with %d servers and %d customers" % (NUM_TYPEA_SERVERS+NUM_TYPEB_SERVERS, NUM_TYPE1_CUSTOMERS+NUM_TYPE2_CUSTOMERS))
print("Served %d Type 1 customers" % NUM_TYPE1_CUSTOMERS)
print("Served %d Type 2 customers" % NUM_TYPE2_CUSTOMERS)
print("Queue Type 1 size at end of simulation: %d" % len(queue_type1.items))
print("Queue Type 2 size at end of simulation: %d" % len(queue_type2.items))
#These statistics need to be changed if the number of servers is changed, we must add server_usage[NEWSERVER][0] to the numerator of the first print statement and 
# add server_usage[NEWSERVER][1] to the numerator of the second print statement only if the new server is type B, NEWSERVER is the identifier of the new server 
print('Average time spent in the system per Type 1 customer:', (server_usage['A1'][0] + server_usage['A2'][0]+server_usage['B1'][0]) / NUM_TYPE1_CUSTOMERS)
print('Average time spent in the system per Type 2 customer:', (server_usage['B1'][1]) / NUM_TYPE2_CUSTOMERS)
print('Average delay in queue for any customer:',sum(waiting_times)/len(waiting_times))
#Note: The following statistics are the requested in the assignment
print('Average delay in queue for Type 1 customers:', avg_delay_type1)
print('Average delay in queue for Type 2 customers:', avg_delay_type2)
print('Expected time average number in queue for type 1 customers:' ,count_type1_queue/SIMULATION_TIME)
print('Expected time average number in queue for type 2 customers:' ,count_type2_queue/SIMULATION_TIME)
print("Proportion of time server A1 was in use by type 1 customers: %.2f" % ((server_usage['A1'][0]/1000)*100))
print("Proportion of time server A1 was in use by type 2 customers: %.2f" % ((server_usage['A1'][1]/1000)*100))
print("Proportion of time server A2 was in use by type 1 customers: %.2f" % ((server_usage['A2'][0]/1000)*100))
print("Proportion of time server A2 was in use by type 2 customers: %.2f" % ((server_usage['A2'][1]/1000)*100))
print("Proportion of time server B1 was in use by type 1 customers: %.2f" % ((server_usage['B1'][0]/1000)*100))
print("Proportion of time server B1 was in use by type 2 customers: %.2f" % ((server_usage['B1'][1]/1000)*100))
#print("Proportion of time server A3 was in use by type 2 customers: %.2f" % ((server_usage['A3'][0]/1000)*100))
#print("Proportion of time server A3 was in use by type 2 customers: %.2f" % ((server_usage['A3'][1]/1000)*100))
#print("Proportion of time server B2 was in use by type 1 customers: %.2f" % ((server_usage['B2'][0]/1000)*100))
#print("Proportion of time server B2 was in use by type 2 customers: %.2f" % ((server_usage['B2'][1]/1000)*100))
print("Maximum of the average delay in queue for both types of customers:", max_avg_delay)

