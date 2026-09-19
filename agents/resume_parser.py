from pathlib import Path
from pypdf import PdfReader
from docx import Document


def extract_text_from_resume(uploaded_file):
    """
    Extract text from an uploaded PDF or DOCX resume.
    """

    file_name = uploaded_file.name.lower()

    # PDF
    if file_name.endswith(".pdf"):

        reader = PdfReader(uploaded_file)

        text = []

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text.append(page_text)

        return "\n".join(text)

    # DOCX
    elif file_name.endswith(".docx"):

        document = Document(uploaded_file)

        text = []

        for paragraph in document.paragraphs:

            if paragraph.text.strip():
                text.append(paragraph.text)

        return "\n".join(text)

    else:

        raise ValueError(
            "Unsupported file type. Please upload a PDF or DOCX resume."
        )