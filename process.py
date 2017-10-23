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
        return True if len(self.requests) == 0 else False

    def count_elements(self):
        return len(self.requests)
    
    def push(self, request, time4request):
        if self.is_full():
            raise IndexError('The buffer is full')
        return self.requests.append((request, time4request))

    def pop(self):
        return self.requests.pop()[1]


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

    def get_queue_len(self):
        if self.buffer:
            return self.buffer.count_elements()
        else:
            return 0

    def is_busy(self):
        return True if self.time_till_free != 0 else False

    def process(self):
        ''' Reduces `time till free` counter. 
        
        Returns:
            int: 0 if the process is free, the number of tacts tiil free otherwise
        '''
        if self.time_till_free != 0:
            self.time_till_free -= 1
        else:
            return 0

        if self.time_till_free == 0 and self.buffer \
                and not self.buffer.is_empty():
            self.time_till_free = self.buffer.pop()

        return self.time_till_free
    
    def _get_processing_time(self):
        ''' Returns the time from now in '''
        return int(random.expovariate(1/self.expected_processing))
        
    def add_process(self, request):
        ''' Adds request either to the process or to the attached buffer. 
        
        Args:
            request(int): id of the request, for now
            
        Returns:
            int: the time of processing, 0 if this request can not be processed
        '''
        if self.time_till_free == 0:
            if self.buffer and not self.buffer.is_empty():
                self.time_till_free = self.buffer.pop()
                self.buffer.push(request, self._get_processing_time())
            self.time_till_free = self._get_processing_time()
            return self.time_till_free
        # check if Process has a buffer and it's not full
        elif self.buffer and not self.buffer.is_full():
            time4request = self._get_processing_time()
            self.buffer.push(request, time4request)
            return time4request
        else:
            return 0
        
