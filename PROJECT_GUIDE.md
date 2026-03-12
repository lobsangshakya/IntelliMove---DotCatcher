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

## 🎯 How It Works

1. **Dot Generator** creates 5-7 dots and sends them to Kafka topic "dots"
2. **Backend Server** consumes dots from Kafka and broadcasts via WebSocket
3. **Frontend** receives dot events and renders them on a 5x5 grid
4. **User** clicks dots to catch them
5. **Score** updates in real-time

## 🐛 Troubleshooting

### Port Already in Use
If you see port conflicts:
```bash
# Free up ports
docker compose down --remove-orphans
```

### Kafka Connection Issues
Wait a bit longer - Kafka takes ~30 seconds to fully start up. The system has retry logic built-in.

### Blank Screen
Check browser console for errors. Ensure all containers are running:
```bash
docker ps
```

### View Logs
```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f backend-server
docker compose logs -f dot-generator
docker compose logs -f frontend
```

## 🎮 Game Rules

- **Goal**: Catch as many dots as possible
- **Win**: Reach 10 points
- **Lose**: Miss 5 dots
- Dots disappear after 3 seconds if not caught

## 📝 Notes

- This is a **demo** that generates only 5-7 dots
- Services have automatic retry logic for Kafka connections
- Health checks ensure proper startup order
- Hot reload enabled for development

## 🤝 Contributing

This is a learning project. Feel free to experiment!

## 📄 License

MIT
