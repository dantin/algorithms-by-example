# -*- coding: utf-8 -*-
"""
    uid
    ~~~~~~

    A library which provides global unique id as twitter's snowflake.

    The original Snowflake is implemented in scala.

    https://github.com/twitter/snowflake/blob/master/src/main/scala/com/twitter/service/snowflake/IdWorker.scala

    The customized sequence format:
        +------------------------------------------------+--------+--------+---------------+
        |                  timestamp                     |  data  | worker |    sequence   |
        |                 milliseconds                   | center |   ID   |     number    |
        +------------------------------------------------+--------+--------+---------------+
        | 0000000000 0000000000 0000000000 0000000000 00 | 00000  | 00000  | 0000000000 00 |
        +------------------------------------------------+--------+--------+---------------+

    :copyright: @ 2018 by HC APM team.
    :license: BSD, see LICENSE for more details.

"""

import re
import time
import logging


def _time_gen():
    return int(time.time() * 1000)


def _till_next_millis(last_timestamp):
    timestamp = _time_gen()
    while timestamp <= last_timestamp:
        timestamp = _time_gen()

    return timestamp


class IdWorker(): # pylint: disable=too-few-public-methods
    """`IdWorker` is the global unique id generator."""
    worker_id_bits = 5
    data_center_id_bits = 5
    sequence_bits = 12

    max_worker_id = -1 ^ (-1 << worker_id_bits)
    max_data_center_id = -1 ^ (-1 << data_center_id_bits)

    worker_id_shift = sequence_bits
    data_center_id_shift = worker_id_shift + worker_id_bits
    timestamp_left_shift = data_center_id_shift + data_center_id_bits

    sequence_mask = -1 ^ (-1 << sequence_bits)

    # Tue, 21 Mar 2006 20:50:14.000 GMT
    twepoch = 1142974214000

    def __init__(self, worker_id, data_center_id):
        # Sanity check for worker_id
        if worker_id > self.max_worker_id or worker_id < 0:
            raise AssertionError('worker_id',
                                 "worker id can't be greater than {} or less than 0"
                                 .format(self.max_worker_id))

        if data_center_id > self.max_data_center_id or data_center_id < 0:
            raise AssertionError('data_center_id',
                                 "data center id can't be greater than {} or less than 0"
                                 .format(self.max_data_center_id))

        self.worker_id = worker_id
        self.data_center_id = data_center_id

        self.logger = logging.getLogger("uid")

        # regex for user agent.
        self.user_agent_parser = re.compile(r'[a-zA-Z][a-zA-Z\-0-9]*')

        # global stats
        self.ids_generated = 0
        # stats at a time slice
        self.sequence = 0
        self.last_timestamp = -1

        self.logger.info("ID worker initialized. "
                         "timestamp left shift: %d, data center id bits: %d, "
                         "worker id bits: %d, sequence bits: %d, worker id: %d",
                         self.timestamp_left_shift, self.data_center_id_bits,
                         self.worker_id_bits, self.sequence_bits, self.worker_id)

    def _next_id(self):
        timestamp = _time_gen()

        if self.last_timestamp > timestamp:
            self.logger.warning('clock is moving backwards. Reject request until %i',
                                self.last_timestamp)
            raise AssertionError('Clock moved backwards. Refusing to generate '
                                 'id for %i milliseconds' % self.last_timestamp)

        if self.last_timestamp == timestamp:
            # lots of requests at the same time, just increase the sequence.
            self.sequence = (self.sequence + 1) & self.sequence_mask
            if self.sequence == 0:
                # too many requests, wait till next millisecond.
                timestamp = _till_next_millis(self.last_timestamp)
        else:
            self.sequence = 0

        self.last_timestamp = timestamp

        new_id = (((timestamp - self.twepoch) << self.timestamp_left_shift) |
                  (self.data_center_id << self.data_center_id_shift) |
                  (self.worker_id << self.worker_id_shift) |
                  self.sequence)

        self.ids_generated += 1
        return new_id

    def _valid_user_agent(self, user_agent):
        return self.user_agent_parser.search(user_agent) is not None

    def get_id(self, agent):
        """Generate global unique id."""
        if not self._valid_user_agent(agent):
            raise AssertionError('invalid user agent')

        new_id = self._next_id()
        self.logger.debug('id: %i, user_agent: %s, worker_id: %i, data_center_id: %i',
                          new_id, agent, self.worker_id, self.data_center_id)
        return new_id
