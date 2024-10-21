from typing import Annotated

from datetime import datetime

from fastapi import FastAPI, Depends, HTTPException, Query

from sqlmodel import Field, Session, SQLModel, create_engine, select

from models import Tasks
#Table creation - Create Models
"""
class Tasks(SQLModel, table=True):
    id: int | None=Field(default=None, primary_key=True)
    task: str = Field(...)
    description : str
    date_creation: str = Field(default_factory=datetime.now)
    completed : bool = Field(default=False)
"""

#Create an Engine
sqlite_file_name = 'todo.db'
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread":False}
engine = create_engine(sqlite_url, connect_args=connect_args)

#Create the tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

#Create a Session Dependency
def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

#Main app

app = FastAPI()

#Create database and tables on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

#Create a task
@app.post("/task/")
def create_task(task: Tasks, session:SessionDep) -> Tasks:
    session.add(task) #Add task
    session.commit() #Commit on db
    session.refresh(task) #Refresh
    return task

#Read tasks. Limit and offset to paginate results
@app.get("/tasks/")
def read_task(session: SessionDep, offset: int=0, limit: Annotated[int, Query(le=100)]=100)->list[Tasks]:
    tasks = session.exec(select(Tasks).offset(offset).limit(limit)).all()
    return tasks
    
#Read one task
@app.get("/task/{task_id}")
def read_task(task_id: int, session: SessionDep) -> Tasks:
    task=session.get(Tasks, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

#Delete a task
@app.delete("/task/{task_id}")
def delete_task(task_id: int, session: SessionDep):
    task = session.get(Tasks, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    return{"ok":True}

@app.get("/")
async def home():
    return {"message":"Hi"}