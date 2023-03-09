from kafka import KafkaConsumer


my_consumer = KafkaConsumer('regions', bootstrap_servers=['localhost:9092'],
                            client_id='my_consumer-1',
                            group_id='regions_group'
                            )

# for message in my_consumer:
#     print("Key: {}, Value: {}, Topic: {}, Partition: {}, Offset: {}".format(message.key.decode("utf-8"),
#     message.value.decode("utf-8"),
#     message.topic,
#     message.partition,
#     message.offset))

for message in my_consumer:
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    # print("topic: %s, partition: %d, offset: %d, key: %s value: %s" % (message.topic,
    #                                              message.partition,
    #                                              message.offset,
    #                                              message.key.decode('utf-8'),
    #                                              message.value.decode('utf-8')))

    # Key: 1, Value: Marmara, Partition: 0, TS: 1613224639352
    # Key: 4, Value: İc Anadolu, Partition: 1, TS: 1613224654849
    # Key: 3, Value: Akdeniz, Partition: 2, TS: 1613224661486
    # Key: 2, Value: Ege, Partition: 2, TS: 1613224667044

    print("Key: %s, Value: %s, Partition %d, TS: %s" % (message.key.decode('utf-8'),
                                                                 message.value.decode('utf-8'),
                                                                 message.partition,
                                                                 str(message.timestamp)))

