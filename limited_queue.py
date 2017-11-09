import simpy as sp
from random import seed, expovariate


def events(env, n_events, expected_density, resource):
    for i in range(n_events):
        env.process(env, customer(name="Customer{}".format(i), resource))
        t = expovariate(1.0/meanTBA)                 


def customer(name, resource):
    arrive = env.now()

    print("%8.4f %s: Here I am "%(env.now(),self.name))
