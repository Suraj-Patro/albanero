from kafka import KafkaConsumer


consumer = KafkaConsumer('test_topic')


for message in consumer:
    print (message)
