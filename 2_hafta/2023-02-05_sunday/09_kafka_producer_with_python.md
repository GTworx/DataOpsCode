- https://kafka-python.readthedocs.io/en/master/index.html  

## 1. Intro
We can produce messages to a kafka topic with many different ways. One of them is Python client.

- In this tutorial we will produce a few simple messages to our local kafka broker and consume with console consumer.


## 2 Console Consumer 
Open terminal for console consumer. You can open 3 consumer. 
` kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic topic1 ` 


## 3. Python Producer
- Open PyCharm and select venvspark virtualenv as interpreter. Create `myproducer.py` and use following codes. 
```
from kafka import KafkaProducer
import time

producer =  KafkaProducer(bootstrap_servers=['localhost:9092'])


# for i in range(0,20):
#     time.sleep(0.5)
#     print(i)
#     message = f'Message-{i}'
#     key = str(i)
#     producer.send(topic='topic1', value=message.encode('utf-8'), key=key.encode('utf-8'))

with open('/home/train/datasets/tr_il_plaka_kod.csv', 'r') as f:
    line = f.read()
    #producer.send(topic='topic1', value=line.encode('utf-8'))
    #print(line)

for line in line.split('\n'):
    time.sleep(1.5)
    if 'plaka,il' not in line:
        producer.send(topic='topic1', value=line.encode('utf-8'))
        print(line)

producer.flush()
```

## 4. Run Producer 
- Inside Pycharm code pane right click then run. 

## 5. Observe results 
- From console consumer 


