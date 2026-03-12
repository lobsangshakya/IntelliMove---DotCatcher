#!/bin/bash

echo "🛑 DotCatcher - Stopping All Services..."
echo ""

# Stop all services
docker compose down --remove-orphans

echo ""
echo "✅ All services stopped!"
echo ""
echo "📋 Next steps:"
echo "  • Start again: npm run dev"
echo "  • Clean volumes: docker compose down -v"
echo ""
