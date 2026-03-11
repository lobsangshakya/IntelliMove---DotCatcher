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

  const [socket, setSocket] = useState(null)

  useEffect(() => {
    addLog('Connecting to WebSocket...')
    console.log('[FRONTEND] Initializing WebSocket connection to http://localhost:5001')
    
    const newSocket = io('http://localhost:5001', {
      transports: ['websocket', 'polling'],
      reconnection: true,
      reconnectionAttempts: 5,
      reconnectionDelay: 1000
    })

    setSocket(newSocket)

    newSocket.on('connect', () => {
      addLog('Connected to server!')
      console.log('[FRONTEND] WebSocket connected successfully')
      setConnected(true)
    })

    newSocket.on('connect_error', (error) => {
      console.error('[FRONTEND] WebSocket connection error:', error)
      addLog('Connection error!')
    })

    newSocket.on('disconnect', (reason) => {
      console.log('[FRONTEND] WebSocket disconnected:', reason)
      addLog('Disconnected: ' + reason)
      setConnected(false)
    })

    newSocket.on('dot_appeared', (data) => {
      console.log('[FRONTEND] dot_appeared event received:', data)
      const dotId = Date.now() + Math.random()
      addLog(`Dot at [${data.position}]`)
      setDots(prev => [...prev, { id: dotId, x: data.position[0], y: data.position[1], timestamp: Date.now() }])
      
      setTimeout(() => {
        setDots(prev => prev.filter(d => d.id !== dotId))
      }, 3000)
    })

    newSocket.on('game_state_update', (state) => {
      console.log('[FRONTEND] game_state_update received:', state)
      setScore(state.score)
    })
    
    newSocket.on('game_over', (data) => {
      console.log('[FRONTEND] game_over event:', data)
      addLog(`Game ${data.result}!`)
    })

    return () => {
      console.log('[FRONTEND] Cleaning up WebSocket connection')
      newSocket.disconnect()
    }
  }, [])

  const handleDotClick = (dot) => {
    addLog(`Clicked dot at [${dot.x}, ${dot.y}]`)
    
    if (socket && connected) {
      socket.emit('catch_dot', {
        event_type: 'dot_caught',
        position: [dot.x, dot.y],
        timestamp: new Date().toISOString()
      })
    }

    // Remove the clicked dot locally immediately for responsiveness
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
