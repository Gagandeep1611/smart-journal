import {
  BrowserRouter,
  Navigate,
  Route,
  Routes,
  Link,
  useNavigate,
} from "react-router-dom";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Journal from "./pages/Journal";
import Chat from "./pages/Chat";
import ProtectedRoute from "./components/ProtectedRoute";

function Navigation() {
  const navigate = useNavigate();

  const token = localStorage.getItem("access_token");

  if (!token) {
    return null;
  }

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    navigate("/login");
  };

  return (
    <nav className="app-nav">
      <div className="brand-mark">Smart Journal</div>

      <div className="nav-links">
        <Link className="nav-link" to="/journal">
          Journal
        </Link>
        <span> | </span>
        <Link className="nav-link" to="/chat">
          Ask AI
        </Link>
      </div>

      <button className="nav-logout" onClick={handleLogout}>
        Logout
      </button>
    </nav>
  );
}

function App() {
  return (
    <BrowserRouter>
      <div className="app-shell">
        <Navigation />

        <main className="page-content">
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />

            <Route element={<ProtectedRoute />}>
              <Route path="/journal" element={<Journal />} />
              <Route path="/chat" element={<Chat />} />
            </Route>

            <Route path="/" element={<Navigate to="/login" replace />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;