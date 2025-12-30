import React, { useState, useEffect, useRef } from "react";
import io from "socket.io-client";
import "./App.css";

const GRID = 5, TARGET = 10, MAX_MISS = 5;

export default function App() {
  const emptyGrid = () => Array(GRID).fill().map(() => Array(GRID).fill(false));
  const [grid, setGrid] = useState(emptyGrid);
  const [score, setScore] = useState(0);
  const [misses, setMisses] = useState(0);
  const [gameOver, setGameOver] = useState(false);
  const [result, setResult] = useState(null);
  const socket = useRef(null);

  useEffect(() => {
    socket.current = io("http://localhost:5001");

    socket.current.on("dot_appeared", ({ position: [x, y] }) => {
      setGrid(g => {
        const ng = g.map(r => [...r]);
        ng[x][y] = true;
        return ng;
      });

      setTimeout(() => {
        setGrid(g => {
          if (!g[x][y]) return g;
          const ng = g.map(r => [...r]);
          ng[x][y] = false;
          socket.current.emit("catch_dot", { position: [x, y], event_type: "dot_missed" });
          return ng;
        });
      }, 2000);
    });

    socket.current.on("game_state_update", d => {
      setScore(d.score || 0);
      setMisses(d.misses || 0);
      setGameOver(d.game_over || false);
    });

    socket.current.on("game_over", d => {
      setResult(d);
      setGameOver(true);
    });

    socket.current.on("game_reset", () => {
      setGrid(emptyGrid());
      setScore(0);
      setMisses(0);
      setGameOver(false);
      setResult(null);
    });

    return () => socket.current.disconnect();
  }, []);

  const clickCell = (x, y) => {
    if (gameOver || !grid[x][y]) return;
    setGrid(g => {
      const ng = g.map(r => [...r]);
      ng[x][y] = false;
      return ng;
    });
    socket.current.emit("catch_dot", { position: [x, y], event_type: "dot_caught" });
  };

  return (
    <div className="App">
      <h1>Dot Catcher</h1>
      <p>Score: {score}/{TARGET} | Misses: {misses}/{MAX_MISS}</p>

      <div className="grid-container">
        {grid.map((r, x) => (
          <div key={x} className="grid-row">
            {r.map((c, y) => (
              <div
                key={y}
                className={`grid-cell ${c ? "dot" : ""}`}
                onClick={() => clickCell(x, y)}
              >
                {c && "●"}
              </div>
            ))}
          </div>
        ))}
      </div>

      <button onClick={() => socket.current.emit("reset_game")}>Reset</button>

      {gameOver && (
        <div className="game-over">
          <h2>{result?.result === "win" ? "🎉 You Won!" : "😢 Game Over"}</h2>
          <p>{result?.message}</p>
        </div>
      )}
    </div>
  );
}
