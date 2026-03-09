import { useState, useEffect } from 'react'
import io from 'socket.io-client'
import './App.css'

function App() {
  const [dots, setDots] = useState([])
  const [score, setScore] = useState(0)
  const [connected, setConnected] = useState(false)
  const [logs, setLogs] = useState([])

  const addLog = (message) => {
    setLogs(prev => [...prev.slice(-4), `${new Date().toLocaleTimeString()}: ${message}`])
    console.log(message)
  }

  useEffect(() => {
    addLog('Connecting to WebSocket...')
    console.log('[FRONTEND] Initializing WebSocket connection to http://localhost:5001')
    
    const socket = io('http://localhost:5001', {
      transports: ['websocket', 'polling'],  // Try websocket first, fallback to polling
      reconnection: true,
      reconnectionAttempts: 5,
      reconnectionDelay: 1000
    })

    socket.on('connect', () => {
      addLog('Connected to server!')
      console.log('[FRONTEND] WebSocket connected successfully')
      setConnected(true)
    })

    socket.on('connect_error', (error) => {
      console.error('[FRONTEND] WebSocket connection error:', error)
      addLog('Connection error!')
    })

    socket.on('disconnect', (reason) => {
      console.log('[FRONTEND] WebSocket disconnected:', reason)
      addLog('Disconnected: ' + reason)
      setConnected(false)
    })

    socket.on('dot_appeared', (data) => {
      console.log('[FRONTEND] dot_appeared event received:', data)
      const dotId = Date.now() + Math.random()  // Ensure unique ID
      addLog(`Dot at [${data.position}]`)
      setDots(prev => [...prev, { id: dotId, x: data.position[0], y: data.position[1], timestamp: Date.now() }])
      
      // Remove this specific dot after 3 seconds
      setTimeout(() => {
        setDots(prev => prev.filter(d => d.id !== dotId))
      }, 3000)
    })

    socket.on('game_state_update', (state) => {
      console.log('[FRONTEND] game_state_update received:', state)
      setScore(state.score)
    })
    
    socket.on('game_over', (data) => {
      console.log('[FRONTEND] game_over event:', data)
      addLog(`Game ${data.result}!`)
    })

    return () => {
      console.log('[FRONTEND] Cleaning up WebSocket connection')
      socket.disconnect()
    }
  }, [])

  const handleDotClick = (dot) => {
    addLog(`Clicked dot at [${dot.x}, ${dot.y}]`)
    // Remove the clicked dot
    setDots(prev => prev.filter(d => d.id !== dot.id))
  }

  return (
    <div className="app">
      <header className="header">
        <h1>Dot Catcher</h1>
        <div className="stats">
          <span className={`status ${connected ? 'connected' : 'disconnected'}`}>
            {connected ? 'Connected' : 'Disconnected'}
          </span>
          <span className="score">Score: {score}</span>
        </div>
      </header>

      <main className="game-container">
        <div className="grid">
          {Array.from({ length: 5 }, (_, row) => (
            <div key={row} className="row">
              {Array.from({ length: 5 }, (_, col) => {
                const dot = dots.find(d => d.x === row && d.y === col)
                return (
                  <div key={col} className="cell">
                    {dot && (
                      <div 
                        className="dot"
                        onClick={() => handleDotClick(dot)}
                      />
                    )}
                  </div>
                )
              })}
            </div>
          ))}
        </div>
      </main>

      <aside className="logs">
        <h3>Event Logs</h3>
        {logs.map((log, i) => (
          <div key={i} className="log-line">{log}</div>
        ))}
      </aside>
    </div>
  )
}

export default App
