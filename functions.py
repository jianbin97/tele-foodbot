import re
from urllib.parse import urlparse

def clean_text(text, replace, replacement, url=False):
    if url:
        text = urlparse(text).path

    for i in range(len(replace)):
        c = replace[i]
        r = replacement[i]
        text = text.replace(c, r)
    
    text = text.lower()
    return text
