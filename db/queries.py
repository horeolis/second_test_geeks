import sqlite3
from config import path_db


def get_connection():
    conn = sqlite3.connect(path_db)
    conn.row_factory = sqlite3.Row
    return conn


create_table = 'CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, quantity INTEGER DEFAULT 1, purchased INTEGER DEFAULT 0)'

insert_task = 'INSERT INTO items (name, quantity) VALUES (?, ?)'

select_tasks = 'SELECT id, name, quantity, purchased FROM items'

select_tasks_completed = 'SELECT id, name, quantity, purchased FROM items WHERE purchased = 1'

select_tasks_uncompleted = 'SELECT id, name, quantity, purchased FROM items WHERE purchased = 0'

update_task = 'UPDATE items SET name = ? WHERE id = ?'
update_task_completed = 'UPDATE items SET purchased = ? WHERE id = ?'

delete_task = 'DELETE FROM items WHERE id = ?'
delete_completed = 'DELETE FROM items WHERE purchased = 1'