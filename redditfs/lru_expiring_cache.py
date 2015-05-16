__author__ = 'benmeier@fastmail.com'
__date__ = '17 May 2015'

from datetime import datetime


class LRUExpiringCache(object):
    """
    Example of a key-value cache that uses a least-recently used cache expiry mechanism as well as timed expiry on
    values. (items are invalid after not being updated for too long)

    The cache has a fixed size and expires the items that have not been used first.
    """

    def __init__(self, existing_data=None, size=20, expire_timeout_seconds=300):
        self.max_size = size
        self.expire_timeout_seconds = expire_timeout_seconds
        self.head = None
        self.tail = None
        self.register = {}

        if existing_data is not None:
            if isinstance(existing_data, dict):
                for k, v in existing_data.items():
                    self._put(k, v)
            elif isinstance(existing_data, list) or isinstance(existing_data, tuple):
                for item in existing_data:
                    self._put(item[0], item[1])
            else:
                raise TypeError('Existing data must be a dict/list/tuple')

    def _put(self, k, v):
        if k in self.register:
            self._delete(self.register[k])
            return self._put(k, v)
        else:
            n = LRUNode(k, v)
            n.next = self.head
            if self.head is not None:
                self.head.prev = n
            else:
                self.tail = n
            self.head = n
            self.register[k] = n
            if len(self) > self.max_size:
                self._delete(self.tail)
            return n

    def _update(self, n):
        self._delete(n)
        return self._put(n.key, n.value)

    def _delete_by_key(self, k):
        self._delete(self.register[k])

    def _delete(self, n):
        if self.head == n and self.tail == n:
            self.head = None
            self.tail = None
        elif self.head == n:
            self.head = n.next
            self.head.prev = None
        elif self.tail == n:
            self.tail = n.prev
            self.tail.next = None
        else:
            n.prev.next = n.next
            n.next.prev = n.prev

        del self.register[n.key]

    def __contains__(self, key):
        return key in self.register and not self.register[key].has_expired(self.expire_timeout_seconds)

    def __getitem__(self, key):
        n = self.register[key]
        if n.has_expired(self.expire_timeout_seconds):
            raise KeyError('Cache does contain key {} but it has expired!'.format(key))
        return self._update(n).value

    def __setitem__(self, key, value):
        self._put(key, value)

    def __len__(self):
        return len(self.register)

    def __delitem__(self, key):
        self._delete_by_key(key)

    def __iter__(self):
        n = self.head
        while n:
            yield n
            n = n.next

    def clear(self):
        self.head = None
        self.tail = None
        self.register.clear()


class LRUNode(object):

    def __init__(self, k, v):
        self.key = k
        self.value = v
        self.created_at = datetime.utcnow()
        self.next = None
        self.prev = None

    def has_expired(self, timeout_seconds):
        now = datetime.utcnow()
        return (now - self.created_at).total_seconds() > timeout_seconds