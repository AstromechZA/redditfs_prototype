import requests
import json


class Datasource(object):

    def __init__(self):
        self.known_subreddits = list()

    def refresh_known_subreddits(self):
        r = requests.get('http://api.reddit.com/subreddits', headers={'User-Agent': 'my super happy random user agent'})
        data = json.loads(r.text)
        print data
        self.known_subreddits = [s['data']['display_name'] for s in data['data']['children']]
        return len(self.known_subreddits)