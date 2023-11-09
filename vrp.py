import sys
import os
import math
from collections import namedtuple

# A namedtuple for easier access to load properties
Load = namedtuple('Load', 'id pickup dropoff')

def calculate_distance(point1, point2):
    # Calculates the Euclidean distance between two points
    return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

def parse_line(line):
    # This function will parse a single line of the input file.
    parts = line.split()
    load_id = int(parts[0])
    # Splitting the coordinates taking into account potential negative numbers
    pickup = tuple(map(float, parts[1].strip('()').split(',')))
    dropoff = tuple(map(float, parts[2].strip('()').split(',')))
    return Load(load_id, pickup, dropoff)

def parse_input(file_path):
    # Parses the input file and returns a list of Load tuples
    loads = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines[1:]:  # Skip header line and read the rest
            if line.strip():  # Ensure it's not an empty line
                loads.append(parse_line(line))
    return loads

def assign_loads(loads):
    MAX_TIME = 720  # 12 hours in minutes
    DEPOT = (0, 0)
    drivers = []
    unassigned_loads = loads.copy()  # Copy the list so we can modify it

    while unassigned_loads:
        current_driver_loads = []
        current_time = 0
        current_location = DEPOT

        while current_time < MAX_TIME and unassigned_loads:
            # Find the closest load to the current location
            closest_load = min(unassigned_loads, key=lambda load: calculate_distance(current_location, load.pickup))
            time_to_pickup = calculate_distance(current_location, closest_load.pickup)
            time_to_dropoff = calculate_distance(closest_load.pickup, closest_load.dropoff)
            time_back_to_depot = calculate_distance(closest_load.dropoff, DEPOT)
            load_time = time_to_pickup + time_to_dropoff + time_back_to_depot

            # Check if adding this load would exceed the max time
            if current_time + load_time > MAX_TIME:
                break  # This driver can't take more loads

            # Assign this load to the current driver
            current_driver_loads.append(closest_load.id)
            current_time += time_to_pickup + time_to_dropoff
            current_location = closest_load.dropoff

            # Remove the assigned load from the list of unassigned loads
            unassigned_loads.remove(closest_load)

        # Account for the last trip back to the depot for the current driver
        if current_driver_loads:
            current_time += calculate_distance(current_location, DEPOT)
            drivers.append(current_driver_loads)

    return drivers


def process_directory(data_folder):
    for filename in os.listdir(data_folder):
        if filename.endswith(".txt"):
            file_path = os.path.join(data_folder, filename)
            print(f"Processing file: {filename}")
            loads = parse_input(file_path)
            solution = assign_loads(loads)
            for driver_loads in solution:
                print(driver_loads)
            print("\n")  # Print a newline for better separation between files

if __name__ == "__main__":
    data_folder = sys.argv[1]
    process_directory(data_folder)
