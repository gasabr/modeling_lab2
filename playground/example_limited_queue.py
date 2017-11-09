""" bank24. BCC system with several counters """
import simpy as sp
from random import expovariate, seed

## Model components ------------------------           

class Source:
    """ Source generates customers randomly """

    def generate(self,number,meanTBA,resource):          
        for i in range(number):
            c = Customer("Customer{}".format(i))
            env.process(c.visit(b=resource))
            t = expovariate(1.0/meanTBA)                 
            yield env.timeout(t) # wait for the next requset to appear

class Customer:
    """ Customer arrives, is served and leaves """
    numBalking = 0                                       

    def __init__(self, name):
        self.name = name

    def visit(self,b):                                   
        visit_time = 20
        arrive = env.now
        print("%8.4f %s: Here I am "%(env.now,self.name))
        print("queue len={}".format(len(b.queue)))
        if len(b.queue) < maxInQueue:     # the test     
            with b.request() as req:
                yield req
                wait = env.now-arrive
                print("%8.4f %s: Wait %6.3f"%(env.now,self.name,wait))
                tib = expovariate(1.0/timeInBank)            
                print(" queue len={}".format(len(b.queue)))
                yield env.timeout(visit_time) # wait to be served
            print("%8.4f %s: Finished  "%(env.now,self.name))
        else:
            Customer.numBalking += 1                      
            print("%8.4f %s: BALKING   "%(env.now,self.name))

## Experiment data -------------------------------       

timeInBank = 12.0 # mean, minutes                        
ARRint = 10.0     # mean interarrival time, minutes
numServers = 1    # servers
maxInSystem = 2   # customers
maxInQueue = maxInSystem - numServers                    

maxNumber = 8
maxTime = 4000 # minutes                                      
theseed = 12345                                          

## Model/Experiment ------------------------------
env = sp.Environment()

seed(theseed)                                            
k = sp.Resource(env, capacity=numServers)            

s = Source()
env.process(s.generate(number=maxNumber,meanTBA=ARRint, 
                         resource=k))             
env.run(until=maxTime)

## Results -----------------------------------------

nb = float(Customer.numBalking)
print("balking rate is %8.4f per minute"%(nb/env.now))
