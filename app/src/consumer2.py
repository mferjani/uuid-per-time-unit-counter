import sys
import json
from kafka import KafkaConsumer
from datetime import datetime


def process_kafka_message(message: str):
    """Process a Kafka message, and return user id and datetime object

    :param message: message from kafka
    :return: uid and datetime
    """
    m = json.loads(message.value)
    uid = m['uid']
    ts = m['ts']
    dt_object = datetime.fromtimestamp(ts)
    return uid, dt_object


def consume(topic: str, host: str):
    """Consume the stream from a topic
        process data_chunks per time_unit
        and print results as soon as they are calculated

    :param topic: name of the topic to consume
    :return:
    """
    # Initialize a consumer
    consumer = KafkaConsumer(topic,
                             group_id=None,
                             bootstrap_servers=[f'{host}:9092'],
                             auto_offset_reset='earliest')

    # Columns : lists used to store data of single chunks sequentially
    uid_set = set()

    # Variable used for chunks : assuming data is ordered by timestamp
    current_time = None

    # Loop on the stream
    for message in consumer:
        try:
            uid, dt_object = process_kafka_message(message)
        except Exception as e:
            print(e)

        if current_time != dt_object.strftime("%m-%d-%YT%H:%M"):
            if current_time is None:
                pass
            else:
                # process this chunk of data
                print(f"{current_time}\n\t{len(uid_set)}")
                # Clear set for next chunk
                uid_set.clear()
            current_time = dt_object.strftime("%m-%d-%YT%H:%M")

        # Feed the set
        uid_set.add(uid)

    consumer.close()


if __name__ == "__main__":
    host = sys.argv[1]
    myTopic = sys.argv[2]
    print("Start consuming !!!!!!")
    consume(myTopic, host)
