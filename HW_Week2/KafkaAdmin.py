from kafka.admin import KafkaAdminClient, NewTopic, ConfigResource, ConfigResourceType
import time


def CreateTopic(admin_client, topic_name="example-topic", num_partitions=1, replication_factor=1):
# Create a topic

    try:
        admin_client.create_topics(new_topics=[NewTopic(topic_name, num_partitions, replication_factor)])
    except:
        print(f"Topic {topic_name} already exists.")

def DeleteTopic(topic_name=["example-topic"]):
# Delete topics
    try:
        admin_client.delete_topics(topics=topic_name)
    except:
        print(f"Topic {topic_name} doesnt exist.")


admin_client = KafkaAdminClient(
    bootstrap_servers=['localhost:9092'],
    client_id='dataops_client'
)

# List existing topics
print(admin_client.list_topics())

CreateTopic(admin_client, topic_name="topic_function1", num_partitions=2, replication_factor=1)
CreateTopic(admin_client, topic_name="topic_function2", num_partitions=2, replication_factor=1)

#time.sleep(5)
print(admin_client.list_topics())

DeleteTopic(topic_name=["topic_function1","topic_function3"])

#time.sleep(5)
print(admin_client.list_topics())


