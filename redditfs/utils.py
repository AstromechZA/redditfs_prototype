from datetime import datetime


def make_user_agent():
    return 'redditfs:{}:A virtual filesystem for browsing reddit'.format(datetime.now().isoformat())