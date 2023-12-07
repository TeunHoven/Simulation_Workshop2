from enum import Enum
import numpy as np
import csv
import os

DISTRIBUTION = Enum("DISTRIBUTION", ['NORMAL', 'EXPONENTIAL', 'UNIFORM'])

# Get a random time according to a distribution
def get_random_time(distribution, avg_time, std_dev=1):
    if(distribution == DISTRIBUTION.NORMAL):
        return np.random.normal(avg_time, std_dev)
    elif(distribution == DISTRIBUTION.EXPONENTIAL):
        return np.random.exponential(avg_time)
    elif(distribution == DISTRIBUTION.UNIFORM):
        return np.random.uniform(avg_time, std_dev)

# Get the average of the data given
def get_avg(data):
    total = 0
    for d in data:
        total += d
    
    return (total/len(data))

# Print timeline of all the events
def print_timeline(timeline):
    print("Timeline:")
    for event in timeline:
        print(event)
    print()

# Print the resulting time stamp when activating an event of each patient
def print_patient_results(patients_data):
    for name in patients_data:
        print(f"Patient {name}: ")
        for category in patients_data[name]:
            for var in patients_data[name][category]:
                print(f"\t{var.ljust(20)}: {patients_data[name][category][var]}")
            print()

# Print all the most important results of the simulation
def print_important_results(saved_data, SIM_TIME, patients_handled):
    print(f"\nPatients handled: {patients_handled}\n")

    print("The final distribution of patients in the simulation are: ")
    for room in saved_data[SIM_TIME]["patient_distribution"]:
            if(room != "averages"):
                print(f"\tNumber of people in {room.ljust(23)}: {saved_data[SIM_TIME]['patient_distribution'][room]}")
    print()

    print("The final distribution of injuries in the simulation are: ")
    for severity in saved_data[SIM_TIME]["injuries_distribution"]:
            print(f"\tNumber of people in {severity.ljust(23)}: {saved_data[SIM_TIME]['injuries_distribution'][severity]}")
    print()

    print("The average waiting times of the simulation are: ")
    print(f"\tWaiting to be prepared:       {saved_data[SIM_TIME]['waiting_times']['averages']['arrived_preparation']}")
    print(f"\tWaiting to be operated:       {saved_data[SIM_TIME]['waiting_times']['averages']['preparation_operation']}")
    print(f"\tWaiting to get to recovery:   {saved_data[SIM_TIME]['waiting_times']['averages']['operation_recovery']}")
    print()

    print("The maximum and average patient in waiting rooms are:")
    print(f"\tWaiting to be prepared:")
    print(f"\t\tMaximum:                        {saved_data[SIM_TIME]['patient_distribution']['averages']['max_patients_waiting_preparation']}")
    print(f"\t\tAverage:                        {saved_data[SIM_TIME]['patient_distribution']['averages']['avg_patients_waiting_preparation']}")
    print(f"\tWaiting to be operated:")
    print(f"\t\tMaximum:                        {saved_data[SIM_TIME]['patient_distribution']['averages']['max_patients_waiting_operation']}")
    print(f"\t\tAverage:                        {saved_data[SIM_TIME]['patient_distribution']['averages']['avg_patients_waiting_operation']}")
    print(f"\tWaiting to get to recovery:")
    print(f"\t\tMaximum:                        {saved_data[SIM_TIME]['patient_distribution']['averages']['max_patients_waiting_recovery']}")
    print(f"\t\tAverage:                        {saved_data[SIM_TIME]['patient_distribution']['averages']['avg_patients_waiting_recovery']}")
    print()

    print("The process time per room of the patients are: ")
    for room in saved_data[SIM_TIME]["process_times"]:
            if(room == "preparation_time"):
                print("\tPreparation times:")
            elif(room == "operation_time"):
                print("\tOperation times:")
            elif(room == "recovery_time"):
                print("\tRecovery times:")
            else:
                print("Room not available!")
            for type in saved_data[SIM_TIME]["process_times"][room]:
                print(f"\t\t{type}: {saved_data[SIM_TIME]['process_times'][room][type]}")
    print()

    print("The utilization of the rooms are:")
    print(f"\tOperating Theater:                {saved_data[SIM_TIME]['utilization_total_sim']['operating_theater']:.2f}%")

# Print the distribution of people in the hospital per timestamp
def print_patient_distribution(saved_data):
    print("Time stamp data: \n")
    for time in saved_data:
        print(f"Time stamp {time}:")
        print("Distribution of patients at this time:")
        for room in saved_data[time]["patient_distribution"]:
            print(f"\tNumber of people in {room.ljust(23)}: {saved_data[time]['patient_distribution'][room]}")
        print()

        print("The final distribution of injuries in the simulation are: ")
        for severity in saved_data[time]["injuries_distribution"]:
                print(f"\tNumber of people in {severity.ljust(23)}: {saved_data[time]['injuries_distribution'][severity]}")
        print()

# Print for each patient the waiting time between rooms (events)
def print_all_waiting_times(saved_data, SIM_TIME):
    print("Waiting time per patient")
    for name in saved_data[SIM_TIME]["waiting_times"]:
        print(f"\tWaiting time patient {name}:")
        print(f"\t\tWaiting time to be prepared:       {saved_data[SIM_TIME]['waiting_times'][name]['arrived_preparation']}")
        print(f"\t\tWaiting time to be operated:       {saved_data[SIM_TIME]['waiting_times'][name]['preparation_operation']}")
        print(f"\t\tWaiting time to get to recovery:   {saved_data[SIM_TIME]['waiting_times'][name]['operation_recovery']}\n")
    print()

# Print all results saved
def print_all_results(saved_data, SIM_TIME, patients_data, patients_handled, timeline):
    print_timeline(timeline)                # Print timeline of events

    print_patient_results(patients_data)            # Print all time stamp of each event per patient

    print_patient_distribution(saved_data)    # Print distribution of people in the hospital per timestamp

    print_all_waiting_times(saved_data, SIM_TIME)       # Print all the patients waiting times

    print_important_results(saved_data, SIM_TIME, patients_handled)       # Print all the important results (averages, etc.)

class Monitor():
    def __init__(self):
        self.op_theater_is_blocking = 0
        self.op_theater_is_operational = 0
        self.recovery_room_full = 0
        self.UTIL_DUMP = []
        self.BF_DUMP = []
        self.OP_DUMP = []
        self.REC_ROOM_DUMP = []
        self.arrival_queues = []
        self.first = True

    def reset(self):
        self.arrival_queues = []
        self.first = True

    def save(self, saved_data, sim_time, num_r_rooms):
        for time in saved_data:
            result = []
            result.append(f"{time:.2f}")
            result.append(saved_data[time]["patient_distribution"]["waiting_for_operation"])

            if(saved_data[time]["patient_distribution"]["waiting_for_recovery"] > 0 & saved_data[time]["patient_distribution"]["operation_theater"] == 0):
                self.op_theater_is_blocking += 1
                result.append("False")
            elif(saved_data[time]["patient_distribution"]["operation_theater"] > 0):
                self.op_theater_is_operational += 1
                result.append("True")
            else:
                result.append("False")

            if(saved_data[time]["patient_distribution"]["recovery_room"] == num_r_rooms):
                self.recovery_room_full += 1 
        
        self.UTIL_DUMP.append(saved_data[sim_time]["utilization_total_sim"]["operating_theater"])
        self.BF_DUMP.append(self.op_theater_is_blocking)
        self.OP_DUMP.append(self.op_theater_is_operational)
        self.REC_ROOM_DUMP.append(self.recovery_room_full)

        self.op_theater_is_blocking = 0
        self.op_theater_is_operational = 0
        self.recovery_room_full = 0
        
    def save_final_data_file_assignment3(self, num_p_rooms, num_r_rooms, distribution):
        file = open(f"Simulations/TOTAL-RUN-{num_p_rooms}PrepRooms_{num_r_rooms}RecRooms.csv", "w+", encoding='UTF8', newline='')
        
        file.write(f"Mean blocking: {np.mean(self.BF_DUMP)}\n")
        file.write(f"st. dev. blocking: {np.std(self.BF_DUMP)}\n\n")

        file.write(f"Mean operational: {np.mean(self.OP_DUMP)}\n")
        file.write(f"st. dev. operational: {np.std(self.OP_DUMP)}\n\n")

        file.write(f"Mean full recovery room: {np.mean(self.REC_ROOM_DUMP)}\n")
        file.write(f"st. dev. operational: {np.std(self.REC_ROOM_DUMP)}\n\n")

        file.write(f"Mean utilization operation theater: {np.mean(self.UTIL_DUMP):.2f}%\n")
        file.write(f"st dev. operation theater: {np.std(self.UTIL_DUMP):.2f}%")

        file.close()

    def save_data_file_assignment_3(self, sim_num, num_p_rooms, num_r_rooms, seed, distribution, saved_data):
        op_theater_is_blocking = 0
        op_theater_is_operational = 0

        header = ["time", "Queue Operation Theater", "Operational", "Recovery Room Full", "utilization_rate"]

        file = open(f"Simulations/{num_p_rooms}PrepRooms_{num_r_rooms}RecRooms_Sim-{sim_num}_{distribution}_{seed}.csv", "w+", encoding='UTF8', newline='')

        writer = csv.writer(file)
        writer.writerow(header)

        for time in saved_data:
            result = []
            result.append(f"{time:.2f}")
            result.append(saved_data[time]["patient_distribution"]["waiting_for_operation"])

            if(saved_data[time]["patient_distribution"]["waiting_for_recovery"] > 0 & saved_data[time]["patient_distribution"]["operation_theater"] == 0):
                op_theater_is_blocking += 1
                result.append("False")
            elif(saved_data[time]["patient_distribution"]["operation_theater"] > 0):
                op_theater_is_operational += 1
                result.append("True")
            else:
                result.append("False")

            if(saved_data[time]["patient_distribution"]["recovery_room"] == num_r_rooms):
                result.append("True")
            else:
                result.append("False")

            result.append(saved_data[time]["utilization"]["operating_theater"])

            writer.writerow(result)

        file.close()
    
        print(f"Blocking: {op_theater_is_blocking} || Operational: {op_theater_is_operational}")

    def save_final_data_file_assignment4(self, config):
        path = f"Data/{config[0]},{config[1]},{config[2]}({config[3]}_{config[4]}),{config[5]}({config[6]}_{config[7]}),{config[8]}({config[9]}_{config[10]}),({config[11]}_{config[12]})"

        if not os.path.exists(path):
            os.makedirs(path)

        file = open(f"{path}/data.csv", "a+", encoding='UTF8', newline='')

        writer = csv.writer(file)

        result = ["Average", np.mean(self.arrival_queues), np.std(self.arrival_queues)]

        writer.writerow(result)
    
    def save_data_file_assignment4(self, config, saved_data):
        path = f"Data/{config[0]},{config[1]},{config[2]}({config[3]}_{config[4]}),{config[5]}({config[6]}_{config[7]}),{config[8]}({config[9]}_{config[10]}),({config[11]}_{config[12]})"

        if not os.path.exists(path):
            os.makedirs(path)

        if self.first:
            file = open(f"{path}/data.csv", "w+", encoding='UTF8', newline='')
        else:
            file = open(f"{path}/data.csv", "a+", encoding='UTF8', newline='') 


        writer = csv.writer(file)
        
        if self.first:
            header = ["count", "avg queue length", "std dev queue"]
            writer.writerow(header)
            self.first = False

        arrival_queue = []
        count = 0

        for time in saved_data:
            arrival_queue.append(saved_data[time]["patient_distribution"]["waiting_room"])
            count += 1

        mean = np.mean(arrival_queue)
        std = np.std(arrival_queue)

        result = [count, mean, std]

        self.arrival_queues.append(mean)

        writer.writerow(result)