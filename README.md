# Stock Market Data Pipeline

## Overview
This project fetches real-time stock market data from an API, streams it to **Apache Kafka**, and then a **Kafka Consumer** reads the data and inserts it into a **PostgreSQL database**.

## Architecture
1. **Data Source:** Alpha Vantage API (Stock price updates every 5 minutes)
2. **Kafka Producer:** Reads stock data from the API and pushes it into a Kafka topic.
3. **Kafka Consumer:** Reads messages from the Kafka topic and inserts them into a PostgreSQL database.
4. **PostgreSQL Database:** Stores stock price data with timestamps to prevent duplicates.

## Technologies Used
- **Python** (requests, pandas, kafka-python, psycopg2)
- **Apache Kafka** (Producer & Consumer for real-time streaming)
- **PostgreSQL** (Database for storing stock data)
- **Docker** (For running Kafka & PostgreSQL services)

---

## Installation & Setup
### 1. Clone the Repository
```sh
git clone https://github.com/Rohith30062001/Kafka_Stock_Market.git
cd kafka_stock_market
```

### 2. Set Up Virtual Environment
```sh
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Start Kafka & PostgreSQL (Using Docker)
```sh
docker-compose up -d
```

### 5. Create PostgreSQL Table
```sql
CREATE TABLE stock_data (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    open DECIMAL(10,2) NOT NULL,
    high DECIMAL(10,2) NOT NULL,
    low DECIMAL(10,2) NOT NULL,
    close DECIMAL(10,2) NOT NULL,
    volume BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE (timestamp)
);
```

---

## Running the Application
### Start the Kafka Producer
```sh
python utils/producer.py
```
### Start the Kafka Consumer
```sh
python utils/consumer.py
```

---

## Files Structure
```
stock-data-pipeline/
│── producer.py        # Fetches stock data and sends to Kafka
│── consumer.py        # Reads from Kafka and inserts into PostgreSQL
│── requirements.txt   # Python dependencies
│── docker-compose.yml # Kafka & PostgreSQL setup
│── README.md          # Documentation
```

---

## Handling Duplicate Data
- The `timestamp` column in the database is marked as **UNIQUE**, ensuring old records are not duplicated.
- The **consumer script** checks if the record exists before inserting new data.

---

## Future Enhancements
✅ Add support for multiple stock symbols 📈
✅ Implement alert system for price fluctuations 🔔
✅ Visualize data with dashboards 📊

---
