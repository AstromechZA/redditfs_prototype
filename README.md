# redditfs

An experimental reddit browser running as a virtual file system.

## About

I worked on this project as a way to learn about virtual file systems, how they operate, and how to write a simple
one using FUSE and Python.

This prototype has the ability to browse and list subreddits, posts inside subreddits, and to view basic attributes of
each post.

It caches requests to Reddit's JSON Api but it still operates fairly slowly when on a slow connection espescially when
fetching the initial list of subreddits. Reddit's json api gives way more information than this program needs.

At the lowest level, each post has its `title`, `link`, `author`, `created`, and `self_text` (if it's a self post).

### Is this a viable way to browse reddit?
For a human being? No.

### Dependencies?
- `fuse` on ubuntu or `osxfuse` on OSX
- Other dependencies are Python modules that will be installed upon `setup.py install`.

### Is the code any good?
- Some parts are good, overall it's pretty hacked together. (Hey it's a proof of concept!)
- LRU Expiring Cache works well.

### What more could be done?

- It only lists the top 25 posts of each subreddit, and by default lists only the top 25 subreddits since those are default
    result sizes that the JSON api returns. Work could be done to expose 'pages' of posts or subreddits as another level
    in the hierarchy.

- It would be interesting to look into allowing a user to post in subreddits by writeing to a file in the filesystem.

- It's a very expandable idea as a prototype, it's not very usable in the real world but it's a fun idea to play with.

- Could be an interesting base for a reddit scraping bot.

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

# un-mount
$ umount ~/redditfs
```