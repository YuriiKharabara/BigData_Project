#!/bin/bash
echo Hello
cleanup() {
    echo "Stopping processes..."
    # Stop background processes
    kill $producer_pid $consumer1_pid $consumer2_pid $consumer3_pid
    exit 1
}

# Trap SIGINT and call cleanup function
trap cleanup SIGINT

# Delay and setup commands
sleep 50
docker cp scripts/init.cql cassandra:/init.cql
sleep 10
docker exec -it cassandra cqlsh -f /init.cql

# Start producer and consumers in the background
python producer.py &
producer_pid=$!

python kafka_consumer/consumer_task_1.py &
consumer1_pid=$!

python kafka_consumer/consumer_task_2.py &
consumer2_pid=$!

python kafka_consumer/consumer_task_3.py &
consumer3_pid=$!

# Wait for all processes to finish
wait $producer_pid $consumer1_pid $consumer2_pid $consumer3_pid
