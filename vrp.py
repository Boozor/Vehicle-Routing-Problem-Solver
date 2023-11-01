import sys
import math
import os


# Function to calculate the Euclidean distance between two points
def euclidean_distance(p1, p2):
    """Calculates the Euclidean distance between two points.

    Args:
        p1: A tuple of two floats, representing the coordinates of the first point.
        p2: A tuple of two floats, representing the coordinates of the second point.

    Returns:
        The Euclidean distance between the two points, in the same units as the
        coordinates of the points.
    """

    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)


# Function to calculate the total distance of a route
def calculate_total_distance(route):
    """Calculates the total distance of a route.

    Args:
        route: A list of tuples, where each tuple contains the load ID, pickup
            location, and dropoff location of a load.

    Returns:
        The total distance of the route, in the same units as the distances
        between the pickup and dropoff locations of the loads.
    """

    total_distance = 0.0
    for i in range(len(route) - 1):
        total_distance += euclidean_distance(route[i][1], route[i+1][2])
    return total_distance


# Function to assign loads to drivers using a nearest neighbor heuristic
def assign_loads_to_drivers(loads):
    """Assigns loads to drivers using a nearest neighbor heuristic.

    Args:
        loads: A list of tuples, where each tuple contains the load ID, pickup
            location, and dropoff location of a load.

    Returns:
        A list of lists, where each inner list contains the load IDs of the loads
        assigned to a driver.
    """

    drivers = []  # List to store driver schedules

    while loads:
        current_driver = [loads.pop(0)]  # Initialize a new driver with the first load

        while loads:
            current_location = current_driver[-1][2]  # Get the current location of the driver

            # Find the index of the nearest load based on dropoff location
            nearest_load_index = min(range(len(loads)), key=lambda i: euclidean_distance(current_location, loads[i][1]))

            next_load = loads[nearest_load_index]  # Get the nearest load

            # Check if adding the nearest load keeps the route within the 720-minute constraint
            if calculate_total_distance(current_driver + [next_load]) <= 720:
                current_driver.append(loads.pop(nearest_load_index))
            else:
                break

        drivers.append(current_driver)

    return drivers


# Main function to read the input file and print the solution
def solve_vrp(input_file):
    """Solves the vehicle routing problem.

    Args:
        input_file: The path to the input file.

    Returns:
        None.
    """

    with open(input_file, 'r') as file:
        lines = file.readlines()

    loads = []
    for line in lines[1:]:
        parts = line.split()
        load_id = int(parts[0])
        pickup_location = eval(parts[1])
        dropoff_location = eval(parts[2])
        loads.append((load_id, pickup_location, dropoff_location))

    # Assign loads to drivers
    drivers = assign_loads_to_drivers(loads)

    # Print driver schedules
    for driver_num, driver in enumerate(drivers, start=1):
        schedule = [load[0] for load in driver]  # Extract load IDs for the driver's schedule
        print(schedule)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python vrp.py train")
        sys.exit(1)

    folder_path = sys.argv[1]
    if not os.path.exists(folder_path):
        print(f"Folder not found: {folder_path}")
        sys.exit(1)

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            input_file = os.path.join(folder_path, filename)
            print(f"Solving {input_file}...")
            solve_vrp(input_file)
            print()
