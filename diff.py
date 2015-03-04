import json
import os
import logging

import clone

difftool="vimdiff"

def diff(args):
    filename=args.filename

    with open(filename, 'r') as file_:
        firstline = file_.readline()
    meta = json.loads(firstline)

    latestdir="./latest/"
    clone.cloneByURL(meta[u'resource_uri'], latestdir)

    os.system(difftool + " " + filename + " " + latestdir + filename)
    # call os.system('vimdiff')
