from datetime import datetime, timezone
from typing import Optional, Literal
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, JSON
from pydantic import EmailStr


class FormRequest(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    name: str
    email: str
    phone: Optional[str] = None
    item: str

    # Store the list as JSON in MySQL
    options: list = Field(
        default_factory=list,
        sa_column=Column(JSON, nullable=False, default=list)
    )

    dependent_name: Optional[str] = None
    dependent_age: Optional[int] = None
    pdf_path: Optional[str] = None

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class FormCreate(SQLModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None

    item: Literal[
        "Choice 1", "Choice 2", "Choice 3", "Choice 4"
    ] = "Choice 1"

    options: list[Literal[
        "Option 1", "Option 2", "Option 3"
    ]] = Field(default_factory=list)

    dependent_name: Optional[str] = None
    dependent_age: Optional[int] = Field(default=None, ge=0, le=150)
