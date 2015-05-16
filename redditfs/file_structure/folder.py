from redditfs.utils import ACTIVE_UID, ACTIVE_GID
from stat import S_IFDIR
from time import time


class Folder(object):

    def __init__(self, name):
        self.name = name
        self.files = dict()
        self.folders = dict()
        self.parent = None

    def add_file(self, f):
        self.files[f.name] = f

    def add_folder(self, f):
        self.folders[f.name] = f
        f.parent = self

    def __contains__(self, name):
        return name in self.files or name in self.folders

    def __getitem__(self, name):
        if name in self.files:
            return self.files[name]
        elif name in self.folders:
            return self.folders[name]
        raise KeyError('folder does not contain item %r' % name)

    def __iter__(self):
        for f in self.folders.values():
            yield f
        for f in self.files.values():
            yield f

    def get_attrs(self):
        return dict(
            st_mode=(S_IFDIR | 0400),
            st_nlink=2 + len(self.folders),
            st_size=0,
            st_ctime=time(),
            st_mtime=time(),
            st_atime=time(),
            st_uid=ACTIVE_UID,
            st_gid=ACTIVE_GID
        )

    def list(self):
        return ['.', '..'] + [f.name for f in list(self)]