from fastapi import FastAPI
app =FastAPI()
tasks=[]
from pydantic import BaseModel
class Task(BaseModel):
    name: str
    deadline: str
    id: int
@app.post('/tasks/')

def add_task( task: Task):
    tasks.append(task)
    return {"name": task.name, "deadline": task.deadline, "id":task.id}
@app.get('/tasks/')
def list_tasks():
    return tasks
@app.get('/tasks/{id}')
def get_task(id: int):
    for task in tasks:
        if task.id == id:
            return task
    return {"task not found"}

@app.put('/tasks/{id}')
def update_task( id:int,modified_task: Task):
    for i in range(len(tasks)):
        if id== tasks[i].id:
            tasks[i]=modified_task
            return modified_task
    return {"message" : "task not found"}
@app.delete('/tasks/{id}')
def delete_task (id: int):
    for task in tasks:
        if task.id==id:
            tasks.remove(task)
            return {"message": "successfully deleted task"}
    return {"message" : "failed to delete task"}


