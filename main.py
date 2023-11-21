# Simulation (TIES481) Workshop 2, University of Jyvaskyla; Semester 2, 2023
# Written by Group 1 (Yu Han, Teun Hoven, Louis Prodhon)

import simpy
import numpy as np
from enum import Enum
from Hospital import Hospital
import util

# 
#   VARIABLES AND PARAMETERS FOR THE SIMULATION MODEL
# 

PATIENTSTATE = Enum("PATIENTSTATE", ['ARRIVED', 'IN_PREPARATION', 'PREPARED', 'IN_OPERATION', 'OPERATED', 'IN_RECOVERY', 'RECOVERED'])
STARTING_PATIENTS = 1       # Number of patients already in the waiting room

NUM_P_ROOMS = 3             # Number of Preparation Rooms
NUM_O_THEATERS = 1          # Number of Operating Theaters
NUM_R_ROOMS = 3             # Number of Recovery Rooms

AVG_PREPARATION_TIME = 40   # Average Preparation time (patient in Preparation Room)
AVG_OPERATION_TIME = 20     # Average Operation time (patient in Operation Theater)
AVG_RECOVERY_TIME = 40      # Average Recovery time (patient in Recovery Room)
PATIENT_INTERVAL = 20       # Average time it takes for a new patient to arrive
ROUNDING_PRECISION = 3      # How many decimal numbers when rounding

SIM_TIME = 12000            # The time for the simulation to run

#
#   VARIABLES FOR THE MONITORING OF THE MODEL
#

patients_data = {}          # Data of each patient
saved_data = {}             # Data of some time_stamps
timeline = []               # Timeline of all the events happening in the simulation
time_in_operating_theater = 0
patients_handled = 0        # Patients handled in the SIM_TIM

#
#   UTIL METHODS
#
    
# Monitors and saves data 
def save_timed_data(save_time):
    num_waiting_room = 0
    num_preparation_room = 0
    num_waiting_for_operation = 0
    num_operating_theater = 0
    num_waiting_for_recovery = 0
    num_recovery_room = 0
    num_recovered = 0
    total = 0

    for name in patients_data:
        # Check how many patients are in which state (length of queues and utilization of rooms)
        state = patients_data[name]["current_data"]["state"]
        if(state == PATIENTSTATE.ARRIVED):
            num_waiting_room += 1
        elif(state == PATIENTSTATE.IN_PREPARATION):
            num_preparation_room += 1
        elif(state == PATIENTSTATE.PREPARED):
            num_waiting_for_operation += 1
        elif(state == PATIENTSTATE.IN_OPERATION):
            num_operating_theater += 1
        elif(state == PATIENTSTATE.OPERATED):
            num_waiting_for_recovery += 1
        elif(state == PATIENTSTATE.IN_RECOVERY):
            num_recovery_room += 1
        elif(state == PATIENTSTATE.RECOVERED):
            num_recovered += 1

    total = num_waiting_room + num_preparation_room + num_waiting_for_operation + num_operating_theater + num_waiting_for_recovery + num_recovery_room + num_recovered 
    total_in_hospital = total - num_recovered

    saved_data[save_time] = {
        "patient_distribution": {
            "waiting_room": num_waiting_room,
            "preparation_room": num_preparation_room,
            "waiting_for_operation": num_waiting_for_operation,
            "operation_theater": num_operating_theater,
            "waiting_for_recovery": num_waiting_for_recovery,
            "recovery_room": num_recovery_room,
            "recovered": num_recovered,
            "total_in_hospital": total_in_hospital,
            "total": total
        }}
    
# Save the final data after the simulation is done 
def save_final_data():
    save_timed_data(SIM_TIME)

    # Save final patient distribution
    # Variables for the saving
    all_num_patients_in_waiting_preparation = []
    max_patients_waiting_preparation = 0
    avg_patients_waiting_preparation = 0

    all_num_patients_in_waiting_operation = []
    max_patients_waiting_operation = 0
    avg_patients_waiting_operation = 0

    all_num_patients_in_waiting_recovery = []
    max_patients_wating_recovery = 0
    avg_patients_waiting_recovery = 0

    for time in saved_data:
        all_num_patients_in_waiting_preparation.append(saved_data[time]["patient_distribution"]["waiting_room"])
        all_num_patients_in_waiting_operation.append(saved_data[time]["patient_distribution"]["waiting_for_operation"])
        all_num_patients_in_waiting_recovery.append(saved_data[time]["patient_distribution"]["waiting_for_recovery"])
    
    max_patients_waiting_preparation = max(all_num_patients_in_waiting_preparation)
    avg_patients_waiting_preparation = util.get_avg(all_num_patients_in_waiting_preparation)

    max_patients_waiting_operation = max(all_num_patients_in_waiting_operation)
    avg_patients_waiting_operation = util.get_avg(all_num_patients_in_waiting_operation)

    max_patients_wating_recovery = max(all_num_patients_in_waiting_recovery)
    avg_patients_waiting_recovery = util.get_avg(all_num_patients_in_waiting_recovery)

    # Save the final distribution in the dictionary
    saved_data[SIM_TIME]["patient_distribution"]["averages"] = {
        "max_patients_waiting_preparation": max_patients_waiting_preparation,
        "avg_patients_waiting_preparation": avg_patients_waiting_preparation,
        "max_patients_waiting_operation": max_patients_waiting_operation,
        "avg_patients_waiting_operation": avg_patients_waiting_operation,
        "max_patients_waiting_recovery": max_patients_wating_recovery,
        "avg_patients_waiting_recovery": avg_patients_waiting_recovery
    }

    # Save the waiting times 
    # Variables for the saving
    waiting_times = {}
    wait_times_arrived_preparation = []
    wait_times_preparation_operation = []
    wait_times_operation_recovery = []

    # Variables for the process times saving
    all_preparation_times = []
    all_operation_times = []
    all_recovery_times = []

    # Go through each patient and calculate their waiting times and get their operating times
    for name in patients_data:
        # Saving the process times
        all_preparation_times.append(patients_data[name]["process_time"]["preparation_time"])
        all_operation_times.append(patients_data[name]["process_time"]["operation_time"])
        all_recovery_times.append(patients_data[name]["process_time"]["recovery_time"])        

        # Check the waiting times between rooms
        time_stamps = patients_data[name]["time_stamps"]
        # Make the calculations
        arrived_preparation = round(time_stamps["starting_preparation"]-time_stamps["arrived"], ROUNDING_PRECISION)
        preparation_operation = round(time_stamps["starting_operation"]-time_stamps["starting_preparation"], ROUNDING_PRECISION)
        operation_recovery = round(time_stamps["starting_recovery"]-time_stamps["starting_operation"], ROUNDING_PRECISION)

        if(arrived_preparation >= 0):
            wait_times_arrived_preparation.append(arrived_preparation)
        if(preparation_operation >= 0):
            wait_times_preparation_operation.append(preparation_operation)
        if(operation_recovery >= 0):
            wait_times_operation_recovery.append(operation_recovery)
        
        if(arrived_preparation < 0):
            arrived_preparation = f"{-arrived_preparation} - Waited but preparation state not reached!"
            preparation_operation = "State not reached!"
            operation_recovery = "State not reached!"
        elif(preparation_operation < 0):
            preparation_operation = f"{-preparation_operation} - Waited but operation state not reached!"
            operation_recovery = "State not reached!"
        elif(operation_recovery < 0):
            operation_recovery = f"{-operation_recovery} - Waited but recovery state not reached!"


        waiting_times[name] = {
            "arrived_preparation": arrived_preparation,
            "preparation_operation": preparation_operation,
            "operation_recovery": operation_recovery
        }

    # Saves the min, max and average of the process times
    process_times = {
        "preparation_time": {
            "min": min(all_preparation_times),
            "max": max(all_preparation_times),
            "avg": util.get_avg(all_preparation_times)
        },
        "operation_time": {
            "min": min(all_operation_times),
            "max": max(all_operation_times),
            "avg": util.get_avg(all_operation_times)
        },
        "recovery_time": {
            "min": min(all_recovery_times),
            "max": max(all_recovery_times),
            "avg": util.get_avg(all_recovery_times)
        }
    }

    saved_data[SIM_TIME]["process_times"] = process_times

    # Saves the Utilizations of the rooms (in %)
    saved_data[SIM_TIME]["utilization"] = {"operating_theater": (time_in_operating_theater/SIM_TIME) * 100}

    # Calculate average wait time between arriving and preparation
    avg_arrived_preparation = round(util.get_avg(wait_times_arrived_preparation), ROUNDING_PRECISION)

    # Calculate average wait time between being prepared and operation
    avg_preparation_operation = round(util.get_avg(wait_times_preparation_operation), ROUNDING_PRECISION)

    # Calculate average wait time between being operated and recovery
    avg_operation_recovery = round(util.get_avg(wait_times_operation_recovery), ROUNDING_PRECISION)

    saved_data[SIM_TIME]["waiting_times"] = waiting_times
    saved_data[SIM_TIME]["waiting_times"]["averages"] = {
        "arrived_preparation": avg_arrived_preparation,
        "preparation_operation": avg_preparation_operation,
        "operation_recovery": avg_operation_recovery,
    }

#
#   SIMULATION MODEL
#

def patient(env, name, distribution, hospital):
    global patients_handled
    global time_in_operating_theater
    timeline.append(f"{env.now:.2f} - A new patient, {name}, enters the waiting room.")

    # Initializing Patient
    in_hospital = True
    state = PATIENTSTATE.ARRIVED
    preparation_time = util.get_random_time(distribution, AVG_PREPARATION_TIME)
    operation_time = util.get_random_time(distribution, AVG_OPERATION_TIME)
    recovery_time = util.get_random_time(distribution, AVG_RECOVERY_TIME)
    patients_data[name] = { 
    "current_data": {
        "state": state,
    },
    "process_time": {
        "preparation_time": round(preparation_time, ROUNDING_PRECISION),
        "operation_time": round(operation_time, ROUNDING_PRECISION),
        "recovery_time": round(recovery_time, ROUNDING_PRECISION)
    }, 
    "time_stamps":{
        "arrived": -1, 
        "starting_preparation": -1, 
        "prepared": -1,
        "starting_operation": -1,
        "operated": -1,
        "starting_recovery": -1,
        "recovered": -1
        }}

    # Process of the Patient in Hospital
    while in_hospital:
        # Patient has arrived
        if state == PATIENTSTATE.ARRIVED:
            patients_data[name]["time_stamps"]["arrived"] = round(env.now, ROUNDING_PRECISION)
            save_timed_data(round(env.now, ROUNDING_PRECISION))
            with hospital.preparation_rooms.request() as request:
                # Wait for a free Preparation Room
                yield request
                state = PATIENTSTATE.IN_PREPARATION
                patients_data[name]["current_data"]["state"] = state

                timeline.append(f"{env.now:.2f} - Patient {name} enter preparation room.")
                patients_data[name]["time_stamps"]["starting_preparation"] = round(env.now, ROUNDING_PRECISION)

                # Wait for the preparing process
                yield env.process(hospital.preparing(preparation_time))
                timeline.append(f"{env.now:.2f} - Patient {name} has been prepared.")
                patients_data[name]["time_stamps"]["prepared"] = round(env.now, ROUNDING_PRECISION)

                state = PATIENTSTATE.PREPARED
                patients_data[name]["current_data"]["state"] = state

        # Patient has been prepared
        elif state == PATIENTSTATE.PREPARED:
            with hospital.operation_theaters.request() as request:
                # Wait for a free Operation Theater
                yield request

                state = PATIENTSTATE.IN_OPERATION
                patients_data[name]["current_data"]["state"] = state

                timeline.append(f"{env.now:.2f} - Patient {name} enter operation theater.")
                patients_data[name]["time_stamps"]["starting_operation"] = round(env.now, ROUNDING_PRECISION)

                # Wait for the operating process
                yield env.process(hospital.operating(operation_time))
                time_in_operating_theater += operation_time
                timeline.append(f"{env.now:.2f} - Patient {name} has been operated.")
                patients_data[name]["time_stamps"]["operated"] = round(env.now, ROUNDING_PRECISION)

                state = PATIENTSTATE.OPERATED
                patients_data[name]["current_data"]["state"] = state

        # Patient has been operated 
        elif state == PATIENTSTATE.OPERATED:
            with hospital.recovery_rooms.request() as request:
                # Wait for a free Recovery Room
                yield request
                state = PATIENTSTATE.IN_RECOVERY
                patients_data[name]["current_data"]["state"] = state

                timeline.append(f"{env.now:.2f} - Patient {name} enter recovery room.")
                patients_data[name]["time_stamps"]["starting_recovery"] = round(env.now, ROUNDING_PRECISION)

                # Wait for the recovery process
                yield env.process(hospital.recovering(recovery_time))
                timeline.append(f"{env.now:.2f} - Patient {name} has been recovered.")
                patients_data[name]["time_stamps"]["recovered"] = round(env.now, ROUNDING_PRECISION)

                state = PATIENTSTATE.RECOVERED
                patients_data[name]["current_data"]["state"] = state
                
        # Patient has recovered and is leaving the hospital 
        elif state == PATIENTSTATE.RECOVERED:
            timeline.append(f"{env.now:.2f} - Patient {name} has recovered and leaves the hospital!")
            patients_handled += 1
            in_hospital = False
    
    
# Setup method
def setup(env):
    hospital = Hospital(env, NUM_P_ROOMS, NUM_O_THEATERS, NUM_R_ROOMS, AVG_PREPARATION_TIME, AVG_OPERATION_TIME, AVG_RECOVERY_TIME)

    for i in range(1, STARTING_PATIENTS+1):
        env.process(patient(env, i, util.DISTRIBUTION.EXPONENTIAL, hospital))

    while True:
        yield env.timeout(np.random.exponential(PATIENT_INTERVAL))
        i += 1
        env.process(patient(env, i, util.DISTRIBUTION.EXPONENTIAL, hospital))

print("Starting Hospital Simulation... \n")
env = simpy.Environment()
env.process(setup(env))
env.run(until=SIM_TIME)

save_final_data()

#util.print_timeline(timeline)
#util.print_patient_results(patients_data)
#util.print_patient_distribution(saved_data)
#util.print_all_waiting_times(saved_data, SIM_TIME)
util.print_important_results(saved_data, SIM_TIME, patients_handled)
#util.print_all_results(saved_data, SIM_TIME, patients_data, patients_handled, timeline)

