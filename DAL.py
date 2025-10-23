import sqlite3
import os

DATABASE_FILE = 'projects.db'

def get_db_connection():
    """Get a database connection."""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database and create the projects table."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create the projects table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            image_file_name TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

def get_all_projects():
    """Retrieve all projects from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM projects ORDER BY id DESC')
    projects = cursor.fetchall()
    
    conn.close()
    return projects

def add_project(title, description, image_file_name):
    """Add a new project to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO projects (title, description, image_file_name)
        VALUES (?, ?, ?)
    ''', (title, description, image_file_name))
    
    conn.commit()
    conn.close()

def delete_project(project_id):
    """Delete a project by its ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM projects WHERE id = ?', (project_id,))
    
    conn.commit()
    conn.close()

def get_project_by_id(project_id):
    """Get a specific project by its ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM projects WHERE id = ?', (project_id,))
    project = cursor.fetchone()
    
    conn.close()
    return project
