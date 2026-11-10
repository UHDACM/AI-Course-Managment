import "./Dashboard.css";
import { useEffect, useState } from "react";
import { Navigate, useNavigate } from "react-router";
import { clearToken, getToken } from "../api.js";

const API_URL = "http://localhost:8000/api/courses";

const CARD_COLORS = ['rgb(46, 167, 116)', 'rgb(47, 48, 104)', 'rgb(180, 49, 34)', 'rgb(207, 152, 48)', 'rgb(153, 37, 128)', 'rgb(43, 77, 83)'];

const hardcodedCourse = {
  _id: "ACM-ASSEMBLE",
  name: "ACM++",
  code: "CS 9000",
  description: "give fortnite token",
  term: "Spring 2099",
  instructor_id: "123456789123456789123456",
  syllabus: null,
  syllabus_updated_at: null,
  created_at: "2099-12-01T06:31:12.999999",
};

export function Dashboard() {
  const navigate = useNavigate();
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadCourses() {
      try {
        const response = await fetch(API_URL);
        if (!response.ok) {
          throw new Error(`Server responded with status ${response.status}`);
        }
        const data = await response.json();
        setCourses(data);
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    }

    loadCourses();
  }, []);

  if (!getToken()) {
    return <Navigate to="/" replace />;
  }

  function handleLogout() {
    clearToken();
    navigate("/");
  }

  const allCourses = [hardcodedCourse, ...courses];

  return (
    <div className="dash-layout">
      {/* Left/Nav */}
      <nav className="dash-rail" >
        <div className="dash-rail-logo">C.AI</div>
        <ul className="dash-rail-list">
          <li><a href="/account" className="dash-rail-link">Account</a></li>
          <li><a href="/dashboard" className="dash-rail-link is-active">Dashboard</a></li>
          <li><a href="/courses" className="dash-rail-link">Courses</a></li>
          <li><a href="/calendar" className="dash-rail-link">Calendar</a></li>
          <li><a href="/inbox" className="dash-rail-link">Inbox</a></li>
          <li><a href="/help" className="dash-rail-link">Help</a></li>
        </ul>
      </nav>

      {/* Main/Middle content */}
      <main className="dash-main">
        <header className="dash-header">
          <h1 className="dash-title">Dashboard</h1>
          <button type="button" className="dash-options-btn">Dashboard options</button>
          <button type="button" className="dash-options-btn" onClick={handleLogout}>Log out</button>
        </header>

        <section >
          <h2 id="courses-heading" className="dash-section-title">
            Courses ({allCourses.length})
          </h2>

          {loading && <p className="dash-empty">Loading courses...</p>}

          {error && (
            <p className="dash-empty" role="alert">
              Could not load courses: {error}. Check that the backend is running on port 8000.
            </p>
          )}

          <ul className="course-grid">
            {allCourses.map((course, i) => (
              <li key={course._id} className="course-card">
                <a href={`/courses/${course._id}`} className="course-card-link">
                  <div
                    className="course-card-hero"
                    style={{ backgroundColor: CARD_COLORS[i % CARD_COLORS.length] }}
                  />
                  <div className="course-card-body">
                    <h3 className="course-card-name">{course.name}</h3>
                    <p className="course-card-code">{course.code}</p>
                    <p className="course-card-term">{course.term}</p>
                  </div>
                </a>
                <div className="course-card-footer">
                  <a href={`/courses/${course._id}/assignments`} className="course-card-tool">Assignments</a>
                  <a href={`/courses/${course._id}/syllabus`} className="course-card-tool">Syllabus</a>
                  <a href={`/courses/${course._id}/ai`} className="course-card-tool">AI Assistant</a>
                </div>
              </li>
            ))}
          </ul>
        </section>
      </main>

      {/* Right sidebar */}
      <aside className="dash-sidebar" >
        <section className="sidebar-block">
          <h2 className="sidebar-title">To Do</h2>
          <p className="sidebar-content">Nothing for now</p>
        </section>

        <section className="sidebar-block">
          <h2 className="sidebar-title">Coming Up</h2>
          <p className="sidebar-content">Nothing for the next week</p>
        </section>

        <section className="sidebar-block">
          <h2 className="sidebar-title">Recent Feedback</h2>
          <p className="sidebar-content">Nothing for now</p>
        </section>
      </aside>
    </div>
  );
}

