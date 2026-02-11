import re
from rag_engine import rag_query, chunk_text

def read_multiline_input(prompt="Paste job description (end with 'END'):\n"):
    """
    Reads multi-line input until the user types END.
    """
    print(prompt)
    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)
    return "\n".join(lines)

def extract_skills(text: str):
    skill_keywords = [
        "python", "fastapi", "django", "flask", "postgresql", "mysql",
        "mongodb", "sql", "pgvector", "semantic search", "aws", "azure", "gcp",
        "docker", "kubernetes", "rest", "api", "graphql", "java", "c++",
        "machine learning", "deep learning", "tensorflow", "pytorch"
    ]
    text_lower = text.lower()
    return [kw for kw in skill_keywords if kw in text_lower]

def preprocess_job_description(description: str, chunk_size=300):
    """
    Break down long job descriptions into smaller chunks for embedding/query.
    """
    description = re.sub(r"\s+", " ", description.strip())
    return chunk_text(description, chunk_size=chunk_size)

def choose_threshold():
    print("\n🎯 Choose a minimum match % threshold:")
    print("1. Show only highly qualified (≥90%)")
    print("2. Show strong candidates (≥70%)")
    print("3. Show moderate candidates (≥50%)")
    print("4. Show all candidates (≥0%)")
    print("5. Create new threshold")
    print("6. Quit")

    choice = input("👉 Enter option (1-6): ").strip()
    if choice == "1": return 90
    elif choice == "2": return 70
    elif choice == "3": return 50
    elif choice == "4": return 0
    elif choice == "5":
        try:
            return int(input("🔧 Enter your custom threshold %: ").strip())
        except ValueError:
            print("⚠️ Invalid input, defaulting to 0%.")
            return 0
    elif choice == "6":
        return "QUIT"
    else:
        print("⚠️ Invalid choice, defaulting to 0%.")
        return 0

def truncate(text, length=30):
    return (text[:length] + "...") if len(text) > length else text

def query_with_long_description(description: str, top_k=3, threshold=50):
    """
    Handles long job descriptions by chunking them and querying RAG DB.
    """
    chunks = preprocess_job_description(description)
    all_candidates = []

    for chunk in chunks:
        raw_chunks = rag_query(chunk, top_k=top_k, return_raw=True)
        required_skills = extract_skills(chunk)

        for (resume_id, name, email, education, content) in raw_chunks:
            matches = [skill for skill in required_skills if skill.lower() in content.lower()]
            match_percent = round((len(matches) / len(required_skills)) * 100, 2) if required_skills else 0

            all_candidates.append((resume_id, name, email, education, matches, match_percent))

    # Deduplicate by email
    unique_candidates = {}
    for cand in all_candidates:
        key = cand[2]  # email as unique identifier
        if key not in unique_candidates or cand[5] > unique_candidates[key][5]:
            unique_candidates[key] = cand

    # Apply threshold filter
    filtered = [c for c in unique_candidates.values() if c[5] >= threshold]
    filtered.sort(key=lambda x: x[5], reverse=True)
    return filtered

def main():
    print("🔍 Resume RAG Query Interface (Handles Long Job Descriptions)")
    print("Paste your job description below. Type 'END' on a new line when finished.")
    print("Or choose option 6 in the menu to quit.\n")

    while True:
        description = read_multiline_input()
        if description.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        try:
            threshold = choose_threshold()
            if threshold == "QUIT":
                print("👋 Goodbye!")
                break

            candidates = query_with_long_description(description, top_k=5, threshold=threshold)

            print(f"\n📊 Candidate Qualification Table (≥{threshold}% Match)\n")
            print("{:<10} | {:<20} | {:<30} | {:<30} | {:<30} | {:<10}".format(
                "ID", "Name", "Email", "Education", "Matched Skills", "Match %"))
            print("-"*140)

            if not candidates:
                print(f"⚠️ No candidates meet the {threshold}% threshold.")
            else:
                for cand in candidates:
                    print("{:<10} | {:<20} | {:<30} | {:<30} | {:<30} | {:<10}".format(
                        cand[0], cand[1], cand[2], truncate(str(cand[3])),
                        ", ".join(cand[4]) if cand[4] else "None",
                        f"{cand[5]}%"
                    ))

        except Exception as e:
            print(f"⚠️ Error while querying: {e}")

if __name__ == "__main__":
    main()
