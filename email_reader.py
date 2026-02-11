import imaplib, email, os, fitz, docx
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
IMAP_SERVER = os.getenv("IMAP_SERVER")

def connect_gmail():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_USER, EMAIL_PASSWORD)
    mail.select("inbox")
    return mail

def extract_pdf_text(pdf_bytes):
    doc = fitz.open(stream=BytesIO(pdf_bytes), filetype="pdf")
    return "\n".join([page.get_text() for page in doc])

def extract_docx_text(doc_bytes):
    document = docx.Document(BytesIO(doc_bytes))
    return "\n".join([p.text for p in document.paragraphs])

def extract_resume_text(msg):
    for part in msg.walk():
        if part.get_content_maintype() == "multipart":
            continue
        if part.get("Content-Disposition") is None:
            continue
        filename = part.get_filename()
        if not filename:
            continue
        file_bytes = part.get_payload(decode=True)
        if filename.lower().endswith(".pdf"):
            return extract_pdf_text(file_bytes)
        elif filename.lower().endswith(".docx"):
            return extract_docx_text(file_bytes)
    return ""

def fetch_emails_with_resumes(mail, max_emails=50):
    _, messages = mail.search(None, '(UNSEEN)')
    email_ids = messages[0].split()[-max_emails:]
    resume_emails = []
    for e_id in email_ids:
        res, msg_data = mail.fetch(e_id, "(RFC822)")
        if res != "OK":
            continue
        msg = email.message_from_bytes(msg_data[0][1])
        for part in msg.walk():
            filename = part.get_filename()
            if filename and (filename.lower().endswith(".pdf") or filename.lower().endswith(".docx")):
                resume_emails.append(msg)
                break
    return resume_emails
