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
==> Use the producer

## Useful Commands  :

# Starting zookeeper :
zookeeper-server-start.sh $KAFKA_HOME/config/zookeeper.properties

# Starting Kafka :
kafka-server-start.sh $KAFKA_HOME/config/server.properties

# Stoping kafka
ps ax | grep -i 'kafka.Kafka' | grep -v grep | awk '{print $1}' | xargs kill -9

# List topics :
kafka-topics.sh --list --bootstrap-server localhost:9092

# Create a topic
kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic mytopic

kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic mySmalltopic

# List topics :
kafka-topics.sh --list --bootstrap-server localhost:9092

# Generate some data
app/bin/data-generator-osx -c 100000 -r 100 -n 10000 -o data/mystream.json

app/bin/data-generator-osx -c 10000 -r 100 -n 1000 -o data/mySmallstream.json

# Populate the topic with data

kafka-console-producer.sh \
  --broker-list localhost:9092 \
  --topic mytopic < /data/mystream.json


kafka-console-producer.sh \
  --broker-list localhost:9092 \
  --topic mySmalltopic < /data/mySmallstream.json

# Consume the topic
kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic mySmalltopic --from-beginning



# Consume the topic with python code
from kafka import KafkaConsumer
consumer = KafkaConsumer('mySmalltopic',group_id=None,bootstrap_servers=['alpic_kafka_1:9092'],auto_offset_reset='earliest')
consumer.topics()
msg = consumer.poll(1.0)



# Usin jq tool with data generator

app/bin/data-generator-osx -c 10 | jq -c "{ts, uid}"

{"ts":1468244385,"uid":"50efd97274f5fa8a054"}
{"ts":1468244386,"uid":"e6a538fb4dd0d9ff204"}
{"ts":1468244387,"uid":"b6dc4acc904e7a2ceef"}
{"ts":1468244388,"uid":"1fcea664573fecab73b"}
{"ts":1468244389,"uid":"9cc918baa3730ab11ea"}
{"ts":1468244390,"uid":"a3e6eff8ecca0bb86ac"}
{"ts":1468244391,"uid":"d83149259c5b9fc7276"}
{"ts":1468244392,"uid":"797cad9413df8ceb917"}
{"ts":1468244393,"uid":"4784412fdc62f9c2981"}
{"ts":1468244394,"uid":"d6193ab5ec2b928b3ea"}



## Useful links

https://success.docker.com/article/getting-started-with-kafka




