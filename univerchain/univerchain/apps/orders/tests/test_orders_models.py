import pytest
from django.utils import timezone


def test_order_created_time(order):
    time = timezone.now()
    cur_time = str(time)[:10]
    order_time = str(order)[:10]

    assert order_time == cur_time


def test_order_item_id(order_item):
    assert str(order_item) == "1"
