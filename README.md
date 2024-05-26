
# Big Data Project: Wikipedia

## Overview

The Big Data Project's  aim is the real-time analysis of Wikipedia's page creation events. 
Utilizing Apache Spark and Apache Cassandra, the project showcases streaming and batch data processing to provide statistics and on-demand data access through RESTful APIs.

## Authors

- [Yurii Kharabara](https://github.com/YuriiKharabara)
- [Anastasiia Petrovych](https://github.com/nastiapetrovych)

## Architecture for Category-A
![image](https://github.com/YuriiKharabara/BigData_Project/assets/92577132/d61e8ee1-9fb1-4706-bc45-844a538e815a)

More detailed info can be found in [`docs/category_a_system_overview.md`](docs/category_a_system_overview.md).


## Architecture for Category-B
![image](https://github.com/YuriiKharabara/BigData_Project/assets/92577132/79feafa7-473f-4f2a-8422-97136b0fc553)

More detailed info can be found in [`docs/category_b_data_models.txt`](docs/category_b_data_models.txt).


## Project Structure



## Directory and File Descriptions

- **`src/`**: This directory contains all source code for the project.
  - **`category_a/`**: Specific configurations and scripts for Category A:
    
    - **`src/`**: Contains all source code for category_a.
       - **`cassandra_config.py`**: Manages database configuration for Cassandra.
       - **`handle_generic_exceptions.py`**: Provides centralized exception handling.
       - **`kafka_config.py`**: Manages Kafka configuration.
       - **`main.py`**: Entry point for the FastAPI application.
       - **`router.py`**: Defines API routes.
       - **`service.py`**: Implements the logic associated with each API endpoint.
    - **`docker-compose.yml`**: Manages Docker services, networks, and volumes for Category A.
    - **`Dockerfile.api`**: Configures the Docker container for the API service in Category A.
    - **`kafka_consumer/`**: Contains Kafka consumer scripts for different tasks.
       - **`consumer_task_1.py`**: Consumer script for task 1.
       - **`consumer_task_2.py`**: Consumer script for task 2.
       - **`consumer_task_3.py`**: Consumer script for task 3.
    - **`producer.py`**: Kafka producer script.
    - **`requirements.txt`**: Necessary Python packages for Category A.
    - **`response.py`**: Handles API responses.
    - **`scripts/`**: Contains scripts for service management.
       - **`init.cql`**: Contains CQL commands to initialize the Cassandra database schema for Category A.
       - **`start_services.sh`**: Script to start services.
       - **`stop_services.sh`**: Script to stop services.
         
  - **`category_b/`**: Specific configurations and scripts for Category B:
    
    - **`src/`**: Contains all source code for category_b.
       - **`cassandra_db.py`**: Manages database sessions and queries for Cassandra.
       - **`constants.py`**: Stores configuration constants that are used across the application.
       - **`extractor.py`**: Script for extracting data from streaming sources.
       - **`handle_generic_exceptions.py`**: Provides a centralized exception handling.
       - **`main.py`**: Entry point for the  FastAPI.
       - **`router.py`**: Defines API routes.
       - **`service.py`**: Implements the logic associated with each API endpoint. 
    - **`Dockerfile.api`**: Configures the Docker container for the API service.
    - **`Dockerfile.extractor`**: Sets up the Docker container for the data extraction service.
    - **`docker-compose.yml`**: Manages Docker services, networks, and volumes.
    - **`init.cql`**: Contains CQL commands to initialize the Cassandra database schema.
    - **`load.py`**: Executes data processing using Spark, interacting with Kafka and Cassandra.
    - **`requirements.txt`**:  Necessary Python packages.

- **`data/`**: Stores schemas and data models that define the structure and integrity of the database.

- **`docs/`**: Holds all documentation, including setup guides and detailed design documents.

- **`scripts/`**: Includes scripts that facilitate database setup, data ingestion, and other maintenance tasks.

## Setup and Operation

Follow the instructions in `README.md` for detailed steps on setting up and running the project. Ensure you have Docker and other necessary tools installed as per the requirements listed in `requirements.txt`.



```bash

## Setup Instruction


Initial steps:
      git clone https://github.com/YuriiKharabara/BigData_Project.git
      cd BigData_Project
a) Category A:
      1. cd  src/category_a
      2. docker-compose up -d # Start api and executor containers
      2. pip install -r requirements.txt
      3. bash ./scripts/start_services.sh # Start producer and consumers. As a result you can find fullfilled table (Within the next full hour.)
      4. Service is available on 'http://localhost:8000/docs' # Access the endpoins
b) Category B:
      1. cd  src/category_b
      2. docker-compose up -d # Start api and executor containers
      2. docker cp init.cql cassandra:/init.cql
         docker exec -it cassandra cqlsh -f /init.cql # Create cassandra tables
      3. docker-compose exec spark-master spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,com.datastax.spark:spark-cassandra-connector_2.12:3.0.0 load.py # Start data processing and write to cassandra tables
      4. Service is available on 'http://localhost:8000/docs' # Access the endpoins

```

## Results
## Results

### Category A

The Category A system was run for 4 hours. The results for the various API calls can be found in the `category_a` directory.

- **Hourly Aggregated Statistics:** Results for different time ranges (`n` = 0, 1, 3, and 6 hours).
- **Bot-created Pages Statistics:** Results for different time ranges (`n` = 0, 1, and 3 hours).
- **Top Users by Page Creation:** Results for different time ranges (`n` = 0, 1, 3, and 6 hours).

More detailed info can be found in [`results/category_a/README.md`](results/category_a/README.md).

### Category B

The Category B system handles ad-hoc queries for various statistics. The results for these queries can be found in the `category_b` directory.

- **Get Articles by Domain:** Number of articles for different domains.
- **Get Domains:** List of all existing domains.
- **Get Page by ID:** Detailed information for pages identified by their IDs.
- **Get Pages by User ID:** List of pages created by specific users.
- **Get Users:** Summary of user activity within specified time ranges.

More detailed info can be found in [`results/category_b/README.md`](results/category_b/README.md).
