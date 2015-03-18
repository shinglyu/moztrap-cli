import json
import os
import logging

import config
import mtapi

difftool=config.difftool

def diff(args):
    filename=args.filename

    with open(filename, 'r') as file_:
        firstline = file_.readline()
    meta = json.loads(firstline)

    latestdir="./latest/"
    # TODO: maybe we can use orm.parseURL here and remove the cloneByURL method
    latestFilename = mtapi.cloneByURL(meta[u'resource_uri'], latestdir)

    os.system(difftool + " " + filename + " " + latestFilename)
    # call os.system('vimdiff')

