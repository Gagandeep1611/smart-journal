from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from smart_journal.models import JournalEmbedding
from smart_journal.services.embedding_service import generate_embedding
from smart_journal.rag.service import RAGService
from smart_journal.schemas.journal import (
    JournalChatRequest,
    JournalChatResponse,
)
from smart_journal.auth.dependencies import get_current_user
from smart_journal.db.database import get_db
from smart_journal.models import JournalEntry, User
from smart_journal.schemas.journal import (JournalEntryCreate,
                                           JournalEntryResponse,
                                           JournalEntryUpdate)

router = APIRouter(
    prefix="/journal",
    tags=["Journal"],
)


@router.post(
    "",
    response_model=JournalEntryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_journal_entry(
    entry_data: JournalEntryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    entry = JournalEntry(
        user_id=current_user.id,
        title=entry_data.title,
        content=entry_data.content,
    )

    db.add(entry)

    # Get the generated journal ID without committing yet.
    db.flush()

    embedding_text = f"{entry.title}\n{entry.content}"

    embedding = generate_embedding(embedding_text)

    journal_embedding = JournalEmbedding(
        journal_entry_id=entry.id,
        user_id=current_user.id,
        embedding=embedding,
    )

    db.add(journal_embedding)

    db.commit()
    db.refresh(entry)

    return entry

@router.get(
    "",
    response_model=list[JournalEntryResponse],
)
def get_journal_entries(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    entries = (
        db.query(JournalEntry)
        .filter(JournalEntry.user_id == current_user.id)
        .order_by(JournalEntry.created_at.desc())
        .all()
    )

    return entries


@router.get(
    "/{entry_id}",
    response_model=JournalEntryResponse,
)
def get_journal_entry(
    entry_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    entry = (
        db.query(JournalEntry)
        .filter(
            JournalEntry.id == entry_id,
            JournalEntry.user_id == current_user.id,
        )
        .first()
    )

    if entry is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Journal entry not found",
        )

    return entry


@router.put(
    "/{entry_id}",
    response_model=JournalEntryResponse,
)
def update_journal_entry(
    entry_id: int,
    entry_data: JournalEntryUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    entry = (
        db.query(JournalEntry)
        .filter(
            JournalEntry.id == entry_id,
            JournalEntry.user_id == current_user.id,
        )
        .first()
    )

    if entry is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Journal entry not found",
        )

    if entry_data.title is not None:
        entry.title = entry_data.title

    if entry_data.content is not None:
        entry.content = entry_data.content

    entry.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(entry)

    return entry


@router.delete(
    "/{entry_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_journal_entry(
    entry_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    entry = (
        db.query(JournalEntry)
        .filter(
            JournalEntry.id == entry_id,
            JournalEntry.user_id == current_user.id,
        )
        .first()
    )

    if entry is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Journal entry not found",
        )

    db.delete(entry)
    db.commit()

    return None

@router.post(
    "/chat",
    response_model=JournalChatResponse,
    status_code=status.HTTP_200_OK,
)
def chat_with_journal(
    request: JournalChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    rag_service = RAGService(db)

    answer = rag_service.answer_question(
        question=request.question,
        user_id=current_user.id,
    )

    return JournalChatResponse(
        answer=answer,
    )