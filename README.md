# redditfs

An experimental reddit browser running as a virtual file system.

## About

I worked on this project as a way to learn about virtual file systems, how they operate, and how to write a simple
one using FUSE and Python.

This prototype has the ability to browse and list subreddits, posts inside subreddits, and to view basic attributes of
each post.

It caches requests to Reddit's JSON Api but it still operates fairly slowly when on a slow connection.

At the lowest level, each post has its `title`, `link`, `author`, and `self_text` (if it's a self post).

### Is this a viable way to browse reddit?
For a human being? No.

## Example Commands
```bash
$ mkdir ~/redditfs
$ mount-redditfs ~/redditfs

# list top subreddits
$ ls ~/redditfs/r

# list posts in subreddit
$ ls ~/redditfs/r/<some_subreddit>

# list available data of a post
$ ls ~/redditfs/r/<some_subreddit>/<some_post>/

# get printable title of a post
$ cat ~/redditfs/r/<some_subreddit>/<some_post>/title

# or the outgoing link?
$ cat ~/redditfs/r/<some_subreddit>/<some_post>/link
```