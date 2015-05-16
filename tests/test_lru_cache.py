import pytest
from redditfs.lru_expiring_cache import LRUExpiringCache
from mock import patch
from datetime import timedelta


def test_basic():
    cache = LRUExpiringCache()

    cache['a'] = 1
    cache['b'] = 2
    cache['c'] = 3
    cache['d'] = 4
    cache['e'] = 5

    # is size correct?
    assert len(cache) == 5

    # is insertion order correct?
    assert [n.key for n in list(cache)] == ['e', 'd', 'c', 'b', 'a']


def test_construct__from_dict():
    cache = LRUExpiringCache({'a': 1, 'b': 2, 'c': 3})
    assert cache['a'] == 1
    assert cache['b'] == 2
    assert cache['c'] == 3


def test_construct__from_list():
    cache = LRUExpiringCache([['a', 1], ['b', 2], ['c', 3]])
    assert [n.key for n in list(cache)] == ['c', 'b', 'a']
    assert cache['a'] == 1
    assert cache['b'] == 2
    assert cache['c'] == 3


def test_construct__from_unknown():
    with pytest.raises(TypeError):
        _ = LRUExpiringCache(object())


def test_get():
    cache = LRUExpiringCache([['a', 1], ['b', 2], ['c', 3]])
    assert [n.key for n in list(cache)] == ['c', 'b', 'a']
    assert cache['b'] == 2
    assert [n.key for n in list(cache)] == ['b', 'c', 'a']


def test_put_overflow():
    cache = LRUExpiringCache([['a', 1], ['b', 2], ['c', 3]], size=3)
    assert [n.key for n in list(cache)] == ['c', 'b', 'a']
    cache['d'] = 4
    assert 'a' not in cache
    with pytest.raises(KeyError):
        _ = cache['a']
    assert [n.key for n in list(cache)] == ['d', 'c', 'b']


def test_delete_item():
    cache = LRUExpiringCache([['a', 1], ['b', 2], ['c', 3]])
    del cache['b']
    assert len(cache) == 2
    assert [n.key for n in list(cache)] == ['c', 'a']


def test_delete_item__missing():
    cache = LRUExpiringCache([['a', 1], ['b', 2], ['c', 3]])
    with pytest.raises(KeyError):
        del cache['unknown']


def test_delete_item_head():
    cache = LRUExpiringCache([['a', 1], ['b', 2], ['c', 3]])
    del cache['c']
    assert [n.key for n in list(cache)] == ['b', 'a']


def test_delete_only_item():
    cache = LRUExpiringCache([['a', 1]])
    assert len(cache) == 1
    del cache['a']
    assert len(cache) == 0
    assert [n.key for n in list(cache)] == []


def test_update():
    cache = LRUExpiringCache([['a', 1], ['b', 2], ['c', 3]])
    # if I update an item's value, does it move it to the front?
    cache['b'] = 20
    assert len(cache) == 3
    assert [n.key for n in list(cache)] == ['b', 'c', 'a']
    assert [n.value for n in list(cache)] == [20, 3, 1]


def test_clear():
    cache = LRUExpiringCache([['a', 1], ['b', 2], ['c', 3]])
    cache.clear()
    assert len(cache) == 0
    assert 'a' not in cache
    assert 'c' not in cache


def test_expiring_items():
    cache = LRUExpiringCache(expire_timeout_seconds=10)
    cache['a'] = 1
    assert cache['a'] == 1
    n = cache.head
    with patch('redditfs.lru_expiring_cache.datetime') as fake_datetime:
        fake_datetime.utcnow.return_value = (n.created_at + timedelta(seconds=9))
        assert 'a' in cache
        assert cache['a'] == 1
        n = cache.head

        fake_datetime.utcnow.return_value = (n.created_at + timedelta(seconds=11))
        assert 'a' not in cache
        with pytest.raises(KeyError):
            _ = cache['a']