# back/init_db.py
import sqlite3
from pathlib import Path
from flask import g

DB_PATH = Path(__file__).parent / "data" / "database.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 1) 테이블 생성 (없으면 생성)
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id       TEXT PRIMARY KEY,          -- 로그인 아이디(고유)
        password_hash TEXT NOT NULL,             -- 비밀번호 해시
        name          TEXT NOT NULL,             -- 이름
        age           INTEGER,                   -- 나이
        gender        TEXT,                      -- 성별
        school_type   TEXT,                      -- 학교
        school_name   TEXT,
        grade         TEXT,                      -- 학년
        rank          INTEGER,                   -- 랭킹(선택)
        created_at    TEXT DEFAULT (datetime('now'))  -- 생성 시각
    );
    """)
    
    #회원 개인정보
    cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,             
        age INTEGER, 
        gender TEXT,  
        school TEXT,
        grade INTEGER,
        head_turn_count INTEGER DEFAULT 0
    );
    """)
    
    # cur.execute("""
    # INSERT OR REPLACE INTO users 
    # (user_id, password_hash, name, age, gender, school_name, grade)
    # VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    # """, ("test01", "test", "홍길동", 22, "남성", "테스트대학교", "2학년", 5))

    
    conn.commit()
    conn.close()
    print(f"DB 초기화 완료: {DB_PATH}")

if __name__ == "__main__":
    init_db()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('data/database.db')
        db.row_factory = sqlite3.Row
    return db