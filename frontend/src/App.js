import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [userId, setUserId] = useState(localStorage.getItem('userId') || '');
  const [stats, setStats] = useState(null);
  const [loginError, setLoginError] = useState('');
  const [myCourses, setMyCourses] = useState([]);
  const [recentActivity, setRecentActivity] = useState([]);
  const [newestCourses, setNewestCourses] = useState([]);
  const [activeDiscussions, setActiveDiscussions] = useState([]);

  useEffect(() => {
    if (userId) {
      fetch(`http://localhost:5000/user/${userId}/stats`)
        .then(response => response.json())
        .then(data => setStats(data))
        .catch(error => console.error('Error fetching stats:', error));

      fetch(`http://localhost:5000/my_courses/${userId}`)
        .then(response => response.json())
        .then(data => setMyCourses(data))
        .catch(error => console.error('Error fetching my courses:', error));

      fetch(`http://localhost:5000/recent_activity/${userId}`)
        .then(response => response.json())
        .then(data => setRecentActivity(data))
        .catch(error => console.error('Error fetching recent activity:', error));

      fetch(`http://localhost:5000/newest_courses`)
        .then(response => response.json())
        .then(data => setNewestCourses(data))
        .catch(error => console.error('Error fetching newest courses:', error));

      fetch(`http://localhost:5000/active_discussions`)
        .then(response => response.json())
        .then(data => setActiveDiscussions(data))
        .catch(error => console.error('Error fetching active discussions:', error));
    }
  }, [userId]);

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoginError('');

    try {
      const response = await fetch('http://localhost:5000/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();

      if (response.ok) {
        localStorage.setItem('userId', data.user_id);
        setUserId(data.user_id);
      } else {
        setLoginError(data.message || 'Login failed');
      }
    } catch (error) {
      setLoginError('Network error');
      console.error('Login error:', error);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('userId');
    setUserId('');
    setStats(null);
  };

  if (!userId) {
    return (
      <div className="App container">
        <div className="card">
          <div className="card-body">
            <h2 className="card-title">Login</h2>
            {loginError && <p className="text-danger">{loginError}</p>}
            <form onSubmit={handleLogin}>
              <div className="mb-3">
                <input
                  type="text"
                  className="form-control"
                  placeholder="Username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                />
              </div>
              <div className="mb-3">
                <input
                  type="password"
                  className="form-control"
                  placeholder="Password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>
              <button type="submit" className="btn btn-primary">Login</button>
            </form>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="App">
      <nav className="navbar navbar-expand-lg navbar-light bg-light">
        <div className="container-fluid">
          <a className="navbar-brand" href="#">Dashboard</a>
          <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarNav">
            <ul className="navbar-nav ms-auto">
              <li className="nav-item">
                <button onClick={handleLogout} className="btn btn-link nav-link">Logout</button>
              </li>
            </ul>
          </div>
        </div>
      </nav>

      <div className="container-fluid">
        <div className="row">
          <nav id="sidebar" className="col-md-3 col-lg-2 d-md-block bg-light sidebar">
            <div className="position-sticky">
              <ul className="nav flex-column">
                <li className="nav-item">
                  <button className="nav-link active" aria-current="page">
                    Overview
                  </button>
                </li>
                <li className="nav-item">
                  <button className="nav-link">
                    Reports
                  </button>
                </li>
                <li className="nav-item">
                  <button className="nav-link">
                    Analytics
                  </button>
                </li>
                <li className="nav-item">
                  <button className="nav-link">
                    Export
                  </button>
                </li>
                <li className="nav-item">
                  <button className="nav-link">
                    My Contributions
                  </button>
                </li>
                <li className="nav-item">
                  <button className="nav-link">
                    Quick Links
                  </button>
                </li>
              </ul>
            </div>
          </nav>

          <main className="col-md-9 ms-sm-auto col-lg-10 px-md-4">
            <div className="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
              <h1 className="h2">Dashboard</h1>
            </div>

            <div className="row">
              <div className="col-md-4">
                <div className="card">
                  <div className="card-body">
                    <h5 className="card-title">Courses Enrolled</h5>
                    <p className="card-text">{stats ? stats.enrollment_count : 'Loading...'}</p>
                  </div>
                </div>
              </div>
              <div className="col-md-4">
                <div className="card">
                  <div className="card-body">
                    <h5 className="card-title">Topics Posted</h5>
                    <p className="card-text">{stats ? stats.topic_count : 'Loading...'}</p>
                  </div>
                </div>
              </div>
              <div className="col-md-4">
                <div className="card">
                  <div className="card-body">
                    <h5 className="card-title">Entries Posted</h5>
                    <p className="card-text">{stats ? stats.entry_count : 'Loading...'}</p>
                  </div>
                </div>
              </div>
            </div>

            <div className="row">
              <div className="col-md-6">
                <div className="card">
                  <div className="card-body">
                    <h5 className="card-title">My Courses</h5>
                    <table className="table">
                      <thead>
                        <tr>
                          <th>Course Name</th>
                          <th>Course Code</th>
                          <th>Enrollment Type</th>
                        </tr>
                      </thead>
                      <tbody>
                        {myCourses.map(course => (
                          <tr key={course.course_code}>
                            <td>{course.course_name}</td>
                            <td>{course.course_code}</td>
                            <td>{course.enrollment_type}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
              <div className="col-md-6">
                <div className="card">
                  <div className="card-body">
                    <h5 className="card-title">Recent Activity</h5>
                    <ul>
                      {recentActivity.map(activity => (
                        <li key={activity.entry_created_at}>
                          {activity.topic_title} - {activity.entry_content}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            </div>

            <div className="row">
              <div className="col-md-6">
                <div className="card">
                  <div className="card-body">
                    <h5 className="card-title">Newest Courses</h5>
                    <ul>
                      {newestCourses.map(course => (
                        <li key={course.course_code}>
                          {course.course_name} - {course.course_code}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
              <div className="col-md-6">
                <div className="card">
                  <div className="card-body">
                    <h5 className="card-title">Active Discussions</h5>
                    <ul>
                      {activeDiscussions.map(discussion => (
                        <li key={discussion.topic_title}>
                          {discussion.topic_title} - {discussion.entry_created_at}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </main>
        </div>
      </div>
    </div>
  );
}

export default App;
