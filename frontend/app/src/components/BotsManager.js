import React, { useEffect, useState } from "react";

const API_URL = process.env.REACT_APP_API_URL;

export default function BotsManager() {
  const [bots, setBots] = useState([]);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [creating, setCreating] = useState(false);

  const token = localStorage.getItem("token");

  const fetchBots = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await fetch(`${API_URL}/bots/`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!res.ok) throw new Error("Chyba při načítání botů.");
      const data = await res.json();
      setBots(data);
    } catch (e) {
      setError(e.message);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchBots();
    // eslint-disable-next-line
  }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    setCreating(true);
    setError("");
    try {
      const res = await fetch(`${API_URL}/bots/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ name, description }),
      });
      if (!res.ok) throw new Error("Chyba při vytváření bota.");
      setName("");
      setDescription("");
      fetchBots();
    } catch (e) {
      setError(e.message);
    }
    setCreating(false);
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Opravdu smazat bota?")) return;
    setError("");
    try {
      const res = await fetch(`${API_URL}/bots/${id}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!res.ok) throw new Error("Chyba při mazání bota.");
      fetchBots();
    } catch (e) {
      setError(e.message);
    }
  };

  const handleStart = async (id) => {
    setError("");
    try {
      const res = await fetch(`${API_URL}/bots/${id}/start`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!res.ok) throw new Error("Chyba při spouštění bota.");
      fetchBots();
    } catch (e) {
      setError(e.message);
    }
  };

  const handlePause = async (id) => {
    setError("");
    try {
      const res = await fetch(`${API_URL}/bots/${id}/pause`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!res.ok) throw new Error("Chyba při pozastavení bota.");
      fetchBots();
    } catch (e) {
      setError(e.message);
    }
  };

  return (
    <div style={{ maxWidth: 600, margin: "2rem auto" }}>
      <h3>Správa botů</h3>
      <form onSubmit={handleCreate} style={{ marginBottom: 16 }}>
        <input
          type="text"
          placeholder="Název bota"
          value={name}
          onChange={e => setName(e.target.value)}
          required
          style={{ marginRight: 8 }}
        />
        <input
          type="text"
          placeholder="Popis"
          value={description}
          onChange={e => setDescription(e.target.value)}
          style={{ marginRight: 8 }}
        />
        <button type="submit" disabled={creating}>
          {creating ? "Vytvářím..." : "Vytvořit"}
        </button>
      </form>
      {error && <div style={{ color: "red", marginBottom: 8 }}>{error}</div>}
      {loading ? (
        <div>Načítám...</div>
      ) : (
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th>ID</th>
              <th>Název</th>
              <th>Popis</th>
              <th>Status</th>
              <th>Akce</th>
            </tr>
          </thead>
          <tbody>
            {bots.map(bot => (
              <tr key={bot.id}>
                <td>{bot.id}</td>
                <td>{bot.name}</td>
                <td>{bot.description}</td>
                <td>{bot.status}</td>
                <td>
                  <button onClick={() => handleStart(bot.id)} disabled={bot.status === "running"}>
                    Spustit
                  </button>
                  <button onClick={() => handlePause(bot.id)} disabled={bot.status === "paused"}>
                    Pozastavit
                  </button>
                  <button onClick={() => handleDelete(bot.id)} style={{ color: "red" }}>
                    Smazat
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}