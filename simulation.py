
# coding: utf-8

# In[1]:

import random

from process import Processor, Buffer


# In[2]:

TIME_LIMIT = 100000
LAMBDA = 0.1
EXPECTED_WORK_TIME = 40


# In[3]:

p1 = Processor('P1', EXPECTED_WORK_TIME, Buffer(4))
p2 = Processor('P2', EXPECTED_WORK_TIME)


# In[4]:

def get_requests_timings(lam):
    timings = []
    current_time = 0
    while current_time < TIME_LIMIT:
        next_request_in = int(random.expovariate(lam))
        timings.append(current_time + next_request_in)
        current_time += next_request_in
        
    return timings

# TODO: tests for this
def count_intervals(timings):
    ''' Returns intervals between events in timings. '''
    intervals = list(map(lambda i: 
        rejected_requests[i] - rejected_requests[i-1], 
        reversed(range(1, len(rejected_requests)))))
    return intervals


# In[5]:

requests = get_requests_timings(LAMBDA)
print(requests[:10])
rejected_requests = []

for i in range(TIME_LIMIT):
    if i % 5000 == 0:
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

    p1.process()
    p2.process()


# In[6]:

intervals = count_intervals(rejected_requests)
print("Workload of System1: ", 1/(sum(intervals)/len(intervals)))


# ### Система 2

# In[7]:

p1 = Processor('P1', EXPECTED_WORK_TIME, Buffer(1))
p2 = Processor('P2', EXPECTED_WORK_TIME)
p3 = Processor('P3', EXPECTED_WORK_TIME)


# In[8]:

#requests = get_requests_timings(LAMBDA)
# print(requests[:10])
rejected_requests = []

for i in range(TIME_LIMIT):
    if i % 5000 == 0:
        print(i, end=' => ')
    p1.process()
    p2.process()
    p3.process()
    if i in requests:
        # define in which arm request should be processed
        arm_check = random.random()
        # check if the arm can process request (either processor or buffer)
        attachment_result = 0
        if arm_check < 0.33:
            attachment_result = p1.add_process(i)
        elif arm_check < .66:
            attachment_result = p2.add_process(i)
        else:
            attachment_result = p3.add_process(i)
        
        if attachment_result == 0:
            # the processor was not able to take request
            rejected_requests.append(i)


# In[9]:

intervals = count_intervals(rejected_requests)
print("Workload of System1: ", 1/(sum(intervals)/len(intervals)))


# In[ ]:



