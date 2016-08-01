#!/usr/bin/env python
# Purge URLs from the IDR Nginx cache
# Assumes cached items are in /var/cache/nginx/*/?/??/

import hashlib
import os
import re
import sys


def get_cache_dirs(parent):
    ls = [os.path.join(parent, f) for f in os.listdir(parent)]
    subdirs = [d for d in ls if os.path.isdir(d)]
    return subdirs


def get_hash(u):
    # Strip the scheme and host if present
    ukey = re.match('((\w+://)?[^/]*)?(/.*)', u).group(3)
    return hashlib.md5(ukey).hexdigest()


parent = '/var/cache/nginx'
cache_dirs = get_cache_dirs(parent)


def remove(u):
    f = get_hash(u)
    d1 = f[-1]
    d2 = f[-3:-1]
    found = False
    for d in cache_dirs:
        p = os.path.join(d, d1, d2, f)
        if os.path.exists(p):
            print 'Removing cache entry for %s (%s)' % (u, p)
            os.unlink(p)
            found = True
    if not found:
        sys.stderr.write('Unable to find cache entry for %s\n' % u)


if __name__ == '__main__':
    for u in sys.argv[1:]:
        try:
            remove(u)
        except Exception as e:
            sys.stderr.write(
                'Error whilst removing cache entry for %s: %s\n' % (u, e))
