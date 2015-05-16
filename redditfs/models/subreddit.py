
class Subreddit(object):

    def __init__(self, url, description, subscribers):
        self.url = url
        self.description = description
        self.subscribers = subscribers
        self.links = list()

        # TODO loads more interesting fields
        # checkout: https://github.com/reddit/reddit/wiki/JSON

    @classmethod
    def from_json(cls, data):
        return Subreddit(data['url'], data['description'], data['subscribers'])