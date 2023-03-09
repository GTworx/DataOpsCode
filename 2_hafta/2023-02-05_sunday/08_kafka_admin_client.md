## For basic usage:
- https://kafka-python.readthedocs.io/en/master/index.html  

## For advanced usage but it is confluent backed
- https://docs.confluent.io/kafka-clients/python/current/overview.html

## 1. Intro
KafkaAdminClient class allows us to manage and manipulate topics and configs.

- In this tuts we will learn how to create, delete and list kafka topics.


## 2. Python KafkaAdminClient
- Open PyCharm and select venvspark virtualenv as interpreter. Create `admin_client.py` and use following codes. 
```
from kafka.admin import KafkaAdminClient, NewTopic, ConfigResource, ConfigResourceType
import time

admin_client = KafkaAdminClient(
    bootstrap_servers=['localhost:9092'],
    client_id='dataops_client'
)

# List configs
print(admin_client.list_topics())

# Describe topic configs
configs = admin_client.describe_configs(
    config_resources=[ConfigResource(ConfigResourceType.TOPIC, 'test1')])
print(configs)

# Describe a topic
print(admin_client.describe_topics(topics=['test1']))


# Create a topic
try:
    admin_client.create_topics(new_topics=[NewTopic('admin-client-topic', 3, 1)])
except:
    print("Topic exist")

time.sleep(5)
print(admin_client.list_topics())

# Delete topic
admin_client.delete_topics(topics=['admin-client-topic'])

time.sleep(5)
print(admin_client.list_topics())
```

## 3. Run  
- Inside Pycharm code pane right click then run. 

## 4. Observe results  


