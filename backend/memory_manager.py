import sqlite3
import json

DB_PATH = "sentinel_memory.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cases (
            case_id TEXT PRIMARY KEY,
            type TEXT,
            status TEXT,
            name TEXT,
            location TEXT,
            clues TEXT,
            alerts TEXT,
            timeline TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_case(case_data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO cases (case_id, type, status, name, location, clues, alerts, timeline)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        case_data["case_id"],
        case_data["type"],
        case_data["status"],
        case_data.get("name", ""),
        case_data.get("location", ""),
        json.dumps(case_data.get("clues", [])),
        json.dumps(case_data.get("alerts", [])),
        json.dumps(case_data.get("timeline", []))
    ))
    conn.commit()
    conn.close()

def get_case(case_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cases WHERE case_id=?", (case_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "case_id": row[0],
            "type": row[1],
            "status": row[2],
            "name": row[3],
            "location": row[4],
            "clues": json.loads(row[5]),
            "alerts": json.loads(row[6]),
            "timeline": json.loads(row[7])
        }
    return None
def update_case(case_id, updates):
    existing = get_case(case_id)
    if not existing:
        return False

    updated_data = {
        "type": updates.get("type", existing["type"]),
        "status": updates.get("status", existing["status"]),
        "name": updates.get("name", existing["name"]),
        "location": updates.get("location", existing["location"]),
        "clues": json.dumps(existing["clues"] + updates.get("clues", [])),
        "alerts": json.dumps(existing["alerts"] + updates.get("alerts", [])),
        "timeline": json.dumps(existing["timeline"] + updates.get("timeline", []))
    }

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE cases SET type=?, status=?, name=?, location=?, clues=?, alerts=?, timeline=? WHERE case_id=?
    ''', (
        updated_data["type"],
        updated_data["status"],
        updated_data["name"],
        updated_data["location"],
        updated_data["clues"],
        updated_data["alerts"],
        updated_data["timeline"],
        case_id
    ))
    conn.commit()
    conn.close()
    return True
