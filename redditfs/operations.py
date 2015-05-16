import errno
import logging
from redditfs.datasource import Datasource
from redditfs.file_structure.folder import Folder
from redditfs.file_structure.reddit_folders import SubredditFolder

from fuse import Operations, FuseOSError

log = logging.getLogger(__name__)


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
                raise FuseOSError(errno.ENOENT)
        return n

    def getattr(self, path, fh=None):
        return self._get_subnode(path).get_attrs()

    def getxattr(self, path, name, position=0):
        return ''

    def listxattr(self, path):
        return []

    def mkdir(self, path, mode):
        raise FuseOSError(errno.EACCES)

    def open(self, path, flags):
        self.file_descriptors += 1
        return self.file_descriptors

    def read(self, path, size, offset, fh):
        return self._get_subnode(path).content[offset:(offset + size)]

    def readdir(self, path, fh):
        return self._get_subnode(path).list()

    def readlink(self, path):
        return self._get_subnode(path).content

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
