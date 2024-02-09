from cassandra.cluster import Cluster
from kafka import KafkaConsumer
from json import loads, dumps


try:
    consumer = KafkaConsumer('stock_data_stream',
                             bootstrap_servers=['<Your Public IP>:9092'],
                             value_deserializer=lambda x: loads(x.decode('utf-8')))
except Exception as e:
    print("An error occurred while initializing the Kafka consumer:", str(e))
    consumer = None


try:
    cluster = Cluster(['<Your Public IP>'])
    session = cluster.connect()
    session.execute(
        "CREATE KEYSPACE IF NOT EXISTS stockmarket WITH replication = {'class':'SimpleStrategy', 'replication_factor':1};")
    session.set_keyspace("stockmarket")
    session.execute('''CREATE TABLE IF NOT EXISTS stock_data (
						                        id int PRIMARY KEY, 
                                                "index" varchar,
                                                sd_date varchar,
                                                open float,
                                                high float,
                                                low float,
                                                close float,
                                                "adj close" float,
                                                volume bigint,
                                                closeUSD float
                                                );''')
except Exception as e:
    print("An error occurred while initializing the session / creating the keyspace / table:", str(e))
    session = None


if consumer and session is not None:
    massage_id = 0
    for message in consumer:
        if (message.value):
            try:
                massage_id += 1
                new_data = {'Id': massage_id}
                new_data.update(message.value)
                final_data = dumps(new_data)
                session.execute(
                    f"INSERT INTO stock_data JSON'{final_data}';")
            except Exception as e:
                print("An error occurred while inserting data into table:", str(e))
