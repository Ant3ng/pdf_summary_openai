import os

import openai
from tqdm import tqdm

from step_01 import *
from step_02 import *


# Step 3: Summarize each of the chunks
def summarize_text(text):
    # APIキーの設定
    openai.api_key = os.environ["OPENAI_API_KEY"]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"Summarize the following text:\n{text}. Reminder: Summarize the texts",
            }
        ],
        temperature=0.0,
    )

    summary = response.choices[0]["message"]["content"].strip()
    return summary


# Step 4: Merge all of the chunks into one text file
def merge_chunks(chunks):
    merged_text = " ".join(chunks)
    return merged_text


# Step 5: Write a new summary from the merged chunks of text
def write_summary(summary, output_path):
    with open(output_path, "w") as f:
        f.write(summary)


if __name__ == "__main__":
    print(sys.argv[1])
    text = convert_pdf_to_text(sys.argv[1])
    chunks = slice_text_into_chunks(text)
    print(f"number of chunks: {len(chunks)}")
    summaries = [summarize_text(chunk) for chunk in tqdm(chunks)]
    merged_text = merge_chunks(summaries)
    write_summary(merged_text, "summary.txt")
