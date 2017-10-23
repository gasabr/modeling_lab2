
# coding: utf-8

# In[1]:

import random

from process import Processor, Buffer


# In[2]:

p1 = Processor('P1', 10, Buffer(4))
p2 = Processor('P2', 10)


# In[3]:

TIME_LIMIT = 10000
LAMBDA = 0.1


# In[4]:

def get_requests_timings(lam):
    timings = []
    current_time = 0
    while current_time < TIME_LIMIT:
        next_request_in = int(random.expovariate(lam))
        timings.append(current_time + next_request_in)
        current_time += next_request_in
        
    return timings


# In[5]:

requests = get_requests_timings(LAMBDA)
print(requests[:10])
rejected_requests = []

for i in range(TIME_LIMIT):
    if i % 500 == 0:
        print(i, end=' => ')
    if i in requests:
        # define in which arm request should be processed
        arm_check = random.random()
        # check if the arm can process request (either processor or buffer)
        attachment_result = 0
        if arm_check < 0.33:
            attachment_result = p1.add_process(i)
        else:
            attachment_result = p2.add_process(i)
        
        if attachment_result == 0:
            # the processor was not able to take request
            rejected_requests.append(i)


# In[6]:

print(rejected_requests)

