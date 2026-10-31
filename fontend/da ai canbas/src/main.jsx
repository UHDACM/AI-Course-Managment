import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { Routes, Route } from 'react-router';
import './index.css'
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Routes>
      /*App is probably gonna be the login page */
      <Route index element={<App />} />
      <Route path="course-list" element={<div>All your courses are taught by Yuan</div>} />
    </Routes>
    
  </StrictMode>,
)
