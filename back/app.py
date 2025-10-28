from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash
from datetime import datetime
from init_db import get_db
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "database.db"

app = Flask(__name__)
CORS(app)  # 개발 단계: 프론트에서 오는 요청 허용

@app.route("/api/hello", methods = ["GET"])
def hello():
    user_id = request.args.get("user_id")
    print(user_id)
    if not user_id:
        return jsonify({"ok": False, "error": "user_id가 없습니다."}), 400

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT user_id, name, age, gender, school_type, school_name, grade 
        FROM users 
        WHERE user_id = ?
    """, (user_id,)) 
    row = cur.fetchone()
    conn.close()
    
    if not row:
        return jsonify({"ok": False, "error": "해당 사용자가 없습니다."}), 404

    return jsonify({
        "ok": True,
        "user": {
            "user_id": row["user_id"],
            "name": row["name"],
            "age": row["age"],
            "gender": row["gender"],
            "school_type": row["school_type"],
            "school_name": row["school_name"],
            "grade": row["grade"],
        }
    })
    # return jsonify({"msg": "hello from flask"})



@app.route("/api/signup", methods = ["POST"])
def signup():
    data = request.get_json()
    user_id = data.get("id")
    password = data.get("password")
    name = data.get("name")
    age = data.get("age")
    gender = data.get("gender")
    
    school_type = data.get("schoolType") 
    school_name = data.get("school")
    
    grade = data.get("grade")
    # rank = data.get("rank")

    # 2️⃣ 기본 검증
    if not all([user_id, password, name]):
        return jsonify({"ok": False, "error": "필수값 누락"}), 400

    # 3️⃣ 중복 체크
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (id TEXT PRIMARY KEY, password TEXT, name TEXT, age TEXT, gender TEXT, school_type TEXT, school_name TEXT, grade TEXT, rank TEXT, created_at TEXT)")
    cur.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
    if cur.fetchone():
        conn.close()
        return jsonify({"ok": False, "error": "이미 존재하는 ID입니다."}), 409

    print(data)
    # 4️⃣ 비밀번호 해시 후 저장
    pw_hash = generate_password_hash(password)
    cur.execute(
        "INSERT INTO users (user_id, password_hash, name, age, gender, school_type, school_name, grade, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (user_id, pw_hash, name, age, gender, school_type, school_name, grade, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

    # 5️⃣ 응답
    return jsonify({"ok": True, "message": "회원가입 완료", "user": {"id": user_id, "name": name}}), 201


@app.route("/api/user", methods=["GET"])
def get_user():
    # user_id = request.args.get("user_id")
    #if not user_id:
    #    return jsonify({"ok": False, "error": "user_id가 필요합니다."}), 400

    
    # conn = get_db()
    # cur = conn.cursor()
    # cur.execute("SELECT user_id, name, age, gender, school, grade, rank FROM users WHERE user_id = ?", (user_id,))
    # row = cur.fetchone()
    # conn.close()

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT user_id, name, age, gender, school, grade, rank FROM users WHERE user_id = test01")
    row = cur.fetchone()
    conn.close()
    
    if not row:
        return jsonify({"ok": False, "error": "해당 사용자가 없습니다."}), 404

    return jsonify({
        "ok": True,
        "user": {
            "user_id": row["user_id"],
            "name": row["name"],
            "age": row["age"],
            "gender": row["gender"],
            "school": row["school"],
            "grade": row["grade"],
            "rank": row["rank"]
        }
    })
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
