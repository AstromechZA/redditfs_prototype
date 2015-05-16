import errno
import os
from collections import defaultdict
from errno import ENOENT
from redditfs.datasource import Datasource
from redditfs.file_structure.folder import Folder
from redditfs.file_structure.subreddit_folder import SubredditFolder
from stat import S_IFDIR, S_IFLNK, S_IFREG
from time import time

from fuse import Operations, FuseOSError

from redditfs.permission_maker import P, READ, WRITE, EXECUTE

PERMISSION_SET_SAFE = P(user=(READ | WRITE | EXECUTE), group=(READ | EXECUTE), other=(READ | EXECUTE))

# read only folders and files by default
DEFAULT_PERMISSION = P(user=READ, group=READ, other=READ)
ACTIVE_UID = os.getuid()
ACTIVE_GID = os.getgid()


class RedditOperations(Operations):

    def __init__(self):
        self.file_descriptors = 0
        self.datasource = Datasource()
        self.root = Folder('')
        self.root.add_folder(SubredditFolder('r', self.datasource))
        self.root.add_folder(Folder('users'))

    def chmod(self, path, mode):
        raise FuseOSError(errno.EACCES)

    def chown(self, path, uid, gid):
        raise FuseOSError(errno.EACCES)

    def create(self, path, mode, **kwargs):
        raise FuseOSError(errno.EACCES)

    def _get_subnode(self, path):
        if path == '/':
            parts = []
        else:
            parts = path.split('/')[1:]

        n = self.root
        for part in parts:
            if part in n:
                n = n[part]
            else:
                raise FuseOSError(ENOENT)
        return n

    def getattr(self, path, fh=None):
        return self._get_subnode(path).get_attrs()

    def getxattr(self, path, name, position=0):
        return ''       # Should return ENOATTR

    def listxattr(self, path):
        return []

    def mkdir(self, path, mode):
        raise FuseOSError(errno.EACCES)

    def open(self, path, flags):
        self.file_descriptors += 1
        return self.file_descriptors

    def read(self, path, size, offset, fh):
        return ''  # self.data[path][offset:offset + size]

    def readdir(self, path, fh):
        return self._get_subnode(path).list()

    def readlink(self, path):
        return ''  # self.data[path]

    def removexattr(self, path, name):
        raise FuseOSError(errno.EACCES)

    def rename(self, old, new):
        raise FuseOSError(errno.EACCES)

    def rmdir(self, path):
        raise FuseOSError(errno.EACCES)

    def setxattr(self, path, name, value, options, position=0):
        raise FuseOSError(errno.EACCES)

    def statfs(self, path):
        return dict(f_bsize=512, f_blocks=4096, f_bavail=2048)

    def symlink(self, target, source):
        raise FuseOSError(errno.EACCES)

    def truncate(self, path, length, fh=None):
        raise FuseOSError(errno.EACCES)

    def unlink(self, path):
        raise FuseOSError(errno.EACCES)

    def utimens(self, path, times=None):
        raise FuseOSError(errno.EACCES)

    def write(self, path, data, offset, fh):
        raise FuseOSError(errno.EACCES)
