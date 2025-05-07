from fastapi import FastAPI, HTTPException
from db import get_connection
from models import Task

app = FastAPI()

@app.post("/tasks")
def create_task(task: Task):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, description, completed) VALUES (%s, %s, %s)",
                   (task.title, task.description, task.completed))
    conn.commit()
    return {"id": cursor.lastrowid, "message": "Task created"}

@app.get("/tasks")
def get_all():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks")
    return cursor.fetchall()

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    result = cursor.fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Not found")
    return result

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET title=%s, description=%s, completed=%s WHERE id=%s",
                   (task.title, task.description, task.completed, task_id))
    conn.commit()
    return {"message": "Task updated"}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=%s", (task_id,))
    conn.commit()
    return {"message": "Task deleted"}
