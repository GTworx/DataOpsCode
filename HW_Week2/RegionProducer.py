from kafka import KafkaProducer
import time

my_producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                            client_id='RegionProducer')

# read from file
with open("/home/train/datasets/RegionsTR.txt") as f:
    lines = f.readlines()

for line in lines:
    time.sleep(1.5)
    print(line.strip("\n"))
    my_producer.send(topic='regions',
                     key=line.strip("\n").split(",")[0].encode('utf-8'),
                     value=line.strip("\n").split(",")[1].encode('utf-8'))

# hardcode

# lines = [(1, "Marmara"), (2, "Ege"), (3, "Karadeniz"), (4, "Akdeniz"), (5, "Dogu Anadolu"), (6, "Ic Anadolu")
# ,(7, "Guney Dogu Anadolu")]
#
#
# for line in lines:
#     time.sleep(1.5)
#     print(line)
#     my_producer.send(topic='regions',
#                     key=str(line[0]).encode('utf-8'),
#                     value=line[1].encode('utf-8'))

my_producer.flush()

#my_producer.close()