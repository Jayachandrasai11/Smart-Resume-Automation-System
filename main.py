import email_reader, llm_client, rag_engine

def main():
    mail = email_reader.connect_gmail()
    resume_emails = email_reader.fetch_emails_with_resumes(mail)

    if not resume_emails:
        print("⚠️ No resumes found")
        mail.logout()
        return

    for idx, msg in enumerate(resume_emails, start=1):
        resume_text = email_reader.extract_resume_text(msg)
        if not resume_text:
            continue

        resume_json = llm_client.extract_json_gemini(resume_text)
        data = llm_client.safe_json_parse(resume_json)
        if data:
            data = llm_client.fallback_extract(resume_text, data)

        print("\n📌 Extracted Resume JSON:\n", data)

        if not (data.get("name") and data.get("email") and data.get("phone")):
            print("⚠️ Incomplete resume JSON, storing anyway for enrichment")

        rag_engine.store_resume_and_chunks(data)
        print(f"✅ Resume {idx} stored in resume_db")

    mail.logout()

if __name__ == "__main__":
    main()
