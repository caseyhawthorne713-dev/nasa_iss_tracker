#!/usr/bin/env python3
from pydantic import BaseModel
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timezone #To get orbit data closest to the current time, we need to know the current time to compare it with the epoch times in the state vectors

current_time = datetime.now()

url = "https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml"
file = "ISS_OEM_J2K_EPH.xml"

response = requests.get(url)
response.raise_for_status()

#Error handling for file download
try:
    with open("ISS_OEM_J2K_EPH.xml", "wb") as f:
        f.write(response.content)

    print(f"Successfully downloaded '{file}'")

except Exception as e:
    print(f"Error downloading '{file}': {e}")

# Define a Pydantic model to represent the orbit data
class Orbit_Data(BaseModel):
    epoch: str
    x: float
    y: float
    z: float
    x_dot: float
    y_dot: float
    z_dot: float
    speed: float # Calculated speed based on the velocity components added into the base model to allow ease of printing the speed along with the other data
    timestamp: datetime

orbit_data_list = {}

# Parse the XML file and extract the relevant data for 15 state vectors 

def parse_xml(file):

    """
    Parses data from the raw xml file and extracts the relevant data for 15 state vectors, storing it in a list of Orbit_Data objects.

    Args:
        file: The path to the XML file containing the ISS orbit data.

    Error Handling:
        If the XML file cannot be parsed, logs an error and returns 0.

    Returns:
        A list of Orbit_Data objects containing the extracted data for the state vectors.
    """
    orbit_data_list = {}
    try:
        tree = ET.parse(file)
    except ET.ParseError as e:
        print(f"Error parsing XML file '{file}': {e}")
        return 0

    root = tree.getroot()

    data = root.find(".//data")
    state_vectors = data.findall("stateVector")

    for i, sv in enumerate(state_vectors):

        epoch = sv.find("EPOCH").text
        x = float(sv.find("X").text)
        y = float(sv.find("Y").text)
        z = float(sv.find("Z").text)
        x_dot = float(sv.find("X_DOT").text)
        y_dot = float(sv.find("Y_DOT").text)
        z_dot = float(sv.find("Z_DOT").text)
        speed = (x_dot**2 + y_dot**2 + z_dot**2)**0.5

        orbit_entry = Orbit_Data(
            epoch=epoch,
            x=x,
            y=y,
            z=z,
            x_dot=x_dot,
            y_dot=y_dot,
            z_dot=z_dot,
            speed=speed,
            timestamp=datetime.now(timezone.utc) #Program execution time is recorded as the timestamp for each entry
        )

        orbit_data_list[i] = orbit_entry
    return orbit_data_list

def print_epoch_range():
    """
    Iterates through the list of orbit data entries, extracts the epoch values, and prints the range of epochs (minimum and maximum) found in the data.

    Args:
        orbit_data_list: A list of orbit data entries

    Error Handling:
        If an epoch value cannot be converted to a datetime object, logs an error and skips that entry.
        If no valid epochs are found, logs an error and returns 0.

    Returns:
        Printsthe range of epochs (minimum and maximum) found in the data.
    """

    valid_epochs = []

    for entry in orbit_data_list.values():
        try:
            # Parse the epoch string into a datetime object
            epoch_dt = datetime.strptime(entry.epoch, "%Y-%jT%H:%M:%S.%fZ")
            epoch_dt = epoch_dt.replace(tzinfo=timezone.utc)
            valid_epochs.append(epoch_dt)
        except ValueError as e:
            print(f"WARNING: Skipping invalid epoch '{entry.epoch}': {e}")
            continue

    if not valid_epochs:
        print("ERROR: No valid epochs found in orbit data.")
        return 0

    # Use datetime objects for min/max
    earliest = min(valid_epochs)
    latest = max(valid_epochs)

    print(f"Epoch range: {earliest.isoformat()} to {latest.isoformat()}")

def find_closest_epoch(data_dict):
    """
    Iterates through the list of orbit data entries, extracts the epoch values, and finds the closest epoch to the current time and returns the key of that entry.

    Args:
        orbit_data_list: A list of orbit data entries

    Error Handling:
        If an epoch value cannot be converted to a datetime object, logs an error and skips that entry.
        If no valid epochs are found, logs an error and returns None.

    Returns:
        The key of the orbit data entry with the closest epoch to the current time.
    """
    current_time = datetime.now(timezone.utc)

    closest_key = None
    smallest_diff = None

    for key, entry in data_dict.items():

        try:
            epoch_dt = datetime.strptime(entry.epoch, "%Y-%jT%H:%M:%S.%fZ")
            epoch_dt = epoch_dt.replace(tzinfo=timezone.utc)
        except ValueError as e:
            print(f"WARNING: Skipping invalid epoch '{entry.epoch}': {e}")
            continue

        diff = abs((epoch_dt - current_time).total_seconds())
        if smallest_diff is None or diff < smallest_diff:
            smallest_diff = diff
            closest_key = key

    if closest_key is None:
        print("ERROR: No valid epochs found after parsing all state vectors.")
        return None

    return closest_key

def print_orbit_data():
    """
    Iterates through the list of orbit data entries and prints the data for the entry with the closest epoch to the current time, including the calculated speed.

    Args:
        orbit_data_list: A list of orbit data entries

    Error Handling:
        If no valid epochs are found, logs an error and returns 0.
    Returns:
        The state vector data for the entry with the closest epoch to the current time, including the calculated speed, is printed to the console.
    """

    closest_key = find_closest_epoch(orbit_data_list)
    if closest_key is None:
        print("ERROR: Cannot print orbit data because no valid epoch was found.")
        return 0

    entry = orbit_data_list[closest_key]

    print(f"State Vector closest to current time (index {closest_key}):")
    print(f"Epoch: {entry.epoch}")
    print(f"Position (km): X={entry.x}, Y={entry.y}, Z={entry.z}")
    print(f"Velocity (km/s): X_DOT={entry.x_dot}, Y_DOT={entry.y_dot}, Z_DOT={entry.z_dot}")
    print(f"Calculated Speed (km/s): {entry.speed:.2f}")
    print(f"Timestamp (Time when program was ran): {entry.timestamp}")
    print("-" * 40)

def main():
    print_epoch_range()
    print_orbit_data()
    return 0

if __name__ == "__main__":
    main()
