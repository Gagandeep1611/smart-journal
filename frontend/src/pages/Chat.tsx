import { useState } from "react";
import type { FormEvent } from "react";
import apiClient from "../api/client";

function Chat() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (!question.trim()) {
      return;
    }

    try {
      setLoading(true);
      setError("");
      setAnswer("");

      const response = await apiClient.post("/journal/chat", {
        question: question.trim(),
      });

      setAnswer(response.data.answer);
    } catch (error: any) {
      setError(
        error.response?.data?.detail ||
          "Failed to get an answer from the AI."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-page">
      <section className="panel chat-panel">
        <div className="panel-header">
          <p className="eyebrow">AI companion</p>
          <h1>Ask Your Journal</h1>
        </div>

        <form className="chat-form" onSubmit={handleSubmit}>
          <div className="form-field">
            <label htmlFor="journal-question">Question</label>
            <textarea
              id="journal-question"
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
              placeholder="Ask something about your journal..."
              rows={5}
            />
          </div>

          {error && <p className="error-message">{error}</p>}

          <button
            className="primary-button"
            type="submit"
            disabled={loading || !question.trim()}
          >
            {loading ? "Thinking..." : "Ask AI"}
          </button>
        </form>

        {answer && (
          <section className="chat-response">
            <h2>AI Response</h2>
            <p>{answer}</p>
          </section>
        )}
      </section>
    </div>
  );
}

export default Chat;