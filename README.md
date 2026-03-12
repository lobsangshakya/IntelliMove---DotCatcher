# 🎮 DotCatcher - Real-Time Kafka Game

A beginner-friendly real-time dot catching game built with Kafka, Flask-SocketIO, and React.

## 🚀 Quick Start (One Command!)

```bash
npm run dev
```

That's it! This single command will start:
- Zookeeper
- Kafka
- Backend WebSocket Server (Flask + SocketIO)
- Dot Generator
- Frontend React App

Then open **http://localhost:3000** in your browser!

## 📋 What You'll See

1. A **5x5 grid** game board
2. **5-7 red dots** appearing randomly on the grid
3. Real-time score tracking
4. WebSocket connection status indicator
5. Event logs showing real-time activity

## 🏗️ System Architecture

```
dot-generator
      ↓
Kafka Topic "dots"
      ↓
backend-server (Kafka Consumer)
      ↓
Flask-SocketIO emit
      ↓
Frontend WebSocket client
      ↓
React grid renders dots
```

## 🛠️ Tech Stack

- **Message Broker**: Apache Kafka + Zookeeper
- **Backend**: Python Flask + Flask-SocketIO
- **Frontend**: React + Vite
- **Communication**: WebSocket (Socket.IO)
- **Containerization**: Docker + Docker Compose

## 📦 Project Structure

```
IntelliMove/
├── dot_catcher/backend/
│   ├── server.py          # Flask + SocketIO server
│   ├── dot_generator.py   # Kafka producer (generates 5-7 dots)
│   ├── requirements.txt   # Python dependencies
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── App.jsx        # Main React component
│   │   ├── App.css        # Styles
│   │   └── main.jsx       # React entry point
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml      # Service orchestration
└── package.json           # Root package.json with npm scripts
```

## 🔧 Commands

### Start Everything
```bash
npm run dev
```

### Stop Everything
```bash
npm run stop
```

### Clean Up (Remove Volumes)
```bash
npm run clean
```

## 🎯 How to Play

1. Open your browser and navigate to: **http://localhost:3000**
2. Dots will randomly appear on the 5x5 grid as red circles
3. Click on dots quickly to catch them before they disappear (3 seconds)
4. Track your progress with the score counter
5. Win by reaching 10 points before missing 5 dots
6. Use the "Reset Game" button to start over

### Game Controls
- **Mouse Click**: Catch a dot
- **Reset Button**: Restart the game
- **Event Logs**: Real-time activity feed

## 🎮 Game Rules

- **Goal**: Catch as many dots as possible
- **Win**: Reach 10 points
- **Lose**: Miss 5 dots
- Dots disappear after 3 seconds if not caught

## 🔍 Technical Details

### Kafka Event Schema

**Dots Topic** (`dots`):
```json
{
  "event_type": "dot_appeared",
  "position": [x, y],
  "timestamp": "ISO_TIMESTAMP"
}
```

**Actions Topic** (`actions`):
```json
{
  "event_type": "dot_caught",
  "position": [x, y],
  "timestamp": "ISO_TIMESTAMP"
}
```

### WebSocket Communication

- **Incoming Events**:
  - `catch_dot`: User action when clicking a dot
  - `reset_game`: Reset game to initial state
  
- **Outgoing Events**:
  - `dot_appeared`: New dot appears on grid
  - `game_state_update`: Score/miss updates
  - `game_over`: Win/lose condition reached
  - `game_reset`: Game restart notification

### Service Ports

| Service | Port | Description |
|---------|------|-------------|
| Zookeeper | 2181 | Kafka coordination |
| Kafka | 9092 | Message broker |
| Backend Server | 5001 | Flask + SocketIO |
| Frontend | 3000 | React dev server |

## 🐛 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Free up ports
   docker compose down --remove-orphans
   ```

2. **Kafka Not Starting**
   ```bash
   # Wait longer - Kafka takes ~30 seconds to start
   # The system has automatic retry logic
   docker compose logs -f kafka
   ```

3. **Frontend Not Loading**
   ```bash
   # Check if all containers are running
   docker ps
   
   # View frontend logs
   docker compose logs -f frontend
   ```

4. **No Dots Appearing**
   ```bash
   # Check dot generator logs
   docker compose logs -f dot-generator
   
   # Check backend logs
   docker compose logs -f backend-server
   ```

### View All Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f backend-server
docker compose logs -f dot-generator
docker compose logs -f frontend
```

### Reset Everything

```bash
# Complete reset
npm run clean
npm run dev
```

## 📝 Notes

- This is a **demo** that generates only 5-7 dots
- Services have automatic retry logic for Kafka connections
- Health checks ensure proper startup order
- Hot reload enabled for development
- Docker handles all dependency management

## 🤝 Contributing

This is a learning project. Feel free to experiment!

## 📄 License

MIT
