# Real-Time Weather Data Pipeline Using Apache Kafka and MongoDB

This project implements a real-time weather data pipeline using **Apache Kafka**, **MongoDB**, and the **OpenWeatherMap API**. The pipeline collects weather data from the OpenWeatherMap API, streams it via Apache Kafka, and stores the data in MongoDB for real-time storage and analysis.

## Overview

The project consists of the following key components:

1. **Weather Data Extraction (app.py)**: Extracts weather data for a specified city (e.g., Nairobi) from the OpenWeatherMap API and transforms the data.
2. **Kafka Producer (weather_producer.py)**: Sends the transformed weather data to a Kafka topic for real-time streaming.
3. **Kafka Consumer (weather_consumer.py)**: Consumes the streamed weather data from Kafka and stores it into MongoDB for analysis and storage.

## Requirements

- **Python 3.x** (Recommended version: 3.7+)
- **Apache Kafka** (with Zookeeper)
- **MongoDB**
- **Confluent Kafka Python library**
- **Pandas** for data transformation
- **OpenWeatherMap API key**

### Python Dependencies

You can install the required Python packages using `pip`:

```
pip install pymongo
requests
confluent_kafka
python-dotenv
pandas
```

## Set Up Kafka and MongoDB

### Apache Kafka Setup:

1. Follow the [Kafka Quickstart guide](https://kafka.apache.org/quickstart) to set up a Kafka broker on your machine.
2. Ensure **Zookeeper** is running, as Kafka requires it.
3. Create a Kafka topic (e.g., `weather_topic`) where the data will be published:

```
kafka-topics.sh --create --topic weather_topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```
## MongoDB Setup:

1. Set up a MongoDB instance locally or use a cloud MongoDB service like [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
2. Create a database (e.g., `weather_db`) to store the weather data.

## Get OpenWeatherMap API Key:

1. Sign up for an API key at [OpenWeatherMap](https://openweathermap.org/api).

## Create a `.env` file in the project root to store sensitive information:

```env
DB_STRING=mongodb://localhost:27017  # MongoDB URI
WEATHER_KEY=your_openweathermap_api_key
```

## How It Works

### 1. `app.py` - Extract, Transform, and Load (ETL) Weather Data

This script connects to the OpenWeatherMap API, extracts weather data, transforms it, and prepares it for storage in MongoDB. The key steps are:

- **Extract**: Fetch weather data from the OpenWeatherMap API.
- **Transform**: Convert temperature from Kelvin to Celsius and remove unnecessary columns.
- **Load**: Insert the transformed data into MongoDB.

### 2. `weather_producer.py` - Kafka Producer

The Kafka producer extracts weather data from `app.py`, transforms it, and sends it to the `weather_topic` Kafka topic. It sends data every 3 minutes (180 seconds). The key steps are:

- **Extract and Transform**: Fetch weather data and transform it.
- **Produce to Kafka**: Send the transformed data to Kafka using the `confluent_kafka.Producer`.

### 3. `weather_consumer.py` - Kafka Consumer

The Kafka consumer reads messages from the `weather_topic` Kafka topic and inserts the data into MongoDB. It consumes data continuously and processes it every 3 minutes. The key steps are:

- **Consume from Kafka**: Read data from the `weather_topic`.
- **Load to MongoDB**: Insert the consumed data into the MongoDB database for storage.


