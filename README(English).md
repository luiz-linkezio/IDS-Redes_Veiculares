# Vehicular Network IDS

This repository was created with the objective of developing Intrusion Detection Systems (IDS) for vehicular networks, specifically for networks using the CAN protocol and networks using the Ethernet protocol, so that these IDSs can be tested in controlled environments and produce results.

## Directory/File Organization

The directory:
 - `requirements` contains the requirements needed to run the project code.
 - `CAN` contains all the work done for CAN networks.
 - `Ethernet` contains all the work done for Ethernet networks.
 - `CAN/data` or `Ethernet/data` contains the data collected for the respective protocol, which was later used for training, validation and testing of the artificial intelligence models.
 - `CAN/models` or `Ethernet/models` contains the trained artificial intelligence models and their respective scalers for the respective protocol.
 - `CAN/Training_the_AI_model(s)_with_Python.ipynb` or `Ethernet/Training_the_AI_model(s)_with_Python.ipynb` are Jupyter notebook files with Python code responsible for training, validating and testing AI models for the respective protocol.
 - `Ethernet/Process_PCAPNG.py` is a Python file responsible for processing PCAPNG files, essentially performing data cleaning and standardization.
 - `CAN/Random_Message_Generator.py` is a Python file responsible for generating random CAN messages.
 - `CAN/CSV_Processing_CAN.py` is a Python file responsible for processing CAN messages from a CSV file, essentially performing data cleaning and standardization.
 - `CAN/Bus_Scripts` is a folder containing scripts to collect (`Message_Collector.py`) CAN messages, attack (`Attacks.py`) a CAN bus and deploy the IDS (`IDS.py`) on real physical CAN buses (even if in controlled environment).
 - `docs` is a folder containing the project reports, including the results.

## Results 

### CAN

[CAN Results](docs/Resultados_CAN.pdf)

### Ethernet 

[Ethernet Results](docs/Resultados_Ethernet.pdf)
