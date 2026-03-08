from fastapi import FastAPI, HTTPException
from iss_tracker import parse_xml, find_closest_epoch

app = FastAPI()
orbit_data = parse_xml("ISS_OEM_J2K_EPH.xml")

@app.get("/epochs")
def read_epochs(limit: int = None, offset: int = None):
    """
    Reads the ISS orbit data from the XML file and returns a list of epochs with their corresponding state vectors.
    Can be filtered using the 'limit' and 'offset' query parameters to control the number of epochs returned and the starting point in the list.

    Args:
        limit (int, optional): The maximum number of epochs to return. Defaults to None, which means no limit.
        offset (int, optional): The number of epochs to skip before starting to return results. Defaults to None, which means no offset.

    Error Handling:
        If the XML file cannot be read or parsed, an error message will be returned.
        If the 'limit' or 'offset' parameters are invalid (e.g., negative numbers), an error message will be returned.

    Returns:
        dict: A dictionary containing a list of epochs with their corresponding state vectors, or an error message if something goes wrong.
    """
    epochs = list(orbit_data.values())
    if offset is not None:
        epochs = epochs[offset:]
    if limit is not None:
        epochs = epochs[:limit]
    return {"epochs": epochs}

@app.get("/epochs/{epoch}")
def read_epoch(epoch: int):
    """
    Reads the ISS orbit data for a specific epoch from the XML file and returns the corresponding state vector.

    Args:
        epoch (int): The index of the epoch to retrieve.

    Error Handling:
        If the XML file cannot be read or parsed, an error message will be returned.
        If the 'epoch' parameter is invalid (e.g., negative number or out of bounds), an error message will be returned.

    Returns:
        dict: A dictionary containing the state vector for the specified epoch, or an error message if something goes wrong.
    """
    if epoch not in orbit_data:
        raise HTTPException(status_code=404, detail="Epoch not found")
    entry = orbit_data[epoch]
    return orbit_data[epoch]

@app.get("/epochs/{epoch}/speed")
def read_epoch_speed(epoch: int): 
    """
    Reads the ISS orbit data for a specific epoch from the XML file and returns the calculated speed based on the velocity components.

    Args:
        epoch (int): The index of the epoch to retrieve.

    Error Handling:
        If the XML file cannot be read or parsed, an error message will be returned.
        If the 'epoch' parameter is invalid (e.g., negative number or out of bounds), an error message will be returned.

    Returns:
        dict: A dictionary containing the calculated speed for the specified epoch, or an error message if something goes wrong.
    """
    if epoch not in orbit_data:
        raise HTTPException(status_code=404, detail="Epoch not found")
    entry = orbit_data[epoch]
    return {"speed": entry.speed}

@app.get("/now")
def read_now():
    """
    Reads the ISS orbit data for a specific epoch from the XML file that is closest to the current time

    Args:
        None

    Error Handling:
        If the XML file cannot be read or parsed, an error message will be returned.

    Returns:
        dict: A dictionary containing the state vector for the epoch closest to the users current time, or an error message if something goes wrong.
    """
    closest_key = find_closest_epoch(orbit_data)

    if closest_key is None:
        raise HTTPException(status_code=404, detail="No valid epoch found")

    entry = orbit_data[closest_key]

    return entry
