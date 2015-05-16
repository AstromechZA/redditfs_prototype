import json
import requests
from random import randrange
from datetime import datetime


class APIException(Exception):
    pass


class CachedRequester(object):

    def __init__(self, invalidation_timeout=300, slots=20):
        self.invalidation_timeout = 300
        self.slots = 20
        self.user_agent = self._make_random_user_agent()
        self.register = {}
        self.head_node = None
        self.tail_node = None
        self.current_count = 0

    def _make_random_user_agent(self):
        return 'redditfs:{}:{}:{}'.format(
            datetime.utcnow().isoformat(),
            self.invalidation_timeout,
            str(hex(randrange(1024*1024, 1024*1024*16)))[2:]
        )

    def get(self, url):
        url = url.strip()
        urlkey = hash(url)

        if self.contains(urlkey):
            return self.get_from_cache(urlkey)

        response = requests.get(url, headers={'User-Agent': self.user_agent})
        if response.ok:
            data = json.loads(response.text)
            self.push(urlkey, data)
        else:
            raise APIException('Code {} for url {}'.format(response.status_code, response.url))

    def push(self, key, value):
        if key in self.register:
            node = self.register[key]
            node.last_retrieved = datetime.utcnow()



        else:
            node = CacheNode(key, value)
            if self.head_node is not None:
                self.head_node.link(node)
            self.head_node = node

            if not self.tail_node:
                self.tail_node = node

            self.current_count += 1

            if self.current_count > self.slots:
                t = self.tail_node.prev_node
                self.tail_node.unlink()
                self.tail_node = t
                del self.register[self.tail_node.key]

            self.register[key] = value

    def contains(self, key):
        return (key in self.register and
                (datetime.utcnow() - self.register[key].last_retrieved).total_seconds() < self.invalidation_timeout)

    def get_from_cache(self, key):
        pass

# how LRU works:
# linked list of slots
# HEAD slot is most recently used
# TAIL slot is least recently used


class CacheNode(object):

    def __init__(self, key, value, last_retrieved=None, prev_node=None):
        self.key = key
        self.value = value
        self.last_retrieved = last_retrieved or datetime.utcnow()
        self.prev_node = prev_node

    def link(self, prev_node=None):
        self.prev_node = prev_node
        return self

    def unlink(self):
        self.prev_node = None
        return self

