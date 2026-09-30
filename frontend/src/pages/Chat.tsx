import { useEffect, useState } from "react";
import type { FormEvent } from "react";
import apiClient from "../api/client";
import "./Chat.css";

interface ChatSource {
  journal_entry_id: number;
  title: string;
  created_at: string;
}

interface ChatResponse {
  answer: string;
  sources: ChatSource[];
}

function Chat() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState<ChatSource[]>([]);
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
      setSources([]);

      const response = await apiClient.post<ChatResponse>(
        "/journal/chat",
        {
          question: question.trim(),
        }
      );

      setAnswer(response.data.answer);
      setSources(response.data.sources);
    } catch (error: any) {
      setError(
        error.response?.data?.detail ||
          "Failed to get an answer from the AI."
      );
    } finally {
      setLoading(false);
    }
  };
  useEffect(() => {
    document.title = 'Ask AI';
  }, []);
 return (
  <div className="chat-page">
    <div className="chat-container">

      {/* Header */}
      <header className="chat-header">
        <p className="chat-eyebrow">
          AI companion
        </p>

        <h1>
          Ask Your Journal
        </h1>

        <p className="chat-subtitle">
          Ask questions about your memories, experiences,
          and thoughts. Your AI assistant answers using
          your journal entries.
        </p>
      </header>

      {/* Chat Card */}
      <section className="chat-panel">

        <form
          className="chat-form"
          onSubmit={handleSubmit}
        >
          <div className="form-field">
            <label htmlFor="journal-question">
              What would you like to know?
            </label>

            <textarea
              id="journal-question"
              value={question}
              onChange={(event) =>
                setQuestion(event.target.value)
              }
              placeholder="Ask something about your journal..."
              rows={5}
            />
          </div>

          {error && (
            <p className="error-message">
              {error}
            </p>
          )}

          <button
            className="primary-button"
            type="submit"
            disabled={
              loading || !question.trim()
            }
          >
            {loading
              ? "Thinking..."
              : "Ask AI"}
          </button>
        </form>

        {/* AI Response */}
        {answer && (
          <section className="chat-response">

            <div className="chat-ai-indicator">
              <span className="chat-ai-dot"></span>
              AI assistant
            </div>

            <h2>
              AI Response
            </h2>

            <p>
              {answer}
            </p>

            {/* Sources */}
            {sources.length > 0 && (
              <div className="chat-sources">

                <h3>
                  Sources from your journal
                </h3>

                <ul>
                  {sources.map((source) => (
                    <li
                      key={source.journal_entry_id}
                    >
                      <strong>
                        {source.title}
                      </strong>

                      {" — "}

                      {new Date(
                        source.created_at
                      ).toLocaleDateString()}
                    </li>
                  ))}
                </ul>

              </div>
            )}

          </section>
        )}

      </section>
    </div>
  </div>
);
}

export default Chat;