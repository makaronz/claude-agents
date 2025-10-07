import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { useWebSocket } from './hooks/useWebSocket';
import Layout from './components/layout/Layout/Layout';
import Dashboard from './pages/Dashboard/Dashboard';
import Projects from './pages/Projects/Projects';
import Clients from './pages/Clients/Clients';
import Squad from './pages/Squad/Squad';
import Settings from './pages/Settings/Settings';

function App() {
  // Initialize WebSocket connection globally
  const { connected } = useWebSocket();

  return (
    <BrowserRouter>
      {/* WebSocket Status Indicator */}
      {!connected && (
        <div className="fixed top-0 right-0 z-50 m-4 px-3 py-1 bg-yellow-100 text-yellow-800 text-xs rounded-md shadow-md">
          ⚠️ Connecting...
        </div>
      )}

      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="projects" element={<Projects />} />
          <Route path="clients" element={<Clients />} />
          <Route path="squad" element={<Squad />} />
          <Route path="settings" element={<Settings />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
