# BigData_Project

## Project Structure

```
my_project/
├── config/         # Configuration files
├── data/           # Data models and schemas
├── docs/           # Documentation and design documents
├── scripts/        # Scripts for data ingestion and processing
└── src/            # Source code directory
```

- **config/**: Contains configuration files for the project.
- **data/**: Contains data.
- **docs/**: Contains documentation and design documents.
- **scripts/**: Contains scripts for data ingestion and processing.
- **src/**: Contains the source code for the project.

## Setup Instruction

```bash
git clone https://github.com/YuriiKharabara/BigData_Project.git
cd BigData_Project
```


## TODO List

### 1. Setup Project Environment
- [x] **Initialize Git Repository**
- [x] **Create Project Structure**
- [x] **Create README.md**
  - [x] Write project structure description.
  - [x] Write setup instructions.

### 2. Implement Data Source Integration
- [ ] **Connect to Wikipedia Stream**
  - [ ] Write a script to connect to the Wikipedia page creation stream.
  - [ ] Parse JSON data from the stream.
- [ ] **Store Data in Database** (Think about schemas and DB)

### 3. Setup Databases with Docker
- [ ] **Install and Configure with Docker**
  - [ ] Write a Dockerfile.
  - [ ] Write a `docker-compose.yml` to manage the services.
- [ ] **Define Data Models**
  - [ ] Create tables.

### 4. Implement Batch Processing with Spark
- [ ] **Write Spark Jobs**
  - [ ] Compute statistics for the number of pages created per domain per hour.
  - [ ] Compute statistics for pages created by bots per domain.
  - [ ] Identify top 20 users by page creation.
- [ ] **Schedule Batch Jobs**
  - [ ] Set up Apache Airflow or ?.
  - [ ] Schedule batch jobs to run every hour.

### 5. Implement Streaming Processing with Spark Streaming
- [ ] **Set Up Spark Streaming**
  - [ ] Configure Spark Streaming to process real-time data.
  - [ ] Implement real-time data processing logic.
  - [ ] Continuously update DB with streaming data.

### 6. Develop REST APIs
- [ ] **Set Up API Framework**
  - [ ] set up Flask or FastAPI.
- [ ] **Implement Category A APIs**
  - [ ] Implement `/api/reports/created-pages` endpoint.
  - [ ] Implement `/api/reports/pages-created-by-bots` endpoint.
  - [ ] Implement `/api/reports/top-users` endpoint.
- [ ] **Implement Category B APIs**
  - [ ] Implement `/api/domains` endpoint.
  - [ ] Implement `/api/user-pages/{user_id}` endpoint.
  - [ ] Implement `/api/domain-articles/{domain}` endpoint.
  - [ ] Implement `/api/page/{page_id}` endpoint.
  - [ ] Implement `/api/users` endpoint.
- [ ] **Test APIs**
  - [ ] Write and run tests for each endpoint to ensure correct functionality.

### 7. Documentation and Finalization
- [ ] **Write Detailed Design Document**
  - [ ] Describe architecture overview.
  - [ ] Explain design decisions.
  - [ ] Detail each system component.
- [ ] **Create Data Model Diagrams**
  - [ ] Draw and include diagrams for data models in the documentation.
- [ ] **Run System for Testing**
  - [ ] Run the system for at least 4 hours.
  - [ ] Collect example results for API calls.
- [ ] **Ensure Code Quality**
  - [ ] Document all source code.
  - [ ] Clean and organize the codebase.
