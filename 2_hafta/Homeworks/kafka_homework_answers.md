# QUESTIONS
## 1.  
Create a topic named `atscale`, 2 partitions and replication factor 1.

## 2. 
List all topics.

## 3. 
Describe `atscale` topic.

## 4. 
Use data-generator and send `https://raw.githubusercontent.com/erkansirin78/datasets/master/Churn_Modelling.csv` to  3 patitioned `churn` topic.

- Message key should be CustomerId.

- Consume under `churn_group` and this group must have 3 consumer. 
    - Use different terminal for each consumer. 
    - Use `kafka-console-consumer.sh` as a consumer.

- Observe 500 messages.

## 5. 
Delete `atscale` and `churn` topics.

## 6.
-  Using Python Kafka do the following tasks:
    - Produce the names of Turkey's geographical regions to a topic you specify, using the numbers you specify at the beginning of each of them as keys. For example, 1 Marmara, 2 Aegean.
    - With the Consumer, print the key, value, partition, timestamp information as following example.
```
Key: 1, Value: Marmara, Partition: 0, TS: 1613224639352 
Key: 4, Value: İç Anadolu, Partition: 1, TS: 1613224654849 
Key: 3, Value: Akdeniz, Partition: 2, TS: 1613224661486 
Key: 2, Value: Ege, Partition: 2, TS: 1613224667044
```

## 7.
- Truncate topic1.
- Produce iris.csv using data-generator to topic1.
- Build a python consumer;
	- Comsume from topic1. 
	- Write the message content, topic name, partition number of each flower type in a separate file with its own name (`/tmp/kafka_out/<species_name_out.txt`>).
	- Write messages that do not belong to any of the three flower types in the `/tmp/kafka_out/other_out.txt` file.

Example result file tree: 
```
tree /tmp/kafka_out/
/tmp/kafka_out/
├── other_out.txt
├── setosa_out.txt
├── versicolor_out.txt
└── virginica_out.txt
```

Example file content
```
 head /tmp/kafka_out/setosa_out.txt
topic1|2|0|0|5.1,3.5,1.4,0.2,Iris-setosa
topic1|2|1|2|4.7,3.2,1.3,0.2,Iris-setosa
topic1|2|2|3|4.6,3.1,1.5,0.2,Iris-setosa
topic1|2|3|9|4.9,3.1,1.5,0.1,Iris-setosa
topic1|2|4|16|5.4,3.9,1.3,0.4,Iris-setosa
topic1|2|5|29|4.7,3.2,1.6,0.2,Iris-setosa
topic1|2|6|32|5.2,4.1,1.5,0.1,Iris-setosa
topic1|2|7|36|5.5,3.5,1.3,0.2,Iris-setosa
topic1|2|8|40|5.0,3.5,1.3,0.3,Iris-setosa
topic1|2|9|41|4.5,2.3,1.3,0.3,Iris-setosa
```

## 8.
Write a python function that fulfills the following requirements.
- Arguments: KafkaAdminClient object, topic name, number of partitions and replication factor
- Do not take any action if there is a topic with the same name
- If there is no topic with the same name, it will create a topic using arguments

def create_a_new_topic_if_not_exists(admin_client, topic_name="example-topic", num_partitions=1, replication_factor=1):
	<YOUR CODE HERE>

------------------------------------------------------------------------------------------









# ANSWERS
## 1. 
```
kafka-topics.sh --bootstrap-server localhost:9092 --create --topic atscale --partitions 2 --replication-factor 1
```

## 2. 
```
kafka-topics.sh --bootstrap-server localhost:9092 --list
__consumer_offsets
atscale
test1
test2
topic1
```

## 3. 
```
kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic atscale
Topic: atscale	PartitionCount: 2	ReplicationFactor: 1	Configs: segment.bytes=1073741824
	Topic: atscale	Partition: 0	Leader: 0	Replicas: 0	Isr: 0
	Topic: atscale	Partition: 1	Leader: 0	Replicas: 0	Isr: 0
```

## 4. 
### Topic create
```
kafka-topics.sh --bootstrap-server localhost:9092 \
--create --topic churn \
--partitions 3 \
--replication-factor1
```

### data-generator download
```
git clone https://github.com/erkansirin78/data-generator.git
cd data-generator
```

### Virtualenv  
` source ~/venvspark/bin/activate ` 

### Download dataset 
`  wget -P ~/datasets https://raw.githubusercontent.com/erkansirin78/datasets/master/Churn_Modelling.csv ` 

### Consumers
Open 3 terminal  
` kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic churn --group churn_group `  

### Produce dataset  
` (venvspark) [train@localhost data-generator]$ python dataframe_to_kafka.py -i ~/datasets/Churn_Modelling.csv -t churn -k 1 ` 

## 5.
`  kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic  atscale,churn  ` 

- Check
```
(venvspark) [train@localhost data-generator]$ kafka-topics.sh --bootstrap-server localhost:9092 --list
__consumer_offsets
test1
test2
topic1
```

## 6.
### Open 2 termina, activate virtualenv, open python shell.

### Create topic.

### Consumer terminal.
```
>>> from kafka import KafkaConsumer
>>> consumer = KafkaConsumer('test1',group_id='group1',bootstrap_servers=['localhost:9092'])

>>> for message in consumer:
...     print("Key: {}, Value: {}, Partition: {}, TS: {} ".format(message.key.decode(), message.value.decode(), message.partition, message.timestamp))
... 
```

### Producer terminal
```
>>> from kafka import KafkaProducer
>>> producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

>>> producer.send("test1", key="1".encode(), value="Marmara".encode())

>>> producer.send("test1", key="2".encode(), value="Ege".encode())

>>> producer.send("test1", key="3".encode(), value="Akdeniz".encode())

>>> producer.send("test1", key="4".encode(), value="İç Anadolu".encode())
```

## Observe results
```
Key: 1, Value: Marmara, Partition: 0, TS: 1613224639352 
Key: 4, Value: İç Anadolu, Partition: 1, TS: 1613224654849 
Key: 3, Value: Akdeniz, Partition: 2, TS: 1613224661486 
Key: 2, Value: Ege, Partition: 2, TS: 1613224667044
```



## 7.
### create kafka_out folder: ` mkdir /tmp/kafka_out ` 

### myconsumer_todisk.py 
```
from utility.message_parser import MessageParser
from kafka import KafkaConsumer
import re
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

setosa_file_obj = open("/tmp/kafka_out/setosa_out.txt", "a")
versicolorfile_obj = open("/tmp/kafka_out/versicolor_out.txt", "a")
virginicafile_obj = open("/tmp/kafka_out/virginica_out.txt", "a")
other_obj = open("/tmp/kafka_out/other_out.txt", "a")
mp = MessageParser()

for message in consumer:
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    print("topic: %s, partition: %d, offset: %d, key: %s value: %s" % (message.topic,
                                                 message.partition,
                                                 message.offset,
                                                 message.key.decode('utf-8'),
                                                 message.value.decode('utf-8')))

    species = mp.message_splitter(message.value.decode('utf-8'))
    print("Species: {} ".format(species))

    if species == "setosa":
        setosa_file_obj.write(
            message.topic + "|" + str(message.partition) + "|" + str(message.offset) + "|" + message.key.decode(
                'utf-8') + "|" + message.value.decode('utf-8') + "\n")
    elif species == "versicolor":
        versicolorfile_obj.write(
            message.topic + "|" + str(message.partition) + "|" + str(message.offset) + "|" + message.key.decode(
                'utf-8') + "|" + message.value.decode('utf-8') + "\n")

    elif species == "virginica":
        versicolorfile_obj.write(
            message.topic + "|" + str(message.partition) + "|" + str(message.offset) + "|" + message.key.decode(
                'utf-8') + "|" + message.value.decode('utf-8') + "\n")
    else:
        other_obj.write(
            message.topic + "|" + str(message.partition) + "|" + str(message.offset) + "|" + message.key.decode(
                'utf-8') + "|" + message.value.decode('utf-8') + "\n")


setosa_file_obj.close()
versicolorfile_obj.close()
virginicafile_obj.close()
other_obj.close()
```

### message_parser.py
from utility.message_parser import MessageParser 
```
import re
class MessageParser:

    def message_splitter(self, message):
        species = re.split(",", message)[-1]
        switcher = {
            'Iris-setosa': "setosa",
            'Iris-versicolor': "versicolor",
            'Iris-virginica': "virginica",
            None: "other"
        }
        return switcher.get(species)
```

### start consumer 

### start data-generator 
` (venvspark) [train@localhost data-generator]$ python dataframe_to_kafka.py -t topic1 ` 




## 8.
```
from kafka.admin import KafkaAdminClient, NewTopic

admin_client = KafkaAdminClient(
    bootstrap_servers="localhost:9092",
    client_id='test'
)

print(admin_client.list_topics())
#  ['test1', 'test', 'test2', '__consumer_offsets']

def create_a_new_topic_if_not_exists(admin_client, topic_name="example-topic", num_partitions=1, replication_factor=1):
    """
    Creates a topic if not exists
    :param topic_name:
    :param num_partitions:
    :param replication_factor:
    :return:
    """
    if topic_name not in admin_client.list_topics():
        new_topic1 = NewTopic(name=topic_name, num_partitions=num_partitions, replication_factor=replication_factor)
        try:
            admin_client.create_topics(new_topics=[new_topic1], validate_only=False)
        except:
            print('kafka.errors.TopicAlreadyExistsError')


create_a_new_topic_if_not_exists(admin_client, topic_name="from-python-client1", num_partitions=1, replication_factor=1)

print(admin_client.list_topics())
# ['test', 'test1', 'from-python-client1', '__consumer_offsets', 'test2']

admin_client.close()

```

