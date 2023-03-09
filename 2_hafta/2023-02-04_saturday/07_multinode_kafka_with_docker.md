## Stop Kafka local


```commandline
sudo systemctl stop kafka
sudo systemctl stop zookeeper
```


## Kafka multinode docker zookeeper-less

### Start cluster
```commandline
sudo systemctl start docker

cd zookeeperless_kafka/

for i in {1..3}; do mkdir -p data/kafka${i}; done

docker-compose up --build -d
```

- Check cluster
```commandline
docker-compose ps


- Output
NAME                COMMAND             SERVICE             STATUS              PORTS
kafka1              "start-kafka.sh"    kafka1              running             0.0.0.0:9092->9092/tcp, :::9092->9092/tcp
kafka2              "start-kafka.sh"    kafka2              running             0.0.0.0:9292->9092/tcp, :::9292->9092/tcp
kafka3              "start-kafka.sh"    kafka3              running             0.0.0.0:9392->9092/tcp, :::9392->9092/tcp
```

- If cluster doesn't start and you try to explore container log. Windows might corrupt start-kafka.sh file.
```commandline
standard_init_linux.go:228: exec user process caused: no such file or directory
```
- This might solve: https://stackoverflow.com/questions/51508150/standard-init-linux-go190-exec-user-process-caused-no-such-file-or-directory

- OR try this one
```commandline
sed -i 's/\r$//' start-kafka.sh
```
### Stop cluster
` docker-compose down `

