import os
import requests
import pandas as pd
import json
import time
from kafka import KafkaProducer

# Environment Variables (Modify as needed)
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
TOPIC = os.getenv("KAFKA_TOPIC", "stock-data")
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "demo")
SYMBOL = os.getenv("STOCK_SYMBOL", "IBM")
INTERVAL = os.getenv("STOCK_INTERVAL", "5min")
API_URL = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={SYMBOL}&interval={INTERVAL}&outputsize=full&apikey={API_KEY}"

# Kafka Producer Setup
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# Track last processed timestamp to avoid duplicates
last_timestamp = None

def fetch_stock_data():
    """Fetch stock data from API and return as a DataFrame."""
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()  # Raise an error for failed responses
        data = response.json()
        time_series = data.get(f"Time Series ({INTERVAL})", {})

        if not time_series:
            print("No data received from API.")
            return pd.DataFrame()

        df = pd.DataFrame.from_dict(time_series, orient="index")
        df.columns = ["open", "high", "low", "close", "volume"]
        df.index = pd.to_datetime(df.index)  # Convert index to datetime
        df = df.astype({"open": float, "high": float, "low": float, "close": float, "volume": int})
        return df.sort_index()  # Sort from oldest to newest

    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return pd.DataFrame()  # Return empty DataFrame on failure

def stream_data():
    """Fetch and send new stock data to Kafka."""
    global last_timestamp  # Keep track of the latest processed data

    while True:
        df = fetch_stock_data()

        if df.empty:
            print("No new data. Retrying in 10 seconds...")
            time.sleep(10)
            continue

        for timestamp, row in df.iterrows():
            # Skip already processed timestamps
            if last_timestamp and timestamp <= last_timestamp:
                continue

            message = {
                "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "open": row["open"],
                "high": row["high"],
                "low": row["low"],
                "close": row["close"],
                "volume": row["volume"]
            }

            try:
                future = producer.send(TOPIC, message)
                record_metadata = future.get(timeout=10)
                print(f"Sent to {record_metadata.topic} at offset {record_metadata.offset}")
                last_timestamp = timestamp  # Update last processed timestamp
            except Exception as e:
                print(f"Error sending message: {e}")

        print("Sleeping for 5 seconds before fetching new data...")
        time.sleep(5)  # Simulate real-time streaming

if __name__ == "__main__":
    try:
        print("Starting Kafka Producer...")
        stream_data()
    except KeyboardInterrupt:
        print("\nStopping producer...")
    finally:
        producer.close()
        print("Producer closed.")
