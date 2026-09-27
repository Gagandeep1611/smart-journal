from datetime import datetime

from pydantic import BaseModel, Field


class JournalEntryCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    content: str = Field(min_length=1)


class JournalEntryUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )
    content: str | None = Field(
        default=None,
        min_length=1,
    )


class JournalEntryResponse(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class JournalChatRequest(BaseModel):
    question: str


class JournalChatSource(BaseModel):
    journal_entry_id: int
    title: str
    created_at: datetime


class JournalChatResponse(BaseModel):
    answer: str
    sources: list[JournalChatSource]
