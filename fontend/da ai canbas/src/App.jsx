import { LoginPage } from './components/LoginPage.jsx';
import './App.css'
import { Routes, Route } from 'react-router';
import { Layout } from './components/Layout.jsx';
import { Dashboard } from './components/Dashboard.jsx';
import { Account } from './components/Account.jsx';
import { CoursePage } from './components/CoursePage.jsx';
import { Calendar } from './components/Calendar.jsx';
import { Inbox } from './components/Inbox.jsx';
import { Help } from './components/Help.jsx';
import { Error } from './components/Error.jsx';

function App() {
  return (
    <Routes>
      {/* No layout: login page */}
      <Route index element={<LoginPage />} />

      {/* Everything inside here gets the nav rail and the login check */}
      <Route element={<Layout />}>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/account" element={<Account />} />
        <Route path="/courses/:id" element={<CoursePage />} />
        <Route path="/calendar" element={<Calendar />} />
        <Route path="/inbox" element={<Inbox />} />
        <Route path="/help" element={<Help />} />
      </Route>

      <Route path="*" element={<Error />} />
    </Routes>
  );
}

export default App