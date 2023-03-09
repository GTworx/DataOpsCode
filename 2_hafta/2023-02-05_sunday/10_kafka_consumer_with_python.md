- https://kafka-python.readthedocs.io/en/master/index.html

## 1. Intro
We can consume messages from kafka topic with many differet ways. One of them is Python client.

- In this tuts we will produce a few simple messages to our local kafka broker with  python producer and consume with python consumer.

## 2. PyCharm 
Open PyCharm project same with python consumer. 


## 3. Python consumer 
- Create `myconsumer.py` and use following codes. 
```
# Import libs
from kafka import KafkaConsumer

# Create consumer object
# Consume earliest messages,
# If there is no new message in 10 seconds, stop consuming.
consumer = KafkaConsumer('topic1',  # topic
                         group_id='group1',
                         # consume earliest available messages, for latest 'latest'
                         auto_offset_reset='earliest',
                         # don't commit offsets
                         enable_auto_commit=False,
                         # stop iteration if no message after 10 secs
                         consumer_timeout_ms=10000,
                         # kafka servers and port
                         bootstrap_servers=['localhost:9092'])

for message in consumer:
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    print("topic: %s, partition: %d, offset: %d, key: %s value: %s" % (message.topic,
                                                 message.partition,
                                                 message.offset,
                                                 message.key.decode('utf-8'),
                                                 message.value.decode('utf-8')))
```

## 4. Run consumer 
- Inside code right click then run. 

## 5. Run Producer
- Inside code right click then run.