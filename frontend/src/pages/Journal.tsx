import { useEffect, useState } from "react";
import type { FormEvent } from "react";
import apiClient from "../api/client";

interface JournalEntry {
  id: number;
  title: string;
  content: string;
  created_at: string;
}

function Journal() {
  const [content, setContent] = useState("");
  const [title, setTitle] = useState("");
  const [entries, setEntries] = useState<JournalEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  const loadEntries = async () => {
    try {
      setError("");

      const response = await apiClient.get("/journal");
      setEntries(response.data);
    } catch (error: any) {
      setError(
        error.response?.data?.detail ||
          "Failed to load journal entries."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadEntries();
  }, []);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (!title.trim() || !content.trim()) {
    return;
    }

    try {
      setSaving(true);
      setError("");

      await apiClient.post("/journal", {
        title: title.trim(),
        content: content.trim(),
        });

      setTitle("");
      setContent("");
      await loadEntries();
    } catch (error: any) {
      setError(
        error.response?.data?.detail ||
          "Failed to save journal entry."
      );
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="journal-page">
      <div className="journal-layout">
        <section className="panel">
          <div className="panel-header">
            <p className="eyebrow">Reflect</p>
            <h1>My Journal</h1>
          </div>

          <form className="journal-form" onSubmit={handleSubmit}>
            <div className="form-field">
              <label htmlFor="journal-title">Entry title</label>
              <input
                id="journal-title"
                type="text"
                value={title}
                onChange={(event) => setTitle(event.target.value)}
                placeholder="Entry title"
                maxLength={255}
                required
              />
            </div>

            <div className="form-field">
              <label htmlFor="journal-content">Story or reflection</label>
              <textarea
                id="journal-content"
                value={content}
                onChange={(event) => setContent(event.target.value)}
                placeholder="Write something..."
                rows={8}
              />
            </div>

            {error && <p className="error-message">{error}</p>}

            <div className="compose-actions">
              <button
                className="primary-button"
                type="submit"
                disabled={saving || !title.trim() || !content.trim()}
              >
                {saving ? "Saving..." : "Save Entry"}
              </button>
            </div>
          </form>
        </section>

        <aside className="panel">
          <div className="panel-header">
            <p className="eyebrow">Archive</p>
            <h2>Previous Entries</h2>
          </div>

          {loading ? (
            <p className="empty-state">Loading journal entries...</p>
          ) : entries.length === 0 ? (
            <p className="empty-state">No journal entries yet.</p>
          ) : (
            <div className="entry-list">
              {entries.map((entry) => (
                <article className="entry-card" key={entry.id}>
                  <h3>{entry.title}</h3>
                  <p>{entry.content}</p>
                  <small className="entry-meta">
                    {new Date(entry.created_at).toLocaleString()}
                  </small>
                </article>
              ))}
            </div>
          )}
        </aside>
      </div>
    </div>
  );
}

export default Journal;