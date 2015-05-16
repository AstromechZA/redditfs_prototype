from redditfs import utils
from redditfs.lru_expiring_cache import LRUExpiringCache
import requests
import json
import os

REDDIT_ENDPOINT = 'http://api.reddit.com/'


class Datasource(object):

    def __init__(self):
        self.cache = LRUExpiringCache(size=50, expire_timeout_seconds=60)
        self.user_agent = utils.make_user_agent()

    def get_json(self, url):
        if url in self.cache:
            return self.cache[url]
        else:
            r = requests.get(url, headers={'User-Agent': self.user_agent})
            if r.ok:
                data = json.loads(r.text)
                self.cache[url] = data
                return data
            else:
                raise RuntimeError('Request to {} failed with {}'.format(r.url, r.status_code))

    def get_reddit_api_json(self, *path_elements):
        return self.get_json(REDDIT_ENDPOINT + os.path.join(*path_elements))

    def get_subreddits(self):
        return self.get_reddit_api_json('subreddits', 'popular')

    def get_listing_for_subreddit(self, subreddit):
        return self.get_reddit_api_json('r', subreddit)
