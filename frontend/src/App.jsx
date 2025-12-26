import React, { useState, useEffect, useRef } from 'react';
import './App.css';
import io from 'socket.io-client';

function App() {
  const GRID_SIZE = 5;
  const [grid, setGrid] = useState(Array(GRID_SIZE).fill().map(() => Array(GRID_SIZE).fill(false)));
  const [score, setScore] = useState(0);
  const [misses, setMisses] = useState(0);
  const [gameOver, setGameOver] = useState(false);
  const [gameResult, setGameResult] = useState(null);
  const [targetScore] = useState(10);
  const [maxMisses] = useState(5);
  const socketRef = useRef(null);
  const dotTimeoutsRef = useRef(new Map()); // Track timeouts for each dot
  const animationFrameRef = useRef(null); // Track animation frames
  const activeAnimationsRef = useRef(new Map()); // Track active animations

  // Single animation loop that handles all dots using requestAnimationFrame
  const animateAllDots = () => {
    const now = Date.now();
    const dotsToRemove = [];
    
    // Iterate through active animations to see which ones need to be removed
    activeAnimationsRef.current.forEach((animation, dotId) => {
      const { x, y, startTime, duration } = animation;
      if (now - startTime >= duration) {
        dotsToRemove.push({ x, y, dotId });
      }
    });
    
    // Remove expired dots in a single state update
    if (dotsToRemove.length > 0) {
      setGrid(prevGrid => {
        const newGrid = prevGrid.map(row => [...row]);
        dotsToRemove.forEach(({ x, y, dotId }) => {
          if (newGrid[x][y]) {
            newGrid[x][y] = false;
            // Notify server that dot was missed
            socketRef.current.emit('catch_dot', {
              position: [x, y],
              timestamp: new Date().toISOString(),
              event_type: 'dot_missed'
            });
          }
          // Remove from active animations
          activeAnimationsRef.current.delete(dotId);
        });
        return newGrid;
      });
    }
    
    // Continue animation loop if there are active animations
    if (activeAnimationsRef.current.size > 0) {
      animationFrameRef.current = requestAnimationFrame(animateAllDots);
    }
  };

  // Initialize grid and WebSocket connection
  useEffect(() => {
    // Reset grid
    const newGrid = Array(GRID_SIZE).fill().map(() => Array(GRID_SIZE).fill(false));
    setGrid(newGrid);
    
    // Connect to WebSocket server
    socketRef.current = io('http://localhost:5001');
    
    // Listen for dot appearance events
    socketRef.current.on('dot_appeared', (data) => {
      console.log('Dot appeared:', data);
      const { position } = data;
      const [x, y] = position;
      
      // Show the dot
      setGrid(prevGrid => {
        const newGrid = prevGrid.map(row => [...row]);
        newGrid[x][y] = true;
        return newGrid;
      });
      
      // Create a timeout ID for this specific dot
      const dotId = `${x}-${y}`;
      
      // Clear any existing timeout for this dot position
      if (dotTimeoutsRef.current.has(dotId)) {
        clearTimeout(dotTimeoutsRef.current.get(dotId));
      }
      
      // Start animation using requestAnimationFrame instead of setTimeout
      const startTime = Date.now();
      
      // Store the animation in active animations
      activeAnimationsRef.current.set(dotId, {
        x,
        y,
        startTime,
        duration: 2000
      });
      
      // Start the animation loop if not already running
      if (animationFrameRef.current === null) {
        animationFrameRef.current = requestAnimationFrame(animateAllDots);
      }
    });
    
    // Listen for game state updates
    socketRef.current.on('game_state_update', (data) => {
      console.log('Game state update:', data);
      setScore(data.score || 0);
      setMisses(data.misses || 0);
      setGameOver(data.game_over || false);
    });
    
    // Listen for game over event
    socketRef.current.on('game_over', (data) => {
      console.log('Game over:', data);
      setGameResult(data);
      setGameOver(true);
    });
    
    // Listen for game reset event
    socketRef.current.on('game_reset', (data) => {
      console.log('Game reset:', data);
      setGameOver(false);
      setGameResult(null);
      const newGrid = Array(GRID_SIZE).fill().map(() => Array(GRID_SIZE).fill(false));
      setGrid(newGrid);
      
      // Clear all pending timeouts
      dotTimeoutsRef.current.forEach(timeoutId => clearTimeout(timeoutId));
      dotTimeoutsRef.current.clear();
      
      // Cancel all active animations
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
        animationFrameRef.current = null;
      }
      activeAnimationsRef.current.clear();
    });
    
    // Clean up WebSocket connection and timeouts
    return () => {
      if (socketRef.current) {
        socketRef.current.disconnect();
      }
      
      // Clear all pending timeouts
      dotTimeoutsRef.current.forEach(timeoutId => clearTimeout(timeoutId));
      dotTimeoutsRef.current.clear();
      
      // Cancel all active animations
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
      activeAnimationsRef.current.clear();
    };
  }, []);

  // Handle cell click
  const handleCellClick = (x, y) => {
    if (gameOver) return;
    
    if (grid[x][y]) {
      // Caught the dot
      setGrid(prevGrid => {
        const newGrid = prevGrid.map(row => [...row]);
        newGrid[x][y] = false;
        return newGrid;
      });
      
      // Clear the timeout for this dot since it was caught
      const dotId = `${x}-${y}`;
      if (dotTimeoutsRef.current.has(dotId)) {
        clearTimeout(dotTimeoutsRef.current.get(dotId));
        dotTimeoutsRef.current.delete(dotId);
      }
      
      // Remove from active animations
      if (activeAnimationsRef.current.has(dotId)) {
        activeAnimationsRef.current.delete(dotId);
      }
      
      // Notify server that dot was caught
      socketRef.current.emit('catch_dot', {
        position: [x, y],
        timestamp: new Date().toISOString(),
        event_type: 'dot_caught'
      });
    }
  };

  // Reset game
  const resetGame = () => {
    socketRef.current.emit('reset_game');
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Dot Catcher Game</h1>
        <div className="game-stats">
          <div>Score: {score}/{targetScore}</div>
          <div>Misses: {misses}/{maxMisses}</div>
        </div>
        
        <div className="progress-bars">
          <div className="progress-container">
            <label>Progress:</label>
            <div className="progress-bar">
              <div 
                className="progress-fill" 
                style={{width: `${Math.min(100, (score/targetScore)*100)}%`}}
              ></div>
            </div>
          </div>
          <div className="progress-container">
            <label>Mistakes:</label>
            <div className="progress-bar mistake-bar">
              <div 
                className="progress-fill" 
                style={{width: `${Math.min(100, (misses/maxMisses)*100)}%`}}
              ></div>
            </div>
          </div>
        </div>
        
        <div className="grid-container">
          {grid.map((row, x) => (
            <div key={x} className="grid-row">
              {row.map((cell, y) => (
                <div
                  key={`${x}-${y}`}
                  className={`grid-cell ${cell ? 'dot' : ''}`}
                  onClick={() => handleCellClick(x, y)}
                >
                  {cell && <div className="dot-symbol">●</div>}
                </div>
              ))}
            </div>
          ))}
        </div>
        
        <div className="controls">
          <button onClick={resetGame}>Reset Game</button>
        </div>
        
        {gameOver && (
          <div className="game-over">
            <h2>{gameResult?.result === 'win' ? '🎉 You Won! 🎉' : '😢 Game Over 😢'}</h2>
            <p>{gameResult?.message}</p>
            <button onClick={resetGame}>Play Again</button>
          </div>
        )}
      </header>
    </div>
  );
}

export default App;