READ = 0x4
WRITE = 0x2
EXECUTE = 0x1
NONE = 0x0

def permission(user=0, group=0, other=0):
    return ((user * 16) + group) * 16 + other

P = permission