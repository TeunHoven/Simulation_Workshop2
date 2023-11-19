from enum import Enum
import numpy as np

DISTRIBUTION = Enum("DISTRIBUTION", ['NORMAL', 'EXPONENTIAL'])

# Get a random time according to a distribution
def get_random_time(distribution, avg_time, std_dev=1):
    if(distribution == DISTRIBUTION.NORMAL):
        return np.random.normal(avg_time, std_dev)
    elif(distribution == DISTRIBUTION.EXPONENTIAL):
        return np.random.exponential(avg_time)

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

# Print the distribution of people in the hospital per timestamp
def print_patient_distribution(saved_data):
    print("Time stamp data: \n")
    for time in saved_data:
        print(f"Time stamp {time}:")
        print("Distribution of patients at this time:")
        for room in saved_data[time]["patient_distribution"]:
            print(f"\tNumber of people in {room.ljust(23)}: {saved_data[time]['patient_distribution'][room]}")
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

