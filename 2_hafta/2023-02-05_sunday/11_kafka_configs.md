1. We can configure Kafka in different ways.
If we want to change something cluster wide, we need to modify `server.properties` file.
We can change configuration per topic but not everything.

- Broker Configs
- Topic Configs
- Producer Configs
- Consumer Configs
- Kafka Connect Configs
- Kafka Streams Configs
- AdminClient Configs

2. There is `kafka-configs.sh` to configure commandline  
Actions:  --describe, --alter

- add-config 
- alter: Alter the configuration for the entity.  
- delete-config: config keys to remove 'k1,k2'
- describe:   List configs for the given entity.

2.1. Decrease topic retention
```
kafka-configs.sh --bootstrap-server localhost:9092 \
--alter \
--entity-type topics \
--entity-name topic1 \
--add-config retention.ms=1000
```
2.2. Change cleanup.policy
```
kafka-configs.sh --bootstrap-server localhost:9092 \
--alter  \
--entity-type topics --entity-name topic1 \
--add-config cleanup.policy='delete'
```
2.3. Change message retention size to 200 MB
```
kafka-configs.sh --bootstrap-server localhost:9092 \
--alter  \
--entity-type topics --entity-name topic1 \
--add-config retention.bytes=209715200

```
2.4. Change retention time to 1.67 minutes
```
kafka-configs.sh --bootstrap-server localhost:9092 \
--alter  \
--entity-type topics --entity-name topic1 \
--add-config retention.ms=100000
```

See the dynamic configs for a given topic
```
kafka-configs.sh \
--bootstrap-server localhost:9092 \
--describe \
--entity-type topics \
--entity-name topic1



Dynamic configs for topic topic1 are:
  cleanup.policy=delete sensitive=false synonyms={DYNAMIC_TOPIC_CONFIG:cleanup.policy=delete, DEFAULT_CONFIG:log.cleanup.policy=delete}
  retention.ms=100000 sensitive=false synonyms={DYNAMIC_TOPIC_CONFIG:retention.ms=100000}
  retention.bytes=209715200 sensitive=false synonyms={DYNAMIC_TOPIC_CONFIG:retention.bytes=209715200, DEFAULT_CONFIG:log.retention.bytes=-1}

```

3. Message count in a topic
```
kafka-run-class.sh kafka.tools.GetOffsetShell \
--broker-list localhost:9092  \
--topic topic1 \
--time -1 \
--offsets 1 | awk -F  ":" '{sum += $3} END {print sum}'
```

4. Truncate a topic? 
- Delete topic and create with same name.
```
kafka-topics.sh \
--bootstrap-server localhost:9092 \
--topic topic1 --delete

kafka-topics.sh \
--bootstrap-server localhost:9092 \
--topic topic1 --create \
--partitions 3 --replication-factor 1


kafka-run-class.sh kafka.tools.GetOffsetShell \
--broker-list localhost:9092  \
--topic topic1 --time -1 --offsets 1 \
| awk -F  ":" '{sum += $3} END {print sum}'
```
