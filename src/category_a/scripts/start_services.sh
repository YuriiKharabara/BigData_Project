#!/bin/bash
echo Hello
cleanup() {
    echo "Stopping processes..."
    # Stop background processes
    kill $producer_pid $consumer1_pid $consumer2_pid $consumer3_pid
    exit 1
}

# Trap SIGINT and call cleanup function (handle Ctrl+C)
trap cleanup SIGINT

sleep 50
docker cp scripts/init.cql cassandra:/init.cql
sleep 10
docker exec -it cassandra cqlsh -f /init.cql

# Start producer and consumers In the background
python producer.py &
producer_pid=$!

python kafka_consumer/consumer_task_1.py &
consumer1_pid=$!

python kafka_consumer/consumer_task_2.py &
consumer2_pid=$!

python kafka_consumer/consumer_task_3.py &
consumer3_pid=$!

wait $producer_pid $consumer1_pid $consumer2_pid $consumer3_pid
