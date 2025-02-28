#!/usr/bin/env python3

import fnmatch
import os
import sys

fuzzysearch = True
try:
    from fuzzywuzzy import process
except ImportError:
    fuzzysearch = False


QUERY = sys.argv[1]
HOME = os.environ['HOME']
PASS_DIR = os.environ.get('PASSWORD_STORE_DIR', os.path.join(HOME, '.password-store/'))


# TODO: list_passwords creates cache of passwords for first time
def list_passwords():
    ret = []

    for root, dirnames, filenames in os.walk(PASS_DIR, True, None, True):
        for filename in fnmatch.filter(filenames, '*.gpg'):
            ret.append(os.path.join(root, filename.replace('.gpg', '')).replace(PASS_DIR, ''))
    return sorted(ret, key=lambda s: s.lower())


def search_passwords(query):
    ''' Search passwords using the Fuzzy search method if fuzzywuzzy is available,
    or default to the filter-based search otherwise'''
    if fuzzysearch:
        return search_passwords_fuzzy(query)
    return search_passwords_filter(query)


def search_passwords_fuzzy(query):
    ''' Search passwords using the Fuzzy search method using fuzzywuzzy'''
    passwords = list_passwords()
    return [entry[0] for entry in process.extract(query, passwords)]


def search_passwords_filter(query):
    ''' Search passwords using the filter-based search, which doesn't require fuzzywuzzy'''
    ret = []

    terms = [x for x in query.lower().split() if x]
    passwords = list_passwords()

    for password in passwords:
        for t in terms:
            if t not in password.lower():
                break
        else:
            ret.append(password)

    return ret


def xmlize_items(items, query):
    items_a = []

    for item in items:
        list = item.rsplit("/", 1)
        name = list[-1]
        path = item if len(list) == 2 else ""

        complete = item
        if item.lower().startswith(query.lower()):
            i = item.find("/", len(query))
            if i != -1:
                complete = item[:(i+1)]

        items_a.append("""
    <item uid="%(item)s" arg="%(item)s" autocomplete="%(complete)s">
        <title>%(name)s</title>
        <subtitle>%(path)s</subtitle>
    </item>
        """ % {'item': item, 'name': name, 'path': path, 'complete': complete})

    return """
<?xml version="1.0"?>
<items>
    %s
</items>
    """ % '\n'.join(items_a)


items = search_passwords(QUERY)
print(xmlize_items(items, QUERY))
