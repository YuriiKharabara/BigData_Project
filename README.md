
# Big Data Project: Wikipedia

## Overview

The Big Data Project's  aim is the real-time analysis of Wikipedia's page creation events. 
Utilizing Apache Spark and Apache Cassandra, the project showcases streaming and batch data processing to provide statistics and on-demand data access through RESTful APIs.

## Project Structure

```plaintext
BigData_Project/
├── docs/           # Documentation and architectural design documents
└── src/            # Source code for the application and APIs



- **docs/**: Contains documentation and design documents.
- **scripts/**: Contains scripts for data ingestion and processing.
- **src/**: Contains the source code for the project.


```

## Setup Instruction

```bash
Initial steps:
      git clone https://github.com/YuriiKharabara/BigData_Project.git
      cd BigData_Project

b) Category B:
      1. cd  category_b
      2. docker-compose up -d # Start api and executor containers
      2. docker cp init.cql cassandra:/init.cql
         docker exec -it cassandra cqlsh -f /init.cql # Create cassandra tables
      3. docker-compose exec spark-master spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,com.datastax.spark:spark-cassandra-connector_2.12:3.0.0 load.py # Start data processing and write to cassandra tables
      4. Service is available on 'http://localhost:8000/docs' # Access the endpoins

```

