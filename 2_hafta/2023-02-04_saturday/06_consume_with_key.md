## 1. Sending keys to kafka 
If you sent key to topic you can guarantee same key goes to same partition.
** this may be job interview question **

## 2. Start consumers 
Start 3 consumer with following command  

``` 
kafka-console-consumer.sh \
--bootstrap-server localhost:9092 \
--topic topic1 \
--property print.key=true \
--group group1
```

## 3. Generate data 

With data generator produce `tr_il_plaka_kod.csv` to topic1 twice (data_generator is able to send keys to kafka).
```
python dataframe_to_kafka.py \
--input ~/datasets/tr_il_plaka_kod.csv \
--topic topic1 \
-k 0 -r 2
```
-k: column index of the data 
-r: repeat whole data set twice.

## 4. Results
Observe that same keys goes to same partitions (because three partitions consumed by three consumers) For example you will see 115'th key twice from same consumer.

