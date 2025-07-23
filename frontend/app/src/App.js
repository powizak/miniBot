import React, { useState } from 'react';
import Auth from './components/Auth';
import Dashboard from './pages/Dashboard';

function App() {
  const [showDashboard, setShowDashboard] = useState(false);

  return (
    <div style={{ textAlign: 'center' }}>
      <header>
        <h1>miniBot Frontend</h1>
        <button onClick={() => setShowDashboard(!showDashboard)}>
          {showDashboard ? 'Přepnout na přihlášení' : 'Přepnout na dashboard'}
        </button>
      </header>
      <main style={{ marginTop: 32 }}>
        {showDashboard ? <Dashboard /> : <Auth />}
      </main>
    </div>
  );
}

export default App;
