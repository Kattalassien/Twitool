import os
import sys
import json
import csv
import re
from pathlib import Path

OUTPUT_DIR = "output/"
Path(OUTPUT_DIR).mkdir(exist_ok=True, exist_ok=True)

# Archive adapter

def parse_tweet_js(filepath):
    """Parse tweet.js file format."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
}
###parse_twitterArchive categories include}