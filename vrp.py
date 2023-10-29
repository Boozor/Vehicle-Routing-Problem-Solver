import sys
import math

# Function to calculate the Euclidean distance between two points
def euclidean_distance(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

# Function to calculate the total distance of a route
def calculate_total_distance(route):
    total_distance = 0
    for i in range(len(route) - 1):
        total_distance += euclidean_distance(route[i][1], route[i+1][2])
    return total_distance

# Function to assign loads to drivers using a nearest neighbor heuristic
def assign_loads_to_drivers(loads):
    drivers = []  # List to store driver schedules
    driver_schedules = []  # List to store driver schedules with costs

    while loads:
        current_driver = [loads.pop(0)]  # Initialize a new driver with the first load

        while loads:
            current_location = current_driver[-1]  # Get the current location of the driver

            # Find the index of the nearest load based on dropoff location
            nearest_load_index = min(range(len(loads)), key=lambda i: euclidean_distance(current_location[2], loads[i][1]))

            next_load = loads[nearest_load_index]  # Get the nearest load

            # Check if adding the nearest load keeps the route within the 720-minute constraint
            if calculate_total_distance(current_driver + [next_load]) <= 720:
                current_driver.append(loads.pop(nearest_load_index))
            else:
                break

        drivers.append(current_driver)

    total_cost = 0
    for i, driver in enumerate(drivers):
        schedule = [load[0] for load in driver]  # Extract load IDs for the driver's schedule
        work_time = calculate_total_distance(driver)  # Calculate the cost for the driver's route
        driver_schedules.append((i + 1, schedule, work_time))  # Store driver schedule and cost

    return driver_schedules, total_cost

# Main function to read the input file and print the solution
def solve_vrp(input_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    loads = []
    for line in lines[1:]:
        parts = line.split()
        load_id = int(parts[0])
        pickup_location = eval(parts[1])
        dropoff_location = eval(parts[2])
        loads.append((load_id, pickup_location, dropoff_location))

    # Call the function to assign loads to drivers and calculate the total cost
    driver_schedules, total_cost = assign_loads_to_drivers(loads)

    total_number_of_driven_minutes = sum(work_time for _, _, work_time in driver_schedules)  # Calculate total driven minutes
    number_of_drivers = len(driver_schedules)  # Calculate the number of drivers

    # Calculate the total cost using the given formula
    total_cost = 500 * number_of_drivers + total_number_of_driven_minutes

    # Print driver schedules, costs, and the total cost
    for driver in driver_schedules:
        driver_num, schedule, work_time = driver
        print(f"Driver {driver_num}: {schedule}")
        print(f"Work_Time: {work_time:.2f} minutes")
        print()

    print(f"Total cost for all drivers: {total_cost:.2f} minutes")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python vpr.py data.txt")
        sys.exit(1)
    input_file = sys.argv[1]
    solve_vrp(input_file)
