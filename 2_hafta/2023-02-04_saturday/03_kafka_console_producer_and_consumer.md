```
kafka-topics.sh --bootstrap-server localhost:9092 \
--create --topic topic1 \
--replication-factor 1 \
--partitions 3
```

## 1. Producer 
Send messages to topic1 with kafka-console.producer.sh

In terminal-1 :
```
kafka-console-producer.sh \
--bootstrap-server localhost:9092 \
--topic topic1


>hello this is first message
>this is second one
>this will be 3'rd msg
>
```

## 2. Consumer
Consume messages from topic1
In terminal-2:
```
kafka-console-consumer.sh \
--bootstrap-server localhost:9092 \
--topic topic1 --from-beginning


hello this is first message
this is second one
this will be 3'rd msg
```

## 3. Close both terminal with Ctrl+C

## 4. Topic creation with defaults
If you produce messages to non-existing topic, topic will be created upon first message arriving but with default properties which is not recommended.

## 5. Producing messages with key 
Terminal-1
```
kafka-console-producer.sh \
--bootstrap-server localhost:9092 \
--topic topic1 \
--property parse.key=true \
--property key.separator=$


> key-1$message-1
> key-2$message-2
> key-3$message-3
>
```

## 6. Consuming messages with key 
Terminal-2
```
kafka-console-consumer.sh \
--bootstrap-server localhost:9092 \
--topic topic1 \
--property print.key=true \
--property key.separator=$


null,this is second one
null,hellothis is first message
null,this will be 3'rd msg
key1$message-1
key-2$message-2
key-3$message-3
```

## 7. Close both terminal Ctrl+C

