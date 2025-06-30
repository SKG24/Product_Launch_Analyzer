import csv
import random
from datetime import datetime, timedelta
import os

# Directory to save fallback CSVs
os.makedirs("fallback_data", exist_ok=True)

products = ["iPhone 15", "Galaxy S24", "Pixel 8", "OnePlus 12", "Nothing Phone"]

sample_texts = [
    "I just bought the {} and it's amazing!",
    "Not happy with the {} battery life.",
    "The {} camera quality is insane.",
    "Is anyone else having issues with the {}?",
    "Absolutely loving my new {}!",
    "The {} is totally worth the price.",
    "Thinking of switching to the {}.",
    "Best phone ever: {}",
    "Worst experience with {} so far.",
    "Unboxing my {} today!"
]

def generate_tweet(product, idx):
    now = datetime.now()
    tweet_time = now - timedelta(days=random.randint(0, 30))
    sentiment = round(random.uniform(-1, 1), 3)

    return {
        "id": str(1000000000000000000 + idx),
        "date": tweet_time.strftime("%Y-%m-%d %H:%M:%S"),
        "text": random.choice(sample_texts).format(product),
        "user": f"user_{random.randint(1000, 9999)}",
        "likes": random.randint(0, 500),
        "retweets": random.randint(0, 100),
        "sentiment": sentiment,
        "product": product
    }

def write_csv(product):
    path = f"fallback_data/{product.replace(' ', '_')}_fallback.csv"
    with open(path, "w", newline="") as csvfile:
        fieldnames = ["id", "date", "text", "user", "likes", "retweets", "sentiment", "product"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for idx in range(100):
            writer.writerow(generate_tweet(product, idx))
    print(f"✅ Saved: {path}")

for product in products:
    write_csv(product)
