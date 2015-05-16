import logging
from redditfs.file_structure.folder import Folder
from redditfs.utils import create_filename, ACTIVE_UID, ACTIVE_GID
from time import time
from stat import S_IFREG

log = logging.getLogger(__name__)


class SubredditFolder(Folder):

    def __init__(self, name, datasource):
        super(SubredditFolder, self).__init__(name)
        self.datasource = datasource
        self.subreddits = set()

    def add_folder(self, f):
        raise TypeError('Cannot add folders to a dynamic folder')

    def add_file(self, f):
        raise TypeError('Cannot add files to a dynamic folder')

    def refresh(self):
        log.debug('refresh')
        data = self.datasource.get_subreddits()
        for i in data['data']['children']:
            self.subreddits.add(i['data']['display_name'])

    def fetch_subreddit(self, name):
        self.subreddits.add(name.strip())

    def list(self):
        self.refresh()
        return ['.', '..'] + list(self.subreddits)

    def __iter__(self):
        return self.subreddits.__iter__()

    def __getitem__(self, name):
        log.debug('GET %r', name)
        self.refresh()
        return SubredditListingFolder(name, self.datasource)

    def __contains__(self, name):
        log.debug('CONTAINS %r', name)
        if name in self.subreddits:
            return True
        if self.datasource.is_a_subreddit(name):
            self.subreddits.add(name)
            return True
        else:
            return False


class SubredditListingFolder(Folder):

    def __init__(self, name, datasource):
        super(SubredditListingFolder, self).__init__(name)
        self.datasource = datasource
        self.listing = dict()

    def add_folder(self, f):
        raise TypeError('Cannot add folders to a dynamic folder')

    def add_file(self, f):
        raise TypeError('Cannot add files to a dynamic folder')

    def refresh(self):
        self.listing = dict()
        data = self.datasource.get_listing_for_subreddit(self.name)
        for i in data['data']['children']:
            f = RedditPostFolder(i['data'], self.datasource)
            self.listing[f.name] = f

    def list(self):
        self.refresh()
        return ['.', '..'] + self.listing.keys()

    def __iter__(self):
        return self.listing.keys().__iter__()

    def __getitem__(self, name):
        self.refresh()
        return self.listing[name]

    def __contains__(self, name):
        self.refresh()
        return name in self.listing


class RedditPostFolder(Folder):

    def __init__(self, data, datasource):
        filename = create_filename(data['title'])
        if len(filename) > 108:
            filename = filename[:105] + '...'

        super(RedditPostFolder, self).__init__(filename)
        self.datasource = datasource
        self.data = data

        super(RedditPostFolder, self).add_file(ContentFile('link',  self.data['url'].encode('utf-8')))
        super(RedditPostFolder, self).add_file(ContentFile('created',  str(self.data['created'])))
        super(RedditPostFolder, self).add_file(ContentFile('title', self.data['title'].encode('utf-8')))
        super(RedditPostFolder, self).add_file(ContentFile('author', self.data['author'].encode('utf-8')))
        super(RedditPostFolder, self).add_file(ContentFile('self_text', self.data.get('self_text', '').encode('utf-8')))

    def add_folder(self, f):
        raise TypeError('Cannot add folders to a dynamic folder')

    def add_file(self, f):
        raise TypeError('Cannot add files to a dynamic folder')


class ContentFile(object):

    def __init__(self, name, content):
        self.name = name
        self.content = content

    def get_attrs(self):
        return dict(
            st_mode=(S_IFREG | 0400),
            st_nlink=1,
            st_size=len(self.content),
            st_ctime=time(),
            st_mtime=time(),
            st_atime=time(),
            st_uid=ACTIVE_UID,
            st_gid=ACTIVE_GID
        )