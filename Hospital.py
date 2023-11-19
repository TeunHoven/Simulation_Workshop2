import simpy
import numpy as np

class Hospital:
    # Initialization of the Hospital Object
    def __init__(self, env, num_p_rooms, num_o_theaters, num_r_rooms, preparation_time, operation_time, recovery_time):
        self.env = env
        self.preparation_rooms = simpy.Resource(env, num_p_rooms)
        self.operation_theaters = simpy.Resource(env, num_o_theaters)
        self.recovery_rooms = simpy.Resource(env, num_r_rooms)
        self.preparation_time = preparation_time
        self.operation_time = operation_time
        self.recovery_time = recovery_time

    # Function for the Preparation Room
    def preparing(self, patient, preparation_time):
        random_time = max(1, np.random.exponential(preparation_time))
        yield self.env.timeout(random_time)

    # Function for the Operating Room
    def operating(self, patient, operation_time):
        random_time = max(1, np.random.exponential(operation_time))
        yield self.env.timeout(random_time)

    # Function for the Recovery Room
    def recovering(self, patient, recovery_time):
        random_time = max(1, np.random.exponential(recovery_time))
        yield self.env.timeout(random_time)