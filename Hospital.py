import simpy
import numpy as np
import util

class Hospital:
    # Initialization of the Hospital Object
    def __init__(self, env, num_p_rooms, num_o_theaters, num_r_rooms, num_nurses, using_twist, time_between_rooms):
        self.env = env
        self.preparation_rooms = simpy.PriorityResource(env, num_p_rooms)
        self.operation_theaters = simpy.PriorityResource(env, num_o_theaters)
        self.recovery_rooms = simpy.Resource(env, num_r_rooms)
        self.nurses = simpy.Resource(env, num_nurses)
        self.using_twist = using_twist
        self.time_between_rooms = time_between_rooms

    # Function for the Preparation Room
    def preparing(self, preparation_time):
        if self.using_twist:
            req_nurse = self.nurses.request()
            yield req_nurse
            yield self.env.timeout(self.time_between_rooms) 
        
        yield self.env.timeout(preparation_time)
            
        if self.using_twist:
            self.nurses.release(req_nurse)

    # Function for the Operating Room
    def operating(self, operation_time):
        if self.using_twist:
            req_nurse = self.nurses.request()
            yield req_nurse
            yield self.env.timeout(self.time_between_rooms) 

        yield self.env.timeout(operation_time)

        if self.using_twist:
            self.nurses.release(req_nurse)

    # Function for the Recovery Room
    def recovering(self, recovery_time):
        if self.using_twist:
            req_nurse = self.nurses.request()
            yield req_nurse
            yield self.env.timeout(self.time_between_rooms)  
            self.nurses.release(req_nurse)

        yield self.env.timeout(recovery_time)