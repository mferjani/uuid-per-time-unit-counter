import json
import pandas as pd
from kafka import KafkaConsumer
from datetime import datetime
from pandas import Series


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


def print_result_to_stdout(msg: str, s: Series):
    print(f"\n{msg}\n\t{s}")


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
                             auto_offset_reset='earliest')

    # Columns : lists used to store data of single chunks sequentially
    ts_list = []
    uid_list = []

    # Counter for logging purpose
    counter = 0

    # Max number of frames to consume
    max_data = 400000

    # Variable used for chunks : assuming data is ordered by timestamp
    current_time = None

    # Loop on the stream
    for message in consumer:
        try:
            uid, dt_object = process_kafka_message(message)
        except Exception as e:
            print(e)

        if current_time != dt_object.strftime("%m-%d-%YT%H:%M"):
            current_time = dt_object.strftime("%m-%d-%YT%H:%M")
            if current_time is None:
                pass
            else:
                # process this chunk of data
                result = process_data_chunk(ts_list, uid_list)
                print_result_to_stdout(f"counter = {counter}", result)
                # Clear columns for next chunk
                ts_list.clear()
                uid_list.clear()

        # Feed columns
        counter = counter + 1
        ts_list.append(dt_object.strftime("%m-%d-%YT%H:%M"))
        uid_list.append(uid)

        # Stop loop condition
        if counter == max_data:
            break
    # If we still have data then we process it
    if len(ts_list) > 0:
        result = process_data_chunk(ts_list, uid_list)
        print_result_to_stdout(f"counter = {counter}, final chunk ! ", result)

    consumer.close()


if __name__ == "__main__":
    # myTopic = sys.argv[1]
    myTopic = "mytopic"
    print("Start consuming !!!!!!")
    consume(myTopic)
