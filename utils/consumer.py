from kafka import KafkaConsumer
import psycopg2
import json

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="learning_db",
    user="myuser",
    password="mypassword"
)
cursor = conn.cursor()

# Kafka Consumer Setup
consumer = KafkaConsumer(
    "stock-data",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda v: json.loads(v.decode('utf-8')),
    auto_offset_reset="earliest",
    enable_auto_commit=True
)

for message in consumer:
    data = message.value
    timestamp = data.get("timestamp")

    # Check if the record already exists
    cursor.execute("SELECT 1 FROM stock_data WHERE timestamp = %s", (timestamp,))
    exists = cursor.fetchone()

    if not exists:  # Insert only if new
        cursor.execute(
            "INSERT INTO stock_data (timestamp, open, high, low, close, volume) VALUES (%s, %s, %s, %s, %s, %s)",
            (data["timestamp"], data["open"], data["high"], data["low"], data["close"], data["volume"])
        )
        conn.commit()
        print(f"Inserted: {data}")

# Close connection
cursor.close()
conn.close()
