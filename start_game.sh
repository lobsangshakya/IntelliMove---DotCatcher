#!/bin/bash

# Dot Catcher Game Startup Script

echo "🚀 Starting Dot Catcher Game..."

# Function to check if a process is running
is_running() {
    pgrep -f "$1" > /dev/null
}

# Function to kill processes
cleanup() {
    echo "🧹 Cleaning up..."
    pkill -f "zookeeper-server-start" 2>/dev/null
    pkill -f "kafka-server-start" 2>/dev/null
    pkill -f "dot_generator.py" 2>/dev/null
    pkill -f "server.py" 2>/dev/null
    pkill -f "game_tracker.py" 2>/dev/null
    pkill -f "npm run dev" 2>/dev/null
    sleep 2
}

# Cleanup any existing processes
cleanup

# Start Zookeeper
echo "🐘 Starting Zookeeper..."
~/kafka/bin/zookeeper-server-start.sh ~/kafka/config/zookeeper.properties > zookeeper.log 2>&1 &
ZOOKEEPER_PID=$!
sleep 5

# Start Kafka
echo "_typeDefinition Starting Kafka..."
~/kafka/bin/kafka-server-start.sh ~/kafka/config/server.properties > kafka.log 2>&1 &
KAFKA_PID=$!
sleep 10

# Create Kafka topics
echo "📋 Creating Kafka topics..."
~/kafka/bin/kafka-topics.sh --create --topic dots --bootstrap-server localhost:9092 2>/dev/null
~/kafka/bin/kafka-topics.sh --create --topic actions --bootstrap-server localhost:9092 2>/dev/null

# Start Game Tracker
echo "📊 Starting Game Tracker..."
cd dot_catcher/backend
python3 game_tracker.py > ../../game_tracker.log 2>&1 &
TRACKER_PID=$!

# Start Backend Server
echo "🖥️ Starting Backend Server..."
cd ../.. # Back to root
cd dot_catcher/backend
python3 server.py > ../../server.log 2>&1 &
SERVER_PID=$!

# Start Dot Generator
echo "🎯 Starting Dot Generator..."
cd ../.. # Back to root
cd dot_catcher/backend
python3 dot_generator.py > ../../dot_generator.log 2>&1 &
GENERATOR_PID=$!

# Start Frontend
echo "🎨 Starting Frontend..."
cd ../.. # Back to root
cd frontend
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!

echo "🎮 Dot Catcher Game is now running!"
echo "🌐 Frontend: http://localhost:5173"
echo "📡 Backend: http://localhost:5001"
echo ""
echo "Use Ctrl+C to stop all services"

# Wait for processes or handle Ctrl+C
trap 'echo "🛑 Stopping all services..."; cleanup; exit' INT TERM

# Keep script running
while true; do
    sleep 1
done