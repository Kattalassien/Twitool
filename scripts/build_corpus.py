import os
import sys
import json
import csv
from pathlib import Path
from typing import List
import re

OUTPUT_DIR = "output/"
Path(OUTPUT_DIR).mkdir(exist_ok=True)

# Common cleaning function
def clean_text(text: str) -> str:
    text = re.sub(r'https?://\S+', '', text)  # Remove URLs
    text = re.sub(r'@\w+', '', text)  # Remove mentions
    text = re.sub(r'\s+', ' ', text).strip()  # Normalize whitespace
    return text

def combine_corpora(raw_files: List[str], output_clean_csv: str):
    combined = []
    for file in raw_files:
        with open(file, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    data = json.loads(line)
                    cleaned_text = clean_text(data.get("text", ""))
                    combined.append({
                        "id": data.get("id"),
                        "created_at": data.get("created_at"),
                        "text": cleaned_text,
                        "source": data.get("source_type"),
                    })
                except json.JSONDecodeError as e:
                    print(f"Warning: Could not process a line in {file} - {e}")

    # Write to a cleaned CSV
    with open(output_clean_csv, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["id", "created_at", "text", "source"])
        writer.writeheader()
        writer.writerows(combined)
    print(f"Combined corpus written to {output_clean_csv}.")

if __name__ == "__main__":
    raw_tweets = os.path.join(OUTPUT_DIR, "raw_tweets.jsonl")
    raw_likes = os.path.join(OUTPUT_DIR, "raw_likes.jsonl")
    output_csv = os.path.join(OUTPUT_DIR, "corpus_combined.csv")

    raw_files = [file for file in [raw_tweets, raw_likes] if os.path.exists(file)]
    if not raw_files:
        print("No raw data files found to combine.")
        sys.exit(1)

    combine_corpora(raw_files, output_csv)