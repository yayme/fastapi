from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
##database setup
SQLALCHEMY_DATABASE_URL ="sqlite:///./tasks.db"
engine = create_engine (SQLALCHEMY_DATABASE_URL, connect_args ={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind=engine)
Base = declarative_base()
##task model
class TaskDB(Base):
    __tablename__ = "tasks"
    id=Column(Integer,primary_key=True, index=True)
    name = Column(String,index=True)
    deadline= Column(String)

##create tables
Base.metadata.create_all(bind=engine)
app =FastAPI()

from pydantic import BaseModel

@app.post('/tasks/')

def add_task( task: Task):
    db=SessionLocal()
    db_task = TaskDB(name= task.name,deadline= task.deadline)
    db.add(db_task)
    db.commit()
    db.refresh(db_task) ## this loads the new id and data from the db
    db.close()
    return {"name": db_task.name, "deadline": db_task.deadline, "id":db_task.id}

@app.get('/tasks/')
def list_tasks():
    db= SessionLocal()
    tasks= db.query(TaskDB).all()
    dict_list=[]
    for task in tasks:
        dict_list.append({"name": task.name, "deadline": task.deadline, "id":task.id})
    db.close()
    return dict_list
@app.get('/tasks/{id}')
def get_task(id: int):

    db= SessionLocal()
    task= db.query(TaskDB).get(id)
    db.close()
    if task !=None :
        return {"id": task.id, "name": task.name, "deadline": task.deadline}
    else:
        return {"task not found"}

@app.put('/tasks/{id}')
def update_task( id:int,modified_task: Task):
    db=SessionLocal()
    task= db.query(TaskDB).get(id)
    if task!= None:
        task.name, task.deadline = modified_task.name, modified_task.deadline
        db.commit()
        db.close()
        return {"id": task.id, "name": task.name, "deadline": task.deadline}
    else:
        db.close()
        return {"message" : "task not found"}
@app.delete('/tasks/{id}')
def delete_task (id: int):
    db=SessionLocal()
    task= db.query(TaskDB).get(id)
    if task!= None:
        
        db.delete(task)
        db.commit()
        db.close()
        return {"id": task.id, "name": task.name, "deadline": task.deadline}
    else:
        db.close()
        return {"message" : "task not found"}



