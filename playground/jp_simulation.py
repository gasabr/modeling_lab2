
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

# THIS FUNCTION IS NOT TESTED!!!

def simulate(time_limit, requests, thresholds, processors):
    ''' Simulates work of `processes` in discrete time till `time_limit`.
    
    Note:
        thresholds are CDF values. So to "encode" 2 processors with 
        prob of 1/3 to get in the 1st and 2/3 in the second use 
        the following array: [0.33, 1]
    
    Args:
        time_limit(int): amount of clocks that should be simulated
        thresholds(list of floats in [0;1)): probability thresholds, that
            certain request would get into i-th processor
        processors(list of Processor`s): processes in system
        
    Returns:
        results(Results): report about performed simulation
    '''
    # requests = get_requests_timings(LAMBDA)
    rejected_requests = []
    processed_requests = []
    
    procs_stats = {p.name: {
        'queue_len': [],
        'lost': 0,
        'done': 0,
        'processing_time': [],
        'lose_prob': 0.0,
        'performance': 0,
        } for p in processors}

    for i in range(time_limit):
        if i % 5000 == 0:
            print(i, end=' => ')
        for p in processors:
            p.process()
            
        if i in requests:
            # define in which arm request should be processed
            arm_check = random.random()
            # check if the arm can process request (either processor or buffer)
            attachment_result = 0
            attached_to = ''
            for proc_index, thresh in enumerate(thresholds):
                if arm_check < thresh:
                    attachment_result = processors[proc_index].add_process(i)
                    attached_to = processors[proc_index].name
                    procs_stats[attached_to]['queue_len'].append(
                        processors[proc_index].get_queue_len()
                    )    
                    break

            if attachment_result == 0:
                # the processor was not able to take request
                rejected_requests.append(i)
                # add one to the counter of *rejected* processes for
                # this responsible processor
                procs_stats[attached_to]['lost'] += 1
            else:
                # add one to the counter of *performed* processes for
                # this responsible processor
                processed_requests.append(i+attachment_result)
                procs_stats[attached_to]['done'] += 1
                procs_stats[attached_to]['processing_time'].append(attachment_result)
                
    if len(processed_requests) + len(rejected_requests) != len(requests):
        print("you fooled me!")
                
    # calculate results
#     for p in procs_stats:
#         # for all processors, probability of losing request =
#         # = #(lost requests) / #(all request to this processor)
#         procs_stats[p]['lose_prob'] = procs_stats[p]['lost'] / (procs_stats[p]['done'] + procs_stats[p]['lost'])
        
    return (procs_stats, rejected_requests)


# In[6]:

class Results:
    def __init__(self):
        self.load = 0.0           # нагрузка
        self.utilization = 0.0   # загрузка
        self.queue_len = {}
        self.n_requests = {}
        self.idle_time = {}
        self.processing_time = {}
        self.lose_prob = {}
        self.performance = {}


requests = get_requests_timings(LAMBDA)
p1 = Processor('P1', EXPECTED_WORK_TIME, Buffer(1))
p2 = Processor('P2', EXPECTED_WORK_TIME)
p3 = Processor('P3', EXPECTED_WORK_TIME)

stats, rejected = simulate(TIME_LIMIT, requests, [1/3, 2/3, 1], [p1, p2, p3])
