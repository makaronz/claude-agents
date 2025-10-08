import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AppProviders } from './context';
import Layout from './components/layout/Layout/Layout';
import Dashboard from './pages/Dashboard/Dashboard';
import Projects from './pages/Projects/Projects';
import Clients from './pages/Clients/Clients';
import Squad from './pages/Squad/Squad';
import Settings from './pages/Settings/Settings';

function App() {
  return (
    <BrowserRouter>
      <AppProviders>
        <AppContent />
      </AppProviders>
    </BrowserRouter>
  );
}

function AppContent() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Dashboard />} />
        <Route path="projects" element={<Projects />} />
        <Route path="clients" element={<Clients />} />
        <Route path="squad" element={<Squad />} />
        <Route path="settings" element={<Settings />} />
      </Route>
    </Routes>
  );
}

export default App;
