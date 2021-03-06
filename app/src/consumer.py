import json
import pandas as pd
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


def process_data_chunk(ts_list, uid_list):
    """Process the two lists using pandas groupby and nunique functions

    :param ts_list: list of timestamps
    :param uid_list: list of uids
    :return: series object with the number of unique users per timeUnit (minute, hour, day, ...)
    """
    df = pd.DataFrame({'ts': ts_list, 'uid': uid_list})
    series = df.groupby('ts').nunique()['uid']
    return series


def consume(topic: str):
    """Consume the stream from a topic
        process data_chunks per time_unit
        and print results as soon as they are calculated

    :param topic: name of the topic to consume
    :return:
    """
    # Initialize a consumer
    consumer = KafkaConsumer(topic,
                             group_id=None,
                             bootstrap_servers=['localhost:9092'],
                             auto_offset_reset='earliest',
                             consumer_timeout_ms=5000)

    # Columns : lists used to store data of single chunks sequentially
    ts_list = []
    uid_list = []

    # Loop on the stream
    for message in consumer:
        try:
            uid, dt_object = process_kafka_message(message)
        except Exception as e:
            print(e)

        # Feed columns
        ts_list.append(dt_object.strftime("%m-%d-%YT%H:%M"))
        uid_list.append(uid)

    result = process_data_chunk(ts_list, uid_list)
    print(result)
    consumer.close()


if __name__ == "__main__":
    # myTopic = sys.argv[1]
    myTopic = "mySmallTopic"
    print("Start consuming !!!!!!")
    consume(myTopic)
