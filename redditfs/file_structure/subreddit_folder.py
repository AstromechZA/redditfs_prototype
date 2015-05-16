from redditfs.file_structure.folder import Folder
from redditfs.utils import create_filename


class SubredditFolder(Folder):

    def __init__(self, name, datasource):
        super(SubredditFolder, self).__init__(name)
        self.datasource = datasource
        self.subreddits = dict()

    def add_folder(self, f):
        raise TypeError('Cannot add folders to a dynamic folder')

    def add_file(self, f):
        raise TypeError('Cannot add files to a dynamic folder')

    def refresh(self):
        self.subreddits = dict()
        data = self.datasource.get_subreddits()
        for i in data['data']['children']:
            self.subreddits[i['data']['display_name']] = i['data']

    def list(self):
        self.refresh()
        return ['.', '..'] + self.subreddits.keys()

    def __iter__(self):
        return self.subreddits.keys().__iter__()

    def __getitem__(self, name):
        self.refresh()
        return SubredditListingFolder(self.subreddits[name], self.datasource)

    def __contains__(self, name):
        self.refresh()
        return name in self.subreddits


class SubredditListingFolder(Folder):

    def __init__(self, data, datasource):
        super(SubredditListingFolder, self).__init__(data['display_name'])
        self.datasource = datasource
        self.data = data
        self.listing = dict()

    def add_folder(self, f):
        raise TypeError('Cannot add folders to a dynamic folder')

    def add_file(self, f):
        raise TypeError('Cannot add files to a dynamic folder')

    def refresh(self):
        self.listing = dict()
        data = self.datasource.get_listing_for_subreddit(self.data['display_name'])
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

        super(RedditPostFolder, self).add_folder(Folder('link'))
        super(RedditPostFolder, self).add_folder(Folder('content'))
        super(RedditPostFolder, self).add_folder(Folder('image'))

    def add_folder(self, f):
        raise TypeError('Cannot add folders to a dynamic folder')

    def add_file(self, f):
        raise TypeError('Cannot add files to a dynamic folder')
