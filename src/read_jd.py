from docx import Document

def read_jd(docx_path="data/job_description.docx"):
    doc = Document(docx_path)

    text = []

    for para in doc.paragraphs:
        if para.text.strip():
            text.append(para.text)

    return "\n".join(text)


if __name__ == "__main__":
    jd = read_jd()
    print(jd[:1000])   # Print first 1000 characters