#!/bin/bash

echo "🎮 DotCatcher - Starting All Services..."
echo ""
echo "This will start:"
echo "  • Zookeeper"
echo "  • Kafka"
echo "  • Backend WebSocket Server"
echo "  • Dot Generator"
echo "  • Frontend React App"
echo ""
echo "⏱️  Note: Kafka may take ~30 seconds to fully start"
echo ""

# Start all services with Docker Compose
docker compose up --build

echo ""
echo "✅ All services started!"
echo ""
echo "🌐 Open your browser to: http://localhost:3000"
echo ""
echo "📋 Useful commands:"
echo "  • View logs: docker compose logs -f"
echo "  • Stop services: docker compose down"
echo "  • Clean everything: docker compose down -v --remove-orphans"
echo ""
