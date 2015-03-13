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
    # TODO: maybe we can use orm.parseURL here and remove the cloneByURL method
    clone.cloneByURL(meta[u'resource_uri'], latestdir)

    os.system(difftool + " " + filename + " " + latestdir + filename)
    # call os.system('vimdiff')

