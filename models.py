from datetime import datetime
from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select

#Table creation - Create Models

class Tasks(SQLModel, table=True):
    id: int | None=Field(default=None, primary_key=True)
    task: str = Field(...)
    description : str
    date_creation: str = Field(default_factory=datetime.now)
    completed : bool = Field(default=False)

class Update_Task(SQLModel):
    description: Optional[str]=None
    completed: Optional[bool]=None