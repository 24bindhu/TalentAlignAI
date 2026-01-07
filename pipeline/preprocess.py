import re

def clean_text(text: str) -> str:
    """
    Cleans and normalizes input text.
    - Lowercases text
    - Removes extra spaces
    """
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()
