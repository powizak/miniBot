// Dashboard s komponentami pro správu botů, historii, grafy a notifikace
import React from "react";
import BotsManager from "../components/BotsManager";
import TradeHistory from "../components/TradeHistory";
import Charts from "../components/Charts";
import Notifications from "../components/Notifications";

export default function Dashboard() {
  return (
    <div>
      <h2>Dashboard</h2>
      <BotsManager />
      <TradeHistory />
      <Charts />
      <Notifications />
    </div>
  );
}