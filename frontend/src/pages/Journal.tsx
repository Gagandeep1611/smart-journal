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

  const [editingId, setEditingId] = useState<number | null>(null);
  const [editTitle, setEditTitle] = useState("");
  const [editContent, setEditContent] = useState("");
  const [updating, setUpdating] = useState(false);
  const [deletingId, setDeletingId] = useState<number | null>(null);

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

  const handleSubmit = async (
    event: FormEvent<HTMLFormElement>
  ) => {
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

  const startEditing = (entry: JournalEntry) => {
    setEditingId(entry.id);
    setEditTitle(entry.title);
    setEditContent(entry.content);
    setError("");
  };

  const cancelEditing = () => {
    setEditingId(null);
    setEditTitle("");
    setEditContent("");
  };

  const handleUpdate = async (
    event: FormEvent<HTMLFormElement>
  ) => {
    event.preventDefault();

    if (
      editingId === null ||
      !editTitle.trim() ||
      !editContent.trim()
    ) {
      return;
    }

    try {
      setUpdating(true);
      setError("");

      await apiClient.put(`/journal/${editingId}`, {
        title: editTitle.trim(),
        content: editContent.trim(),
      });

      cancelEditing();
      await loadEntries();
    } catch (error: any) {
      setError(
        error.response?.data?.detail ||
          "Failed to update journal entry."
      );
    } finally {
      setUpdating(false);
    }
  };

  const handleDelete = async (entryId: number) => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this journal entry?"
    );

    if (!confirmed) {
      return;
    }

    try {
      setDeletingId(entryId);
      setError("");

      await apiClient.delete(`/journal/${entryId}`);

      if (editingId === entryId) {
        cancelEditing();
      }

      await loadEntries();
    } catch (error: any) {
      setError(
        error.response?.data?.detail ||
          "Failed to delete journal entry."
      );
    } finally {
      setDeletingId(null);
    }
  };

  return (
    <div>
      <h1>My Journal</h1>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={title}
          onChange={(event) => setTitle(event.target.value)}
          placeholder="Entry title"
          maxLength={255}
          required
        />

        <br />

        <textarea
          value={content}
          onChange={(event) => setContent(event.target.value)}
          placeholder="Write something..."
          rows={8}
          required
        />

        <br />

        <button
          type="submit"
          disabled={
            saving ||
            !title.trim() ||
            !content.trim()
          }
        >
          {saving ? "Saving..." : "Save Entry"}
        </button>
      </form>

      {error && <p>{error}</p>}

      <hr />

      <h2>Previous Entries</h2>

      {loading ? (
        <p>Loading journal entries...</p>
      ) : entries.length === 0 ? (
        <p>No journal entries yet.</p>
      ) : (
        entries.map((entry) => (
          <article key={entry.id}>
            {editingId === entry.id ? (
              <form onSubmit={handleUpdate}>
                <input
                  type="text"
                  value={editTitle}
                  onChange={(event) =>
                    setEditTitle(event.target.value)
                  }
                  maxLength={255}
                  required
                />

                <br />

                <textarea
                  value={editContent}
                  onChange={(event) =>
                    setEditContent(event.target.value)
                  }
                  rows={8}
                  required
                />

                <br />

                <button
                  type="submit"
                  disabled={
                    updating ||
                    !editTitle.trim() ||
                    !editContent.trim()
                  }
                >
                  {updating ? "Updating..." : "Save Changes"}
                </button>

                <button
                  type="button"
                  onClick={cancelEditing}
                  disabled={updating}
                >
                  Cancel
                </button>
              </form>
            ) : (
              <>
                <h3>{entry.title}</h3>

                <p>{entry.content}</p>

                <small>
                  {new Date(
                    entry.created_at
                  ).toLocaleString()}
                </small>

                <br />

                <button
                  type="button"
                  onClick={() => startEditing(entry)}
                >
                  Edit
                </button>

                <button
                  type="button"
                  onClick={() =>
                    handleDelete(entry.id)
                  }
                  disabled={deletingId === entry.id}
                >
                  {deletingId === entry.id
                    ? "Deleting..."
                    : "Delete"}
                </button>
              </>
            )}

            <hr />
          </article>
        ))
      )}
    </div>
  );
}

export default Journal;