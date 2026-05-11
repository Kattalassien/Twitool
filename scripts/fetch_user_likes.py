import argparse
import json
import os
from pathlib import Path
import tweepy
import requests

OUTPUT_DIR = "output/"
Path(OUTPUT_DIR).mkdir(exist_ok=True)

def fetch_likes_tweepy(username: str, limit: int):
    bearer_token = os.getenv("X_BEARER_TOKEN")
    if not bearer_token:
        print("Error: Missing Tweepy credentials.")
        exit(1)

    client = tweepy.Client(bearer_token=bearer_token)
    user = client.get_user(username=username)
    user_id = user.data.id
    likes = client.get_liked_tweets(user_id, tweet_fields=["created_at"], max_results=limit)
    output_file = Path(OUTPUT_DIR, "raw_likes.jsonl")
    with output_file.open("w", encoding="utf-8") as f:
        for tweet in likes.data:
            json.dump(tweet.data, f)
            f.write("\n")
    print(f"Fetched likes for {username} → {output_file}")

def fetch_likes_apify(username: str, limit: int, actor: str, token: str):
    url = f"https://api.apify.com/v2/acts/{actor}/runs?token={token}"
    payload = {"username": username, "limit": limit}
    res = requests.post(url, json=payload)
    if res.status_code != 201:
        print(f"Error: Apify failed with status {res.status_code}")
        exit(1)
    with Path(OUTPUT_DIR, "raw_likes.jsonl").open("w", encoding="utf-8") as f:
        json.dump(res.json(), f)
    print(f"Fetched likes for {username} → output/raw_likes.jsonl")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", required=True, help="Twitter username")
    parser.add_argument("--limit", required=True, help="Max likes to fetch")
    parser.add_argument("--backend", choices=["tweepy", "apify"], default="tweepy", help="Backend to use")
    args = parser.parse_args()

    if args.backend == "tweepy":
        fetch_likes_tweepy(args.username, args.limit)
    elif args.backend == "apify":
        apify_actor = os.getenv("APIFY_ACTOR")
        apify_token = os.getenv("APIFY_TOKEN")
        if not (apify_actor and apify_token):
            print("Error: Missing Apify credentials.")
            exit(1)
        fetch_likes_apify(args.username, args.limit, apify_actor, apify_token)