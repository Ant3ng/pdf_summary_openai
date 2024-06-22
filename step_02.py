import re
from step_01 import *
from tqdm import tqdm

# Step 2: Slice lots of sentences in texts into chunks. Limit of chatgpt is 4000 characters in each use.
def slice_text_into_chunks(text, max_chunk_size=15000):
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    chunks = []
    current_chunk = ''
    for sentence in tqdm(sentences):
        if len(current_chunk) + len(sentence) <= max_chunk_size:
            current_chunk += sentence
        else:
            chunks.append(current_chunk)
            current_chunk = sentence
    if current_chunk:
        chunks.append(current_chunk)
    return chunks

if __name__ == "__main__":
    print(sys.argv[1])
    text = convert_pdf_to_text(sys.argv[1])
    chunks = slice_text_into_chunks(text)
    print(chunks)
