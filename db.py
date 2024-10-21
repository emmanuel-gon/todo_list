from sqlmodel import Field, Session, SQLModel, create_engine, select

sqlite_file_name = "todo.db"
sqlite_url = f'sqlite:///{sqlite_file_name}'

connect_args = {"check_same_thread":False}

engine = create_engine(sqlite_url, connect_args=connect_args)

