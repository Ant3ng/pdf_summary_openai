import time

import openai

from step_01 import *
from step_02 import *


def process_summary_and_save(chunks):
    # OpenAI APIキーを設定
    openai.api_key = os.environ["OPENAI_API_KEY"]

    # 要約された文章を保存するリストを作成
    summarized_texts = []

    # 要約が完了した文章のインデックスを保存するリストを作成
    completed_indexes = []

    # ループを開始する
    while len(chunks) > 0:
        print(f"rest of chunks: {len(chunks)}")

        # 要約する文章を取得する
        text = chunks[0]

        # OpenAI APIに要約をリクエストする
        try:
            summarized_text = (
                openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "user",
                            "content": f"Summarize the following text:\n{text}. Reminder: Summarize the texts",
                        }
                    ],
                    temperature=0.0,
                )
                .choices[0]["message"]["content"]
                .strip()
            )

            # 要約された文章を保存する
            summarized_texts.append(summarized_text)

            # 要約が完了した文章のインデックスを保存する
            completed_indexes.append(0)

        except Exception as e:
            # APIエラーが発生した場合、10秒待機して再試行する
            print("APIエラーが発生しました。10秒待機します。")
            print(e)
            time.sleep(10)
            continue

        # 要約が完了した文章をリストから削除する
        chunks.pop(0)

        # 要約が完了した文章のインデックスをリストから削除する
        completed_indexes.pop(0)

        # 要約が完了していない文章のインデックスを更新する
        for i in range(len(completed_indexes)):
            completed_indexes[i] -= 1

        # 要約が完了していない文章を別のリストに保存する
        new_original_texts = []
        for i in range(len(chunks)):
            if i not in completed_indexes:
                new_original_texts.append(chunks[i])

        # 要約が完了していない文章のリストを更新する
        chunks = new_original_texts

        # 要約された文章を保存する
        with open("summarized_texts.txt", "a") as f:
            f.write(summarized_text + "\n")

        print("要約が完了しました。")


if __name__ == "__main__":
    print(sys.argv[1])
    text = convert_pdf_to_text(sys.argv[1])
    chunks = slice_text_into_chunks(text)
    print(f"number of chunks: {len(chunks)}")

    process_summary_and_save(chunks)
