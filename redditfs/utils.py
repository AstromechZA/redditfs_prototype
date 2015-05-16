import os
import re
from datetime import datetime

ACTIVE_UID = os.getuid()
ACTIVE_GID = os.getgid()


def make_user_agent():
    return 'redditfs:{}:A virtual filesystem for browsing reddit'.format(datetime.now().isoformat())


def create_filename(s):
    s = s.strip().lower().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)