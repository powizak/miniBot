import React, { useEffect, useState, useRef } from "react";

const WS_URL = process.env.REACT_APP_WS_URL;

export default function Notifications() {
  const [notifications, setNotifications] = useState([]);
  const [error, setError] = useState("");
  const ws = useRef(null);

  useEffect(() => {
    ws.current = new window.WebSocket(WS_URL);

    ws.current.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data);
        setNotifications((prev) => [{ ...msg, id: Date.now() }, ...prev]);
      } catch {
        setError("Chyba při zpracování notifikace.");
      }
    };

    ws.current.onerror = () => setError("Chyba websocket spojení.");
    ws.current.onclose = () => setError("Spojení ukončeno.");

    return () => {
      ws.current && ws.current.close();
    };
  }, []);

  const removeNotification = (id) => {
    setNotifications((prev) => prev.filter((n) => n.id !== id));
  };

  return (
    <div style={{ maxWidth: 400, margin: "2rem auto" }}>
      <h3>Notifikace</h3>
      {error && <div style={{ color: "red" }}>{error}</div>}
      {notifications.length === 0 ? (
        <div>Žádné nové notifikace.</div>
      ) : (
        <ul style={{ listStyle: "none", padding: 0 }}>
          {notifications.map((n) => (
            <li key={n.id} style={{ background: "#f5f5f5", marginBottom: 8, padding: 8, borderRadius: 4 }}>
              <span>{n.message || JSON.stringify(n)}</span>
              <button
                onClick={() => removeNotification(n.id)}
                style={{ float: "right", background: "none", border: "none", color: "#888", cursor: "pointer" }}
                title="Skrýt"
              >
                ×
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}