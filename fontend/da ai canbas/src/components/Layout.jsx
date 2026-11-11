import "./Layout.css";
import { useEffect, useState } from "react";
import { Navigate, Outlet, NavLink, Link } from "react-router";
import { getToken } from "../api.js";

const API_URL = "http://localhost:8000/api/courses";

function navClass({ isActive }) {
  return isActive ? "dash-rail-link is-active" : "dash-rail-link";
}

export function Layout() {

  const [coursesOpen, setCoursesOpen] = useState(false);
  const [courses, setCourses] = useState([]);


  useEffect(() => {
    async function loadCourses() {
      try {
        const response = await fetch(API_URL);
        if (response.ok) {
          setCourses(await response.json());
        }
      } catch (err) {
        console.error("Fetch error:", err);
      }
    }

    loadCourses();
  }, []);

  if (!getToken()) {
    return <Navigate to="/" replace />;
  }

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

  const allCourses = [hardcodedCourse, ...courses];


  return (
    <div className="layout">
      <nav className="dash-rail">
        <div className="dash-rail-logo">C.AI</div>
        <ul className="dash-rail-list">
          <li><NavLink to="/account" className={navClass}>Account</NavLink></li>
          <li><NavLink to="/dashboard" className={navClass}>Dashboard</NavLink></li>
          <li>
            <button
              type="button"
              className={coursesOpen ? "dash-rail-link dash-rail-button is-active" : "dash-rail-link dash-rail-button"}
              onClick={() => setCoursesOpen(!coursesOpen)}
            >
              Courses
            </button>
          </li>
          <li><NavLink to="/calendar" className={navClass}>Calendar</NavLink></li>
          <li><NavLink to="/inbox" className={navClass}>Inbox</NavLink></li>
          <li><NavLink to="/help" className={navClass}>Help</NavLink></li>
        </ul>
      </nav>

      {coursesOpen && (
        <aside className="courses-tray">
          <div className="tray-header">
            <h2 className="tray-title">Courses</h2>
            <button type="button" className="dash-options-btn" onClick={() => setCoursesOpen(false)}>Close</button>
          </div>

          {allCourses.length === 0 && <p className="tray-empty">No courses yet.</p>}

          <ul className="tray-list">
            {allCourses.map((course) => (
              <li key={course._id} className="tray-item">
                <Link
                  to={`/courses/${course._id}`}
                  className="tray-link"
                  onClick={() => setCoursesOpen(false)}
                >
                  {course.name}
                </Link>
                <p className="tray-detail">{course.code} · {course.term}</p>
              </li>
            ))}
          </ul>
        </aside>
      )}

      <div className="layout-content">

        <Outlet />
        
      </div>

      
    </div>
  );
}