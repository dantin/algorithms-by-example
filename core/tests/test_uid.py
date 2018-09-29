# -*- coding: utf-8 -*-
"""
    test_guid
    ~~~~~~

    Test cases for `guid.py`.

    :copyright: @ 2018 by HC APM team.
    :license: BSD, see LICENSE for more details.
"""

import pytest

from snowflake.uid import IdWorker


# pylint: disable=no-self-use, too-few-public-methods
@pytest.fixture
def default_agent():
    """Default agent name."""
    return 'agent'


@pytest.fixture
def id_worker():
    """Default IdWorker."""
    data_center_id = 1
    worker_id = 1
    return IdWorker(data_center_id, worker_id)


class TestIdWorker():
    """Tests for `IdWorker`."""

    def test_get_id(self, id_worker, default_agent):
        """Test that `get_id` works properly."""
        id_1 = id_worker.get_id(default_agent)
        id_2 = id_worker.get_id(default_agent)
        fmt = '{:064b}'
        assert id_2 > id_1
        assert len(fmt.format(id_1)) == 64
        assert len(fmt.format(id_2)) == 64
