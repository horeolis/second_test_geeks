import sqlite3
from config import path_db
from db import queries


def init_db():
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.create_table)
    conn.commit()
    conn.close()


def add_task_db(task, quantity=1):
    with sqlite3.connect(path_db) as conn:
        cursor = conn.cursor()
        cursor.execute(queries.insert_task, (task, quantity))
        task_id = cursor.lastrowid

    return task_id


def update_task(task_id, new_task=None, completed=None):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    if new_task is not None:
        cursor.execute(queries.update_task, (new_task, task_id))
    elif completed is not None:
        cursor.execute(queries.update_task_completed, (completed, task_id))
    conn.commit()
    conn.close()


def delete_task_db(task_id: int):
    with sqlite3.connect(path_db) as conn:
        cursor = conn.cursor()
        cursor.execute(queries.delete_task, (task_id,))
        conn.commit()


def clear_completed():
    with sqlite3.connect(path_db) as conn:
        cursor = conn.cursor()
        cursor.execute(queries.delete_completed)
        conn.commit()


def get_tasks(filter_type="all"):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()

    if filter_type == "all":
        cursor.execute(queries.select_tasks)
    elif filter_type == "uncompleted":
        cursor.execute(queries.select_tasks_uncompleted)
    elif filter_type == "completed":
        cursor.execute(queries.select_tasks_completed)

    tasks = cursor.fetchall()
    conn.close()
    return tasks