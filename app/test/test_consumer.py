import pandas as pd
from app.src import consumer
from kafka.consumer.fetcher import ConsumerRecord
from datetime import datetime
from pandas._testing import assert_series_equal


class TestConsumer:

    def test_process_kafka_message(self):
        cr = ConsumerRecord(topic="test_topic",
                            partition=0, offset=0, timestamp=1583312930269, timestamp_type=0,
                            headers=[],
                            checksum=None,
                            serialized_key_size=-1,
                            serialized_value_size=2114,
                            serialized_header_size=-1,
                            key=None,
                            value=b'{"k1": "v1","k2": "v2","uid": "uid_value","ts": 1468244385}'
                            )

        uid, dt = consumer.process_kafka_message(cr)
        assert uid == "uid_value"
        assert dt == datetime.fromtimestamp(1468244385)

    def test_process_data_chunk(self):
        ts_list = ['t1', 't1', 't1', 't1', 't2', 't2', 't2', 't3', 't3', 't3', 't3']
        uid_list = ['u1', 'u1', 'u1', 'u2', 'u2', 'u1', 'u2', 'u1', 'u2', 'u1', 'u3']

        result = consumer.process_data_chunk(ts_list, uid_list)

        # Expected result
        # a simple dictionary
        dict = {'t1': 2,
                't2': 2,
                't3': 3}

        # create series from dictionary
        expected = pd.Series(dict, name='uid', index=pd.Index(['t1', 't2', 't3'], dtype='object', name='ts'))

        assert_series_equal(result, expected, check_dtype=True, check_names=True)

    def test_consume(self):
        pass
