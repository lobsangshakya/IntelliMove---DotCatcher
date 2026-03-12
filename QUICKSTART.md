# ⚡ Quick Start Guide

## 🚀 Start in 3 Seconds

```bash
npm run dev
```

That's it! Then open **http://localhost:3000**

## 🎮 What to Expect

1. **5x5 grid** appears on screen
2. **5-7 red dots** pop up randomly
3. Click dots to catch them
4. Score updates in real-time
5. Event logs show activity

## 🛑 Other Commands

```bash
# Stop everything
npm run stop

# Clean slate (removes volumes)
npm run clean

# View live logs
npm run logs

# Restart
npm run restart
```

## 🐛 Troubleshooting

### "Port already in use"
```bash
docker compose down --remove-orphans
```

### "Cannot connect to Docker"
Make sure Docker Desktop is running

### Kafka taking too long
Wait ~30 seconds - Kafka needs time to start. Check logs:
```bash
docker compose logs -f kafka
```

### Blank screen
Check browser console (F12) for errors

## 📖 Need More Help?

See the full [README.md](README.md) or [PROJECT_GUIDE.md](PROJECT_GUIDE.md)
