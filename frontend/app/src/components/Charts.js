import React, { useEffect, useState } from "react";
import ReactECharts from "echarts-for-react";

const API_URL = process.env.REACT_APP_API_URL;

export default function Charts() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError("");
      try {
        // Příklad: načtení historických cen z backendu
        const res = await fetch(`${API_URL}/market/history`);
        if (!res.ok) throw new Error("Chyba při načítání dat.");
        const json = await res.json();
        setData(json); // očekává se pole objektů { time, close, volume, rsi, macd }
      } catch (e) {
        setError(e.message);
      }
      setLoading(false);
    };
    fetchData();
  }, []);

  const option = {
    title: { text: "Vývoj ceny a indikátorů" },
    tooltip: { trigger: "axis" },
    legend: { data: ["Cena", "Objem", "RSI", "MACD"] },
    xAxis: {
      type: "category",
      data: data.map(d => d.time),
    },
    yAxis: [
      { type: "value", name: "Cena" },
      { type: "value", name: "Objem", position: "right" },
    ],
    series: [
      {
        name: "Cena",
        type: "line",
        data: data.map(d => d.close),
        smooth: true,
      },
      {
        name: "Objem",
        type: "bar",
        yAxisIndex: 1,
        data: data.map(d => d.volume),
        opacity: 0.5,
      },
      {
        name: "RSI",
        type: "line",
        data: data.map(d => d.rsi),
        smooth: true,
      },
      {
        name: "MACD",
        type: "line",
        data: data.map(d => d.macd),
        smooth: true,
      },
    ],
  };

  return (
    <div style={{ maxWidth: 900, margin: "2rem auto" }}>
      <h3>Grafy a vizualizace</h3>
      {error && <div style={{ color: "red" }}>{error}</div>}
      {loading ? (
        <div>Načítám data...</div>
      ) : (
        <ReactECharts option={option} style={{ height: 400 }} />
      )}
      <div style={{ fontSize: 12, color: "#888", marginTop: 8 }}>
        Data jsou načítána z backendu (endpoint <code>/market/history</code>).
      </div>
    </div>
  );
}