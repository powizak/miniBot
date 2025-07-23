// Komponenta pro autentizaci uživatele (přihlášení)
import React, { useState } from "react";

export default function Auth({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    if (!username || !password) {
      setError("Vyplňte uživatelské jméno a heslo.");
      return;
    }
    setLoading(true);
    try {
      const res = await fetch(`${process.env.REACT_APP_API_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });
      if (!res.ok) {
        throw new Error("Neplatné přihlašovací údaje.");
      }
      const data = await res.json();
      if (data && data.token) {
        localStorage.setItem("token", data.token);
        if (onLogin) onLogin();
      } else {
        setError("Chyba při přihlášení.");
      }
    } catch (err) {
      setError(err.message || "Chyba připojení k serveru.");
    }
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: 350, margin: "2rem auto", padding: 24, border: "1px solid #ddd", borderRadius: 8 }}>
      <h2>Přihlášení</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Uživatel</label>
          <input
            type="text"
            value={username}
            onChange={e => setUsername(e.target.value)}
            autoComplete="username"
            required
            style={{ width: "100%", marginBottom: 8 }}
          />
        </div>
        <div>
          <label>Heslo</label>
          <input
            type="password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            autoComplete="current-password"
            required
            style={{ width: "100%", marginBottom: 8 }}
          />
        </div>
        {error && <div style={{ color: "red", marginBottom: 8 }}>{error}</div>}
        <button type="submit" disabled={loading} style={{ width: "100%" }}>
          {loading ? "Přihlašuji..." : "Přihlásit"}
        </button>
      </form>
    </div>
  );
}