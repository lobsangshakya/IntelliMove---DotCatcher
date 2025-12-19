#!/bin/bash

# Dot Catcher Game Stop Script

echo "🛑 Stopping Dot Catcher Game..."

# Function to kill processes
cleanup() {
    echo "🧹 Cleaning up..."
    pkill -f "zookeeper-server-start" 2>/dev/null
    pkill -f "kafka-server-start" 2>/dev/null
    pkill -f "dot_generator.py" 2>/dev/null
    pkill -f "server.py" 2>/dev/null
    pkill -f "game_tracker.py" 2>/dev/null
    pkill -f "npm run dev" 2>/dev/null
    pkill -f "start_game.sh" 2>/dev/null
    sleep 2
    echo "✅ All services stopped."
}

# Cleanup processes
cleanup