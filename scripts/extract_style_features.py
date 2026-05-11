import os
import sys
import json
import csv
from collections import Counter
from pathlib import Path
from typing import List, Dict
import re

OUTPUT_DIR = "output/"
Path(OUTPUT_DIR).mkdir(exist_ok=True)

def extract_features(input_file: str, output_file: str):
    with open(input_file, "r", encoding="utf-8") as f:
        data = csv.DictReader(f)
        word_counter = Counter()
        bigram_counter = Counter()
        lengths = []
        punctuation_count = Counter()
        for row in data:
            text = row['text']
            words = text.split()
            word_counter.update(words)
            bigrams = zip(words, words[1:])
            bigram_counter.update(bigrams)
            lengths.append(len(words))
            punctuation_count.update(re.findall(r'[.!?",:;]', text))

    # Calculate summary statistics
    summary = {
        "most_common_unigrams": word_counter.most_common(20),
        "most_common_bigrams": bigram_counter.most_common(20),
        "average_length": sum(lengths) / len(lengths) if lengths else 0,
        "top_punctuation": punctuation_count
    }

    with open(output_file, "w", encoding="utf-8") as out:
        json.dump(summary, out, indent=4)

    print(f"Style features extracted: {output_file}")

if __name__ == "__main__":
    input_csv = os.path.join(OUTPUT_DIR, "corpus_combined.csv")
    output_json = os.path.join(OUTPUT_DIR, "style_features.json")

    if not os.path.exists(input_csv):
        print(f"Input file not found: {input_csv}")
        sys.exit(1)

    extract_features(input_csv, output_json)