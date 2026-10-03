import sqlite3
import os
import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "funobotz.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create learners table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS learners (
            learner_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            customer_id TEXT NOT NULL,
            starting_knowledge TEXT DEFAULT 'Beginner',
            active_character TEXT DEFAULT 'quacky',
            total_xp INTEGER DEFAULT 0,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create chat_history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            sender TEXT NOT NULL,
            message TEXT NOT NULL,
            character_id TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create quiz_logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quiz_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            question TEXT NOT NULL,
            selected_option INTEGER,
            is_correct INTEGER,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def save_learner(learner_id: str, name: str, age: int, customer_id: str, starting_knowledge: str, active_character: str, total_xp: int = 0):
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO learners (learner_id, name, age, customer_id, starting_knowledge, active_character, total_xp, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(learner_id) DO UPDATE SET
            name=excluded.name,
            age=excluded.age,
            customer_id=excluded.customer_id,
            starting_knowledge=excluded.starting_knowledge,
            active_character=excluded.active_character,
            total_xp=excluded.total_xp,
            updated_at=excluded.updated_at
    ''', (learner_id, name, age, customer_id, starting_knowledge, active_character, total_xp, datetime.datetime.now()))
    conn.commit()
    conn.close()

def log_chat_message(session_id: str, sender: str, message: str, character_id: str = None):
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO chat_history (session_id, sender, message, character_id, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', (session_id, sender, message, character_id, datetime.datetime.now()))
    conn.commit()
    conn.close()

def log_quiz_answer(session_id: str, question: str, selected_option: int, is_correct: bool):
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO quiz_logs (session_id, question, selected_option, is_correct, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', (session_id, question, selected_option, 1 if is_correct else 0, datetime.datetime.now()))
    conn.commit()
    conn.close()
