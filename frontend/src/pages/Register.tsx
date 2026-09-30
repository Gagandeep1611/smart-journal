import { useEffect, useState } from "react";
import type { FormEvent } from "react";
import { Link, useNavigate } from "react-router-dom";
import apiClient from "../api/client";
import "./Auth.css";

function Register() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    setError("");
    setLoading(true);

    try {
      await apiClient.post("/auth/register", {
        email,
        password,
      });

      navigate("/login");
    } catch (error: any) {
      setError(
        error.response?.data?.detail ||
          "Registration failed. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };
  useEffect(() => {
    document.title = 'Register';
  }, []);
  return (
    <div className="login-page">
      <div className="login-background">
        <div className="background-orb orb-one"></div>
        <div className="background-orb orb-two"></div>
        <div className="background-orb orb-three"></div>
      </div>

      <div className="login-container">

        {/* Brand */}
        <div className="brand">
          <div className="brand-icon">
            <span>✦</span>
          </div>

          <span className="brand-name">Smart Journal</span>
        </div>

        {/* Card */}
        <div className="login-card">

          <div className="login-header">
            <p className="eyebrow">Get started</p>

            <h1>Create your account</h1>

            <p className="login-subtitle">
              Start keeping your thoughts organized and accessible.
            </p>
          </div>

          <form className="login-form" onSubmit={handleSubmit}>

            {/* Email */}
            <div className="form-field">
              <label htmlFor="email">Email address</label>

              <div className="input-wrapper">
                <span className="input-icon">
                  <svg
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="1.8"
                  >
                    <rect x="3" y="5" width="18" height="14" rx="2" />
                    <path d="m3 7 9 6 9-6" />
                  </svg>
                </span>

                <input
                  id="email"
                  type="email"
                  placeholder="you@example.com"
                  value={email}
                  onChange={(event) => setEmail(event.target.value)}
                  required
                />
              </div>
            </div>

            {/* Password */}
            <div className="form-field">
              <label htmlFor="password">Password</label>

              <div className="input-wrapper">
                <span className="input-icon">
                  <svg
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="1.8"
                  >
                    <rect x="4" y="10" width="16" height="10" rx="2" />
                    <path d="M8 10V7a4 4 0 0 1 8 0v3" />
                  </svg>
                </span>

                <input
                  id="password"
                  type="password"
                  placeholder="At least 8 characters"
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                  minLength={8}
                  required
                />
              </div>

              <span className="field-hint">
                Password must contain at least 8 characters.
              </span>
            </div>

            {/* Error */}
            {error && (
              <div className="error-message">
                {error}
              </div>
            )}

            {/* Button */}
            <button
              className="primary-button"
              type="submit"
              disabled={loading}
            >
              {loading ? (
                <>
                  <span className="button-spinner"></span>
                  Creating account...
                </>
              ) : (
                "Create account"
              )}
            </button>
          </form>

          {/* Footer */}
          <p className="auth-footer">
            Already have an account?{" "}
            <Link to="/login">Login</Link>
          </p>

        </div>

        {/* Privacy */}
        <p className="privacy-note">
          Your journal is private and protected.
        </p>

      </div>
    </div>
  );
}

export default Register;