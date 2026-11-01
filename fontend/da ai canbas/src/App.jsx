import { LoginPage } from './components/LoginPage.jsx';
import './App.css'
import { Routes, Route } from 'react-router';
import { Dashboard } from './components/Dashboard.jsx';
import { Error } from './components/Error.jsx';
function App() {
  

  return (
    <Routes>
      <Route index element={<LoginPage />} />
      <Route path="dashboard" element={<Dashboard />} />
      <Route path="*" element={<Error />} />
    </Routes>
  );
}

export default App
