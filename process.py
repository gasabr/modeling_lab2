import random


class Buffer:
    def __init__(self, capacity):
        self.capacity = capacity
        self.requests = []

    def __repr__(self):
        return "Buffer full on {}/{}".format(len(self.requests), self.capacity)
        
    def is_full(self):
        return (len(self.requests) >= self.capacity)

    def is_empty(self):
        return True if len(self.requests) != 0 else False
    
    def push(self, request):
        if self.is_full():
            raise IndexError('The buffer is full')
        return self.requests.append(request)

    def pop(self, request):
        return self.requests.pop()


class Processor:

    def __init__(self, name, expected_processing, buffer=None):
        ''' Creates the process.
        
        Args:
            name(str): name of the process to be able to identify it
            expexted_processing(float): expected time of processing single
                request
            buffer(Buffer, default=None): created buffer object that should be 
                attached to that process
        '''
        self.name = name
        self.time_till_free = 0
        self.buffer = buffer
        self.expected_processing = expected_processing

    def __repr__(self):
        proc_info = "Processor <{}>, free in {}".format(
                self.name, self.time_till_free)
        if self.buffer:
            proc_info += "\n\t with: {}".format(self.buffer.__repr__())

        return proc_info

    def process(self):
        ''' Reduces `time till free` counter. 
        
        Returns:
            int: 0 if the process is free, the number of tacts tiil free otherwise
        '''
        # if the procces will be finished right now
        if self.time_till_free == 1:
            self.time_till_free -= 1
            # check if buffer exists
            # check if there are available process in buffer
            if self.buffer and not self.buffer.is_empty():
                # if so, get one process
                self.buffer.pop()
                # reset time till free
                self.time_till_free = self._get_processing_time()

        # if there is still some time for process execution just reduce timer
        elif self.time_till_free != 0:
            self.time_till_free -= 1

        else:
            return 0

        return self.time_till_free
    
    def _get_processing_time(self):
        ''' Returns the time from now in '''
        return random.expovariate(1/self.expected_processing)
        
    def add_process(self, request):
        ''' Adds request either to the process or to the attached buffer. 
        
        Args:
            request(int): id of the request, for now
            
        Returns:
            int: the time of processing, 0 if this request can not be processed
        '''
        if self.time_till_free == 0:
            self.time_till_free = int(self._get_processing_time())
        # check if Process has a buffer and it's not full
        elif self.buffer and not self.buffer.is_full():
            self.buffer.push(request)
        else:
            return 0
        
        return self.time_till_free
