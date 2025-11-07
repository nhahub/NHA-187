#!/bin/bash
echo "🛑 Stopping all SmartComplaint-related services..."

# Stop Spark jobs
echo "Stopping Spark streaming..."
pkill -f 'spark-submit' || echo "No Spark streaming jobs found."

# Stop Kafka brokers
echo "Stopping Kafka..."
pkill -f 'kafka.Kafka' || echo "Kafka not running."

# Stop Zookeeper
echo "Stopping Zookeeper..."
pkill -f 'quorum.QuorumPeerMain' || echo "Zookeeper not running."

# Stop Streamlit
echo "Stopping Streamlit..."
pkill -f 'streamlit' || echo "Streamlit not running."

# Stop Python scripts (any other running project scripts)
echo "Stopping other Python scripts..."
pkill -f 'python' || echo "No other Python scripts running."

# Stop Docker containers (if used)
if command -v docker &> /dev/null
then
    echo "Stopping Docker containers..."
    docker ps -q | xargs -r docker stop
    echo "Removing Docker containers, networks, volumes (optional)..."
    docker system prune -af
    docker volume prune -f
    docker network prune -f
fi

# Clean temporary Spark checkpoints
echo "Cleaning Spark checkpoints..."
rm -rf ./checkpoints/* || echo "No checkpoints to clean."

# Clean Kafka logs (optional, start fresh next time)
echo "Cleaning Kafka logs..."
rm -rf /tmp/kafka-logs || echo "No Kafka logs found."

# Clean Zookeeper data (optional)
echo "Cleaning Zookeeper data..."
rm -rf /tmp/zookeeper || echo "No Zookeeper data found."

# Clean Python caches and logs
echo "Cleaning Python caches and logs..."
find . -name "__pycache__" -type d -exec rm -rf {} +
find . -name "*.pyc" -type f -delete
rm -rf logs/*.log || echo "No logs to clean."

echo "✅ All services stopped and cleaned. Environment is fresh."
# Stop Kafdrop
pkill -f 'kafdrop' || echo "Kafdrop not running."
