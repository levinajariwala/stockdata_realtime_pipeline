from kafka import KafkaProducer
from time import sleep
from json import dumps
import pandas as pd


try:
    stock_producer = KafkaProducer(bootstrap_servers=['<Your Public IP>:<port_no>'],
                             value_serializer=lambda x: dumps(x).encode('utf-8'))
    df = pd.read_csv('latestStockData.csv.csv')
except Exception as e:
    print("An error occurred while initializing the producer / reading the CSV file:", str(e))
    stock_producer = None
    df = None

if stock_producer and df is not None:
    while True:
        try:
            sample_data = df.sample(1).to_dict(orient='records')[0]
            stock_producer.send('stock_data_stream', value=sample_data)
            sleep(0.1)
        except Exception as e:
            print("An error occurred while sending data to Kafka:", e)

if stock_producer:
    try:
        stock_producer.flush()
    except Exception as e:
        print("An error occurred while flushing the producer:", e)
