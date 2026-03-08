# nasa-iss-tracker → fastapi application
![Python](https://img.shields.io/badge/python-3.10+-magenta?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-TACC-orange)
![System](https://img.shields.io/badge/System-Lonestar6-lightblue)
![Course](https://img.shields.io/badge/COE-332-black)

## Description:
Below are descriptions of each file within this project folder
### [Dockerfile](Dockerfile)
- Contains instructions for building and running the image/container used to run the files below
### [diagram.png](diagram.png)
- Software diagram demonstrating the interaction of a localhost machine to access and run the fastapi app through TACC servers
### [docker-compose.yml](docker-compose.yml)
- Allows for multi-container utility, making all docker containers run as one cohesive unit
### [main.py](main.py)
- Fastapi app file with multiple routes allowing for web functionality of the following 2 files
### [iss_tracker.py](iss_tracker.py)
- Downloads and reads XML data from the ISS Trajectory Data webpage to output the state vector including the epoch timestamp, position and velocity fields, calculated speed, and the time at which the program was ran
### [test_iss_tracker.py](test_iss_tracker.py) 
- Uses unit tests to test each of the functions given in iss_tracker.py

## Installation 
All necessary dependencies and data should be installed by simply running the containerized program via docker build

## Usage

### Dockerfile

- Build the Docker image
  ```bash
  docker run --name "api" -d -p 8000:8000 casyeh/coe332sp26-fastapi:1.0

- Ensure things are running via
  ```bash
  docker ps -a

- Curl usage on your local host
  ```bash
  # Return entire data set
  curl localhost:8000/epochs

  # Return modified list of Epochs given query parameters
  curl localhost:8000/epochs?limit=int&offset=int

  # Return state vectors for a specific Epoch from the data set
  curl localhost:8000/epochs/{epoch}

  # Return instantaneous speed for a specific Epoch in the data set
  curl localhost:8000/epochs/{epoch}/speed

  # Return state vectors and instantaneous speed for the Epoch that is nearest to the current time
  curl localhost:8000/now

- Web access will be handled and streamlined by simple usage of fastapi
  
- Running the main and unit test scripts
  ```bash
  # Main script
  uv run python /code/iss_tracker.py

  # Test script
  uv run python /code/test_iss_tracker.py
  ```
- Note: The container run command can be reduced by using docker-compose.yml with the following command in the directory of the correct Dockerfile
  ```bash
  docker compose up
  
### iss_tracker.py
Expected outputs will be the range of epochs from earliest to most recent timestamps in addition to a state vector containing; epoch timestamp, position and velocity fields, calculated speed, and the time at which the program was ran

### test_iss_tracker.py
Expect outputs will be nothing for the respective assert statements, and a pytest test session output based on the functions given in iss_tracker.py and the following developer given data set

```python
    xml_data = """
    <data>
        <epoch>2024-06-01T00:00:00Z</epoch>
        <epoch>2024-06-01T00:10:00Z</epoch>
        <epoch>2024-06-01T00:20:00Z</epoch>
    </data>
    """
```
