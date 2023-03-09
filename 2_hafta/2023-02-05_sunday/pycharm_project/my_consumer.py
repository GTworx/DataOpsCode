from kafka import KafkaConsumer


my_consumer = KafkaConsumer('topic1', bootstrap_servers=['localhost:9092', 'localhost:9292'],
                            client_id='my_consumer-1',
                            group_id='group1'
                            )

for message in my_consumer:
    print("Key: {}, Value: {}, Topic: {}, Partition: {}, Offset: {}".format(message.key.decode("utf-8"),
            message.value.decode("utf-8"),
            message.topic,
          message.partition,
          message.offset))