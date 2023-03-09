from kafka import KafkaConsumer

dir = "/tmp/kafka_out/"
ext = "_out.txt"
iristypes = ["setosa","versicolor","virginica"]
iris_files = {}

iris_consumer = KafkaConsumer('topic1', bootstrap_servers=['localhost:9092'],
                            client_id='iris_consumer-1',
                            group_id='iris_group'
                              )
# open the files
for sp in iristypes:
    print(sp, dir+sp+ext)
    iris_files.update({sp: open((dir+sp+ext), "a")})

#iris_files = {sp: open((dir+sp+ext), "a") for sp in iristypes}
other_file = open((dir+"other"+ext), 'a')

for message in iris_consumer:
    print("Key: %s, Value: %s, Partition %d, TS: %s" % (message.key.decode('utf-8'), message.value.decode('utf-8'),
                                                                 message.partition,
                                                                 str(message.timestamp)))
    suffix, iristype = message.key.decode('utf-8').split("-")

    if iristype in iristypes:
        iris_files[iristype].write(f"{message.topic}|{message.partition}|{message.offset}|{message.timestamp}|{message.value.decode('utf-8')}\n")
    else:
        other_file.write(f"{message.topic}|{message.partition}|{message.offset}|{message.timestamp}|{message.value.decode('utf-8')}\n")

# Close all output files
for iris_file in iris_files.values():
    iris_file.close()
other_file.close()

