from kafka import KafkaProducer


producer = KafkaProducer(bootstrap_servers='localhost:9092')

result = producer.send("test_topic", b"Hello, World !!!")

print( result )

producer.flush()
