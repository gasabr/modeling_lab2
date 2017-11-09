import simpy

num_of_machines = 2

env = simpy.Environment()
bcs = simpy.Resource(env, capacity=num_of_machines)

def monitor(resource):
     """This is our monitoring callback."""

     print('Queue size: %s' % len(resource.queue))

def process_client(env, name):

    with bcs.request() as req:
        yield req
        print('%s starting to charge at %s' % (name, env.now))
        yield env.timeout(90)
        print('%s ending charge at %s' % (name, env.now))
        monitor(bcs)



def setup(env):
    i = 0

    while True:
        i += 1
        yield env.timeout(1)

        env.process(process_client(env, ('Car %s' % i)))

env.process(setup(env))

env.run(until=300)
