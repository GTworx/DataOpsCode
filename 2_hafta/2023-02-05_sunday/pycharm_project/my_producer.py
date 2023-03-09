from kafka import KafkaProducer
import time

my_producer = KafkaProducer(bootstrap_servers=['localhost:9092', 'localhost:9292', 'localhost:9392'],
                            client_id='my_producer')

# for i in range(10):
#     my_producer.send(topic='topic1',
#                      key=f'{i}'.encode('utf-8'),
#                      value=f'Hello Kafka-{i}'.encode('utf-8'))

with open("/home/train/datasets/tr_il_plaka_kod.csv") as f:
    lines = f.readlines()

for line in lines[1:]:
    time.sleep(1.5)
    print(line.strip("\n"))
    my_producer.send(topic='topic1',
                     key=line.strip("\n").split(",")[0].encode('utf-8'),
                     value=line.strip("\n").split(",")[1].encode('utf-8'))

my_producer.flush()

#my_producer.close()
