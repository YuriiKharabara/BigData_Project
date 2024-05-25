
# BigData_Project

## Project Structure

```
project/
├── data/           # Data models and schemas
├── docs/           # Documentation and design documents
├── scripts/        # Scripts for data ingestion and processing
└── src/            # Source code directory
```


- **data/**: Contains data.
- **docs/**: Contains documentation and design documents.
- **scripts/**: Contains scripts for data ingestion and processing.
- **src/**: Contains the source code for the project.

## Setup Instruction

```bash
git clone https://github.com/YuriiKharabara/BigData_Project.git
cd BigData_Project

b) Category B:
  1. cd  category_b
  2. docker cp init.cql cassandra:/init.cql
      docker exec -it cassandra cqlsh -f /init.cql
  3. docker-compose exec spark-master spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,com.datastax.spark:spark-cassandra-connector_2.12:3.0.0 load.py
  4. Service is available on 'http://localhost:8000/docs'

```

