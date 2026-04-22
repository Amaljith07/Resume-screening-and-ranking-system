import pdfplumber
import docx

def load_text(file):
    if file.name.endswith(".pdf"):
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    elif file.name.endswith(".docx"):
        doc = docx.Document(file)
        return " ".join([p.text for p in doc.paragraphs])

    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")

    else:
        return ""
