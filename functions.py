import gzip
import os
import hashlib

os.makedirs("AllZipfile", exist_ok=True)

def write_html_direct_gzip(html_data, filename):
    filepath = f"AllZipfile/{filename}.gz"
    with gzip.open(filepath, "wt", encoding="utf-8") as f:
        f.write(html_data)

def read_gzip(filename):
    with gzip.open(filename, "rt", encoding="utf-8") as f:
        return f.read()

def make_hash(value):
    return hashlib.md5(value.encode()).hexdigest()