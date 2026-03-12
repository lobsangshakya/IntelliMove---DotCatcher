# 🎮 DotCatcher - START HERE!

Welcome to the DotCatcher project! This is your complete guide to getting started.

## ⚡ Quick Start (30 Seconds)

### Prerequisites
- Docker Desktop installed and running
- Node.js 16+ installed

### Start the Game

```bash
npm run dev
```

That's it! Then open **http://localhost:3000** in your browser.

## 📚 Documentation Menu

Choose based on your needs:

### 🚀 Want to start immediately?
→ Read **[QUICKSTART.md](QUICKSTART.md)** (1 minute read)

### 🎯 Want complete documentation?
→ Read **[README.md](README.md)** (5 minute read)

### 📖 Want detailed walkthrough?
→ Read **[PROJECT_GUIDE.md](PROJECT_GUIDE.md)** (10 minute read)

### 🏗️ Want architecture details?
→ Read **[SYSTEM_OVERVIEW.md](SYSTEM_OVERVIEW.md)** (15 minute read)

### ✅ Want to verify everything works?
→ Read **[CHECKLIST.md](CHECKLIST.md)** (reference guide)

## 🎮 What You'll See

When you open http://localhost:3000:

```
┌─────────────────────────────────────┐
│  Dot Catcher           Connected    │
│                        Score: 0     │
├─────────────────────────────────────┤
│                                     │
│   ┌───┬───┬───┬───┬───┐            │
│   │   │   │   │   │   │            │
│   ├───┼───┼───┼───┼───┤   5x5      │
│   │   │ 🔴│   │   │   │   Grid     │
│   ├───┼───┼───┼───┼───┤            │
│   │   │   │   │   │   │            │
│   ├───┼───┼───┼───┼───┤            │
│   │   │   │   │🔴 │   │            │
│   ├───┼───┼───┼───┼───┤            │
│   │   │   │   │   │   │            │
│   └───┴───┴───┴───┴───┘            │
│                                     │
│  Event Logs:                        │
│  • Dot appeared at [2,3]           │
│  • Dot appeared at [1,2]           │
└─────────────────────────────────────┘
```

## 🛠️ All Commands

```bash
# Start everything
npm run dev

# Stop everything
npm run stop

# Clean slate (removes volumes)
npm run clean

# View live logs
npm run logs

# Restart
npm run restart

# Alternative: Use shell scripts
./start.sh
./stop.sh
```

## 🔧 Troubleshooting

### "Cannot connect to Docker"
**Fix**: Make sure Docker Desktop is running

### "Port already in use"
**Fix**: 
```bash
docker compose down --remove-orphans
```

### "Blank screen"
**Fix**: 
1. Wait 30 seconds for startup
2. Check browser console (F12)
3. Verify containers: `docker ps`

### "No dots appearing"
**Fix**: Check logs:
```bash
npm run logs
```

## 📦 What Gets Installed

When you run `npm run dev`, Docker starts:

1. **Zookeeper** - Kafka coordination
2. **Kafka** - Message broker
3. **Backend Server** - Flask + SocketIO (port 5001)
4. **Dot Generator** - Creates 5-7 dots
5. **Frontend** - React app (port 3000)

All services are containerized - no manual installation needed!

## 🎯 How to Play

1. Open http://localhost:3000
2. Wait for dots to appear (red circles)
3. Click dots quickly to catch them
4. Dots disappear after 3 seconds
5. Reach 10 points to win
6. Don't miss 5 dots or you lose!

## 🏗️ System Flow

```
dot-generator → Kafka → backend → WebSocket → frontend → Grid
```

Detailed flow:
1. Dot generator creates random dots
2. Sends to Kafka topic "dots"
3. Backend consumes from Kafka
4. Broadcasts via WebSocket
5. Frontend receives and renders
6. You see dots on the grid!

## 📊 Success Criteria

✅ Single command startup
✅ Works reliably
✅ Clear documentation
✅ Easy to debug
✅ Beginner-friendly
✅ No manual configuration

## 🎓 Learning Resources

### New to Kafka?
- Kafka is a message broker (like a post office for data)
- Topics are like channels (dots, actions)
- Producers send messages
- Consumers receive messages

### New to Docker?
- Docker packages apps in containers
- docker-compose.yml defines all services
- `docker compose up` starts everything
- `docker compose down` stops everything

### New to WebSockets?
- WebSocket = persistent connection between browser and server
- Socket.IO = library that makes WebSockets easy
- Enables real-time updates

## 🤝 Contributing

Feel free to:
- Experiment with code
- Add new features
- Fix bugs
- Improve documentation
- Share feedback

## 📄 License

MIT - Feel free to use, modify, and share!

## 🙋 Need Help?

1. Check the error message
2. Look in documentation
3. Run `npm run logs`
4. Google the error message
5. Ask for help!

## 🎉 Ready to Go!

```bash
npm run dev
```

Then: **http://localhost:3000**

Have fun! 🎮

---

**Quick Links:**
- [QUICKSTART.md](QUICKSTART.md) - Quick reference
- [README.md](README.md) - Full documentation  
- [PROJECT_GUIDE.md](PROJECT_GUIDE.md) - Detailed guide
- [SYSTEM_OVERVIEW.md](SYSTEM_OVERVIEW.md) - Architecture
- [CHECKLIST.md](CHECKLIST.md) - Verification checklist
