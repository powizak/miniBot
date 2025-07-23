import React, { useEffect, useState } from "react";

const API_URL = process.env.REACT_APP_API_URL;

export default function TradeHistory() {
  const [trades, setTrades] = useState([]);
  const [logs, setLogs] = useState([]);
  const [filter, setFilter] = useState("all");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [detail, setDetail] = useState(null);

  const token = localStorage.getItem("token");

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError("");
      try {
        const [tradesRes, logsRes] = await Promise.all([
          fetch(`${API_URL}/trades`, { headers: { Authorization: `Bearer ${token}` } }),
          fetch(`${API_URL}/logs`, { headers: { Authorization: `Bearer ${token}` } }),
        ]);
        if (!tradesRes.ok || !logsRes.ok) throw new Error("Chyba při načítání dat.");
        setTrades(await tradesRes.json());
        setLogs(await logsRes.json());
      } catch (e) {
        setError(e.message);
      }
      setLoading(false);
    };
    fetchData();
    // eslint-disable-next-line
  }, []);

  const filteredTrades = filter === "all" ? trades : trades.filter(t => t.type === filter);

  return (
    <div style={{ maxWidth: 900, margin: "2rem auto" }}>
      <h3>Historie obchodů a logů</h3>
      <div style={{ marginBottom: 16 }}>
        <label>Filtr typů obchodů: </label>
        <select value={filter} onChange={e => setFilter(e.target.value)}>
          <option value="all">Vše</option>
          <option value="buy">Nákup</option>
          <option value="sell">Prodej</option>
        </select>
      </div>
      {error && <div style={{ color: "red" }}>{error}</div>}
      {loading ? (
        <div>Načítám data...</div>
      ) : (
        <>
          <table style={{ width: "100%", borderCollapse: "collapse", marginBottom: 24 }}>
            <thead>
              <tr>
                <th>ID</th>
                <th>Čas</th>
                <th>Typ</th>
                <th>Množství</th>
                <th>Cena</th>
                <th>Bot</th>
                <th>Detail</th>
              </tr>
            </thead>
            <tbody>
              {filteredTrades.map(trade => (
                <tr key={trade.id}>
                  <td>{trade.id}</td>
                  <td>{trade.time}</td>
                  <td>{trade.type}</td>
                  <td>{trade.amount}</td>
                  <td>{trade.price}</td>
                  <td>{trade.bot_name || trade.bot_id}</td>
                  <td>
                    <button onClick={() => setDetail(trade)}>Zobrazit</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          <h4>Logy</h4>
          <ul style={{ maxHeight: 200, overflowY: "auto", background: "#f9f9f9", padding: 8 }}>
            {logs.map(log => (
              <li key={log.id} style={{ fontSize: 13, marginBottom: 4 }}>
                <b>{log.time}:</b> {log.message}
              </li>
            ))}
          </ul>
        </>
      )}
      {detail && (
        <div style={{
          position: "fixed", top: 80, left: 0, right: 0, maxWidth: 500, margin: "auto",
          background: "#fff", border: "1px solid #ccc", borderRadius: 8, padding: 24, zIndex: 1000
        }}>
          <h4>Detail obchodu</h4>
          <pre style={{ whiteSpace: "pre-wrap" }}>{JSON.stringify(detail, null, 2)}</pre>
          <button onClick={() => setDetail(null)}>Zavřít</button>
        </div>
      )}
    </div>
  );
}