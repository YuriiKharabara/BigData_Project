## System Overview: Category A

Choose Cassandra DB for its features, which are well-suited to both streaming and batch-processing applications in real life.

Here are the key advantages that impacted this choice:

1. **Flexible Data Storage:** Ideal for environments that must handle both streaming inputs and batch data, allowing the adjustment of the data schema.
2. **High Availability and Write Performance:** Essential for achieving throughput in scenarios with heavy real-time write loads.
3. **Scalability:** Ensures that the system can efficiently manage increasing volumes of data without any single point of failure.

### Precomputed Report Support: Category A

- **a)** Hourly aggregated statistics: Return the aggregated statistics containing the number of created pages for each Wikipedia domain for each hour in the last `n` hours, excluding the last hour.
- **b)** Bot-created pages statistics: Return the statistics about the number of pages created by bots for each of the domains for the last `n` hours, excluding the last hour.
- **c)** Top users by page creation: Return the top 20 users that created the most pages during the last `n` hours, excluding the last hour. The response should contain the user name, user ID, start and end time, the list of page titles, and the number of pages created.

### Data Models Description: Category A

**a) hourly_stats**
- **Reason:** Store the aggregated statistics of created pages for each Wikipedia domain per hour.
- **Primary Key:** Composite of `hour_start` (partition key) and `domain` (clustering key).

| Column      | Role              | Type      |
|-------------|-------------------|-----------|
| hour_start  | Partition Key     | TIMESTAMP |
| domain      | Clustering Key    | TEXT      |
| hour_end    |                   | TIMESTAMP |
| page_count  |                   | INT       |

**b) bot_stats**
- **Reason:** Track the number of pages created by bots for each domain within a specified time range.
- **Primary Key:** Composite of `time_start` (partition key) and `domain` (clustering key).

| Column         | Role              | Type      |
|----------------|-------------------|-----------|
| time_start     | Partition Key     | TIMESTAMP |
| domain         | Clustering Key    | TEXT      |
| time_end       |                   | TIMESTAMP |
| created_by_bots|                   | INT       |

**c) user_stats**
- **Reason:** Store detailed information about each page created by users, allowing for quick lookups and aggregations by user.
- **Primary Key:** Composite of `user_id` (partition key) and `creation_time` (clustering key).

| Column        | Role              | Type      |
|---------------|-------------------|-----------|
| user_id       | Partition Key     | TEXT      |
| creation_time | Clustering Key    | TIMESTAMP |
| user_name     |                   | TEXT      |
| page_title    |                   | TEXT      |
