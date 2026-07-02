import pymupdf4llm

def pdf_to_markdown(pdf_path: str) -> str:
    md_text = pymupdf4llm.to_markdown(pdf_path)
    return md_text