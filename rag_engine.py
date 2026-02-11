import json
from sentence_transformers import SentenceTransformer
from db import get_resume_db

embed_model = SentenceTransformer("all-MiniLM-L6-v2")

def flatten_json(data):
    parts = []
    for k, v in data.items():
        try:
            if isinstance(v, (list, dict)):
                parts.append(json.dumps(v, ensure_ascii=False))
            else:
                parts.append(str(v))
        except Exception:
            parts.append(str(v))
    return " ".join(parts)

def chunk_text(text, chunk_size=500):
    if not isinstance(text, str):
        text = str(text)
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

def store_resume_and_chunks(data):
    conn = get_resume_db()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO resumes (name, email, phone, education, skills, experience, projects)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING resume_id
        """, (
            data.get("name", ""),
            data.get("email", ""),
            data.get("phone", ""),
            json.dumps(data.get("education", []), ensure_ascii=False),
            json.dumps(data.get("skills", []), ensure_ascii=False),
            json.dumps(data.get("experience", []), ensure_ascii=False),
            json.dumps(data.get("projects", []), ensure_ascii=False),
        ))
        resume_id = cur.fetchone()[0]

        text = flatten_json(data)
        chunks = chunk_text(text)

        for chunk in chunks:
            emb = embed_model.encode(chunk).tolist()
            cur.execute(
                "INSERT INTO rag_chunks (resume_id, content, embedding) VALUES (%s, %s, %s)",
                (resume_id, chunk, emb)
            )

        conn.commit()
        return resume_id
    except Exception as e:
        conn.rollback()
        raise RuntimeError(f"Failed to store resume: {e}")
    finally:
        cur.close()
        conn.close()

def rag_query(question, top_k=3, return_raw=False):
    conn = get_resume_db()
    cur = conn.cursor()
    q_emb = embed_model.encode(question).tolist()
    cur.execute("""
        SELECT r.resume_id, r.name, r.email, r.education, c.content
        FROM rag_chunks c
        JOIN resumes r ON r.resume_id = c.resume_id
        ORDER BY c.embedding <-> %s::vector
        LIMIT %s
    """, (q_emb, top_k))
    docs = [(row[0], row[1], row[2], row[3], row[4]) for row in cur.fetchall()]
    cur.close()
    conn.close()
    return docs if return_raw else docs
