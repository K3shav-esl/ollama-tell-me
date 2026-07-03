import pymupdf4llm
import re

def pdf_to_markdown(pdf_path: str) -> str:
    md_text = pymupdf4llm.to_markdown(pdf_path)
    return clean_markdown(md_text)

def clean_markdown(text: str) -> str:
    # Remove null bytes
    text = text.replace('\x00', '')
    
    # Remove lines that are clearly garbled math (high ratio of non-ASCII/non-printable)
    lines = text.split('\n')
    clean_lines = []
    for line in lines:
        if not line.strip():
            clean_lines.append(line)
            continue
        # Count non-standard characters
        weird_chars = sum(1 for c in line if ord(c) > 127 or (ord(c) < 32 and c not in '\t\n\r'))
        ratio = weird_chars / max(len(line), 1)
        # Drop lines where more than 40% of characters are garbage
        if ratio < 0.4:
            clean_lines.append(line)
        else:
            # Replace with a placeholder so LLM knows something was here
            clean_lines.append('[EQUATION - could not be extracted from PDF]')
    
    # Collapse multiple consecutive placeholders into one
    text = '\n'.join(clean_lines)
    text = re.sub(r'(\[EQUATION - could not be extracted from PDF\]\n){2,}', 
                  '[EQUATIONS - could not be extracted from PDF]\n', text)
    return text