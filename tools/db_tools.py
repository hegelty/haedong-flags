import sqlite3

conn = sqlite3.connect('db.sqlite3', check_same_thread=False)


def db_init():
    curs = conn.cursor()
    curs.execute('''
    CREATE TABLE IF NOT EXISTS user (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        student_id TEXT NOT NULL,
        score INTEGER NOT NULL,
        solved INTEGER NOT NULL,
        solved_oobal TEXT NOT NULL
    )
    ''')
    curs.execute('''
    CREATE TABLE IF NOT EXISTS problem (
    id INTEGER PRIMARY KEY,
    answer TEXT NOT NULL,
    score INTEGER NOT NULL,
    message TEXT NOT NULL
    )
    ''')
    curs.execute('''
    CREATE TABLE IF NOT EXISTS problem_oobal (
    id INTEGER PRIMARY KEY,
    answer TEXT NOT NULL,
    score INTEGER NOT NULL,
    message TEXT NOT NULL
    )
    ''')
    curs.execute('''
    CREATE TABLE IF NOT EXISTS history (
    id text NOT NULL,
    name text NOT NULL,
    student_id text NOT NULL,
    problem_id INTEGER NOT NULL,
    problem_type TEXT NOT NULL,
    time time NOT NULL
    )''')
    conn.commit()


def get_conn():
    return conn