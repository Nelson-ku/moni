from simpy.resources import container
import random
import numpy
from scipy import stats
import simpy

'''part1 set inspector1,2 and workstation1,2,3'''
class simulation:
    class inspector1(object):
        def __init__(self, env, count, workstation1, workstation2, workstation3):
            self.env = env
            self.count = count
            self.action = env.process(self.run())
            #share resource with work stations
            self.workstation1 = workstation1    
            self.workstation2 = workstation2
            self.workstation3 = workstation3

        def run(self):
            while True:
                service_time = data_input.inspect1_dep1(self)  #service time
                self.count.ls_ins1(service_time)
                # Finds the buffer with the least number of C1
                yield self.env.timeout(service_time)
                # get clock
                block_time_ins1 = self.env.now
                yield self.workstation1.component_container.put(1) | self.workstation2.component_container_1.put(1) | self.workstation3.component_container_1.put(1)
                # if self.workstation1.component_container.level <= self.workstation2.component_container_1.level or \
                #         self.workstation1.component_container.level <= self.workstation3.component_container_1.level and \
                #             self.workstation1.component_container.level < 2:
                #     yield self.workstation1.component_container.put(1)
                # elif self.workstation2.component_container_1.level <= self.workstation3.component_container_1.level and \
                #     self.workstation2.component_container_1.level < 2:
                #     yield self.workstation2.component_container_1.put(1)
                # elif self.workstation3.component_container_3.level < 2:
                #     yield self.workstation3.component_container_1.put(1)
                    #if all buffers are full, ins1 is blocked
                self.count.lb_ins1(self.env.now - block_time_ins1)


    class inspector2(object):

        def __init__(self, env, count, workstation2, workstation3):
            self.env = env
            self.count = count
            self.action = env.process(self.run())
            self.workstation2 = workstation2
            self.workstation3 = workstation3

        def run(self):
            while True:
                if bool(random.getrandbits(1)):  # Randomly decides which component to make
                    service_time = data_input.inspect1_dep2(self)  # service time
                    self.count.ls_ins2_2(service_time)
                    yield self.env.timeout(service_time)
                                    # get clock
                    block_time_ins2 = self.env.now
                    #if self.workstation2.component_container_2.level < 2:
                    yield self.workstation2.component_container_2.put(1)
                    #if all buffers are full, inspector2 is blocked
                    #else:
                    self.count.lb_ins2_2(self.env.now - block_time_ins2)
                else:
                    service_time = data_input.inspect1_dep3(self)  # service time
                    self.count.ls_ins2_3(service_time)
                    yield self.env.timeout(service_time)
                                    # get clock
                    block_time_ins2 = self.env.now
                    #if self.workstation3.component_container_3.level < 2:
                    yield self.workstation3.component_container_3.put(1)
                    #if all buffers are full, inspector2 is blocked
                    self.count.lb_ins2_3(self.env.now - block_time_ins2)


    class Workstation1(object):

        def __init__(self, env, count):
            self.env = env
            self.count = count
            self.component_container = container.Container(self.env, 2)
            self.action = env.process(self.run())

        def run(self):
            while True:
                # Waits until there are components available to use
                idle_start = self.env.now
                yield self.component_container.get(1)
                self.count.ls_ws1_idle(self.env.now - idle_start)
                # count k1_1 in use time if there is a component
                if self.component_container.level >= 1:
                    self.count.ls_k1_1_time(self.env.now - idle_start)
                # count workstation idle time
                service_time = data_input.workstation1_dep(self)  # service time
                self.count.ls_ws1(service_time)
                yield self.env.timeout(service_time)
                # count product produced
                self.count.dep_product1()


    class Workstation2(object):

        def __init__(self, env, count):
            self.env = env
            self.count = count
            self.component_container_1 = container.Container(self.env, 2)
            self.component_container_2 = container.Container(self.env, 2)
            self.action = env.process(self.run())

        def run(self):
            while True:
                # Waits until there are components available to use
                idle_start = self.env.now
                yield self.component_container_1.get(1) & self.component_container_2.get(1)
                # count k1_2 and k2 in use time if there is a component
                if self.component_container_1.level >= 1:
                    self.count.ls_k1_2_time(self.env.now - idle_start)
                if self.component_container_2.level >= 1:
                    self.count.ls_k2_time(self.env.now - idle_start)
                # count workstation idle time
                self.count.ls_ws2_idle(self.env.now - idle_start)
                service_time = data_input.workstation2_dep(self)  # service time
                self.count.ls_ws2(service_time)
                yield self.env.timeout(service_time)
                # count product produced
                self.count.dep_product2()


    class Workstation3(object):

        def __init__(self, env, count):
            self.env = env
            self.count = count
            self.component_container_1 = container.Container(self.env, 2)
            self.component_container_3 = container.Container(self.env, 2)
            self.action = env.process(self.run())

        def run(self):
            while True:
                # Waits until there are components available to use
                idle_start = self.env.now
                yield self.component_container_1.get(1) & self.component_container_3.get(1)
                # count k1_2 and k2 in use time if there is a component
                if self.component_container_1.level >= 1:
                    self.count.ls_k1_3_time(self.env.now - idle_start)
                if self.component_container_3.level >= 1:
                    self.count.ls_k3_time(self.env.now - idle_start)
                # count workstation idle time
                self.count.ls_ws3_idle(self.env.now - idle_start)
                service_time = data_input.workstation3_dep(self)  # service time
                self.count.ls_ws3(service_time)
                yield self.env.timeout(service_time)
                # count product produced
                self.count.dep_product3()

'''.part2 tracker variable to store information through the simulation'''
class tracker_variable(object):
    def __init__(self, logger):
        self.logger = logger
        self.service_times = {
            1: [],
            2: [],
            3: [],
            4: [],
            5: [],
            6: [],

        }
        self.idle_time = {
            1: [],
            2: [],
            3: [],
        }
        self.block_times = {
            1: [],
            2: [],
            3: []
        }
        self.products = {
            1: 0,
            2: 0,
            3: 0,
        }
        self.buffer = {
            1:[],
            2:[],
            3:[],
            4:[],
            5:[],
        }

    def ls_ins1(self, value):
        self.service_times[4].append(value)

    def ls_ins2_2(self, value):
        self.service_times[5].append(value)

    def ls_ins2_3(self, value):
        self.service_times[6].append(value)

    def ls_ws1(self, value):
        self.service_times[1].append(value)

    def ls_ws2(self, value):
        self.service_times[2].append(value)

    def ls_ws3(self, value):
        self.service_times[3].append(value)

    def lb_ins1(self, value):
        self.block_times[1].append(value)

    def lb_ins2_2(self, value):
        self.block_times[2].append(value)

    def lb_ins2_3(self, value):
        self.block_times[3].append(value)

    def ls_ws1_idle(self, value):
        self.idle_time[1].append(value)

    def ls_ws2_idle(self, value):
        self.idle_time[2].append(value)

    def ls_ws3_idle(self, value):
        self.idle_time[3].append(value)

    def dep_product1(self):
        self.products[1] += 1

    def dep_product2(self):
        self.products[2] += 1

    def dep_product3(self):
        self.products[3] += 1

    def ls_k1_1_time(self,value):
        self.buffer[1].append(value)

    def ls_k1_2_time(self,value):
        self.buffer[2].append(value)

    def ls_k1_3_time(self,value):
        self.buffer[3].append(value)

    def ls_k2_time(self,value):
        self.buffer[4].append(value)

    def ls_k3_time(self,value):
        self.buffer[5].append(value)

'''part3 generate data'''
class data_input:
    def data_random(datalist):
        datatotal = 0
        for x in range(0, 300):
            datatotal += float(datalist[x])
        mean = datatotal / 300
        #   Return number, adjust to seconds
        return numpy.random.exponential(mean, 1)[0]*60
        
    def inspect1_dep1(self):
        datalist = open('servinsp1.dat').read().splitlines()
        #datalist = (-numpy.log(1-(numpy.random.uniform(low=0.0,high=1.0))) * 1.0)
        return data_input.data_random(datalist)


    def inspect1_dep2(self):
        datalist = open('servinsp22.dat').read().splitlines()
        #datalist = (-numpy.log(1-(numpy.random.uniform(low=0.0,high=1.0))) * 3)
        return data_input.data_random(datalist)


    def inspect1_dep3(self):
        datalist = open('servinsp23.dat').read().splitlines()
        #datalist = (-numpy.log(1-(numpy.random.uniform(low=0.0,high=1.0))) * 3)
        return data_input.data_random(datalist)


    def workstation1_dep(self):
        datalist = open('ws1.dat').read().splitlines()
        #datalist = (-numpy.log(1-(numpy.random.uniform(low=0.0,high=1.0))) * 11)
        return data_input.data_random(datalist)


    def workstation2_dep(self):
        datalist = open('ws2.dat').read().splitlines()
        #datalist = (-numpy.log(1-(numpy.random.uniform(low=0.0,high=1.0))) * 12)
        return data_input.data_random(datalist)


    def workstation3_dep(self):
        datalist = open('ws3.dat').read().splitlines()
        #datalist = (-numpy.log(1-(numpy.random.uniform(low=0.0,high=1.0))) * 13)
        return data_input.data_random(datalist)

'''part4 calculate goal from data'''
class data_calculator:
    def ws_busytime_probability_cul(data): #data will be idle time
        sum_time = numpy.sum(data)
        probability = sum_time/60000 
        return probability

    def throughput_cul(data): #data will be total products produced
        sum_product = numpy.sum(data)
        throughput = sum_product/10000*60
        return throughput
    
    def ins1_blocktime_probability_cul(data): #data will be block time of inspectors
        sum_time = numpy.sum(data)
        probability = sum_time/10000
        return probability

    def ins2_blocktime_probability_cul(data1, data2): #data will be block time of inspectors
        sum_time1 = numpy.sum(data1)
        sum_time2 = numpy.sum(data2)
        probability = (sum_time1+ sum_time2) /10000
        return probability
    
    def buffer_occupancy_cul(data): #data will be block time of buffers
        sum_time = numpy.sum(data)
        occupancy = sum_time/10000
        return occupancy

    def calculate_statistics(data):
        block_times_1 = []
        block_times_2 = []
        block_times_3 = []
        w1_idle_time = []
        w2_idle_time = []
        w3_idle_time = []
        products_produced_1 = []
        products_produced_2 = []
        products_produced_3 = []
        buffer1_1_block_time = []
        buffer1_2_block_time = []
        buffer1_3_block_time = []
        buffer2_block_time = []
        buffer3_block_time = []
        w1_service_time = []
        w2_service_time = []
        w3_service_time = []

        for variable in data:
            block_times_1.extend(variable.block_times[1]) #inspector1 blocktime
            block_times_2.extend(variable.block_times[2]) #inspector2_2 blocktime
            block_times_3.extend(variable.block_times[3]) #inspector2_3 blocktime
            w1_idle_time.extend(variable.idle_time[1])
            w2_idle_time.extend(variable.idle_time[2])
            w3_idle_time.extend(variable.idle_time[3])
            products_produced_1.append(variable.products[1])
            products_produced_2.append(variable.products[2])
            products_produced_3.append(variable.products[3])
            w1_service_time.extend(variable.service_times[1])
            w2_service_time.extend(variable.service_times[2])
            w3_service_time.extend(variable.service_times[3])
            buffer1_1_block_time.extend(variable.buffer[1])
            buffer1_2_block_time.extend(variable.buffer[2])
            buffer1_3_block_time.extend(variable.buffer[3])
            buffer2_block_time.extend(variable.buffer[4])
            buffer3_block_time.extend(variable.buffer[5])


        throughput = data_calculator.throughput_cul(products_produced_1)/60
        print("product 1 throughput is " + str(throughput)  + "\n")
        throughput = data_calculator.throughput_cul(products_produced_2)/60
        print("product 2 throughput is " + str(throughput)  + "\n")
        throughput = data_calculator.throughput_cul(products_produced_3)/60
        print("product 3 throughput is " + str(throughput)  + "\n")
        ins_blocktime = data_calculator.ins1_blocktime_probability_cul(block_times_1)/60
        print("inspector 1 block(idle) probability is " + str(ins_blocktime)  + "\n")
        ins_blocktime = data_calculator.ins2_blocktime_probability_cul(block_times_2, block_times_3)/60
        print("inspector 2 block(idle) probability is " + str(ins_blocktime)  + "\n")
        ws_busy_prob = data_calculator.ws_busytime_probability_cul(w1_service_time)/60
        print("workstation 1 busy probability is " + str(ws_busy_prob)  + "\n")
        ws_busy_prob = data_calculator.ws_busytime_probability_cul(w2_service_time)/60
        print("workstation 2 busy probability is " + str(ws_busy_prob)  + "\n")
        ws_busy_prob = data_calculator.ws_busytime_probability_cul(w3_service_time)/60
        print("workstation 3 busy probability is " + str(ws_busy_prob)  + "\n")
        occupancy = data_calculator.buffer_occupancy_cul(buffer1_1_block_time)/60
        print("occupancy of first c1 buffer is " + str(occupancy)  + "\n")
        occupancy = data_calculator.buffer_occupancy_cul(buffer1_2_block_time)/60
        print("occupancy of second c1 buffer is " + str(occupancy)  + "\n")
        occupancy = data_calculator.buffer_occupancy_cul(buffer1_3_block_time)/60
        print("occupancy of third c1 buffer is " + str(occupancy)  + "\n")
        occupancy = data_calculator.buffer_occupancy_cul(buffer2_block_time)/60
        print("occupancy of c2 buffer is " + str(occupancy)  + "\n")
        occupancy = data_calculator.buffer_occupancy_cul(buffer3_block_time)/60
        print("occupancy of c3 buffer is " + str(occupancy)  + "\n")
        
'''part5 main body'''
class __main__:
    if __name__ == '__main__':
        # start progrom
        print("Wellcome to Mohan pipeline simulation(20 times by default)")
        i = int(input("How many times you want to run the simluation: ") or "1000")
        print("simulation will run 10000s")
        run_time = 10000  #how many second simulation will run
        REPLICATION_OUTPUTS = {}

        count = []
        print("Creating simulation environment")

        #   start loop
        for iteration in range(1, i+1):
            #   set simpy environment
            print('cycle ' + str(iteration))
            main_env = simpy.Environment()
            REPLICATION_VARIABLES = tracker_variable(None)
            workstation1 = simulation.Workstation1(main_env, REPLICATION_VARIABLES)
            workstation2 = simulation.Workstation2(main_env, REPLICATION_VARIABLES)
            workstation3 = simulation.Workstation3(main_env, REPLICATION_VARIABLES)
            inspector_1 = simulation.inspector1(main_env, REPLICATION_VARIABLES,
                                                workstation1, workstation2, workstation3)
            inspector_2 = simulation.inspector2(main_env, REPLICATION_VARIABLES, workstation2, workstation3)
            print("Running ")

            main_env.run(until=run_time) 

            #   Save iteration variables
            # REPLICATION_OUTPUTS[iteration] = simulation_output.get_means()
            count.append(REPLICATION_VARIABLES)
            # End

        #   Collect data from simulation
        print('Simulation ended, collecting output\n')
        #   calculate data
        data_calculator.calculate_statistics(count)











