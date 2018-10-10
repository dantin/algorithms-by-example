# -*- coding: utf-8 -*-
"""
    super_fast_hash
    ~~~~~~

    Stream-adapted SuperFastHash algorithm.

    :copyright: @ 2018 by Dantin.
    :license: BSD, see LICENSE for more details.

"""


# pylint: disable=invalid-name
class uint32_t(int):
    """Class that occupy 4 bytes as integer"""

    _MAX_UINT32 = (1 << 32) - 1

    def __rshift__(self, other):
        return uint32_t(int.__rshift__(self, other) & self._MAX_UINT32)

    def __lshift__(self, other):
        return uint32_t(int.__lshift__(self, other) & self._MAX_UINT32)

    def __add__(self, other):
        return uint32_t(int.__add__(self, other) & self._MAX_UINT32)

    def __xor__(self, other):
        return uint32_t(int.__xor__(self, other) & self._MAX_UINT32)


def __get_16_bits(ptr):
    """Get integer value of 2 bytes."""
    return ord(ptr[0]) + (ord(ptr[1]) << 8)


def super_fast_hash(data, seed):
    """`super_fast_hash` implement SuperFastHash algorithm.

    See: http://www.azillionmonkeys.com/qed/hash.html
    """

    if not data: # data is None or empty sequence.
        return 0

    len_ = len(data)
    # get first two bytes of data.
    rem = len_ & 3
    len_ >>= 2

    # use seed to initialize the final result.
    hash_ = uint32_t(seed)

    # Main loop
    while len_ > 0:
        len_ -= 1
        hash_ += __get_16_bits(data)
        tmp = (__get_16_bits(data[2:]) << 11) ^ hash_
        hash_ = (hash_ << 16) ^ tmp
        data = data[4:]
        hash_ += (hash_ >> 11)

    # Handle end cases
    if rem == 3:
        hash_ += __get_16_bits(data)
        hash_ ^= (hash_ << 16)
        hash_ ^= (ord(data[2]) << 18)
        hash_ += (hash_ >> 11)
    elif rem == 2:
        hash_ += __get_16_bits(data)
        hash_ ^= (hash_ << 11)
        hash_ += (hash_ >> 17)
    elif rem == 1:
        hash_ += ord(data[0])
        hash_ ^= (hash_ << 10)
        hash_ += (hash_ >> 1)

    # Force "avalanching" of final 127 bits.
    hash_ ^= (hash_ << 3)
    hash_ += (hash_ >> 5)
    hash_ ^= (hash_ << 4)
    hash_ += (hash_ >> 17)
    hash_ ^= (hash_ << 25)
    hash_ += (hash_ >> 6)

    return hash_
