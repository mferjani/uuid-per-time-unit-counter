## Documentation

https://github.com/mferjani/uuid-per-time-unit-counter.git


## Hypotesis & assumptions :

- Data is ordered by timestamp
- Only one partition


- You can assume that 99.9% of the frames arrive with a maximum latency of 5 seconds.
==>
before processing a chunk we store the new data in a tmp_new_ds during 5 secs
we check previous time (YYYY, YYYYMM, YYYYMMDD, YYYYMMDDHH) doesn't exist otherwise we move it to the current_chunk_ds
we process the current_chunk_ds
we clear current_chunk_ds and move tmp_new_ds to it
we resume

- the results should be forwarded to a new kafka topic (again as json.) choose a suitable structure.




## Useful Commands  :

- Starting zookeeper :
zookeeper-server-start.sh $KAFKA_HOME/config/zookeeper.properties

- Starting Kafka :
kafka-server-start.sh $KAFKA_HOME/config/server.properties

- Stoping kafka
ps ax | grep -i 'kafka.Kafka' | grep -v grep | awk '{print $1}' | xargs kill -9

- List topics :
kafka-topics.sh --list --bootstrap-server localhost:9092

- Create a topic
kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic mytopic

- Data generator help
app/bin/data-generator-osx -h

- Create a stream sample
app/bin/data-generator-osx -c 1000000 -r 1000 -n 10000 -o data/mytopic.json

- Send the stream to the topic
kafka-console-producer.sh \
  --broker-list localhost:9092 \
  --topic topic3 < data/mytopic.json

- Consume the stream from the topic
kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic mytopic --from-beginning


## Useful links

https://success.docker.com/article/getting-started-with-kafka




