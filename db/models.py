from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime


class Thread(SQLModel, table=True):
    id: str = Field(primary_key=True)
    subject: Optional[str] = None
    emails: List["Email"] = Relationship(back_populates="thread")


class Email(SQLModel, table=True):
    id: str = Field(primary_key=True)
    thread_id: str = Field(foreign_key="thread.id", index=True)
    
    from_: Optional[str] = Field(default=None, index=True)
    to: Optional[str] = Field(default=None, index=True)
    subject: Optional[str] = Field(default=None, index=True)
    date: Optional[datetime] = Field(default=None, index=True)
    snippet: Optional[str] = Field(default=None, index=True)
    body: Optional[str] = None
    
    is_read: bool = Field(default=False, index=True)
    labels: Optional[str] = Field(default=None, index=True)  # comma-separated string
    
    thread: Optional[Thread] = Relationship(back_populates="emails")


Email.model_rebuild()
