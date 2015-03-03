#!/usr/bin/python
import urllib2
import json
import sys
import os
import platform
import argparse
import logging

import clone

logging.basicConfig(level=logging.INFO)

def downloadCaseversionById(cid):
    # query = query.replace(" ", "\%20")
    # baseurl = "https://developer.mozilla.org/en-US/search?format=json&q="
    baseURL = "https://moztrap.mozilla.org/api/v1/caseversion/"
    url = baseURL + str(cid) + "/"
    url = url + "/?format=json"
    data = urllib2.urlopen(url).read()
    return json.loads(data)


def formatCaseversion(caseversion):
    txt = ("TEST THAT {name}\n"
           "{desc}\n"
           "\n"
          ).format(name=caseversion['name'],
                   desc=caseversion['description'])
    #txt += "TEST THAT "
    #txt += caseversion['name']
    #txt += "\n"
    #txt += caseversion['description']
    #txt += "\n"
    for step in caseversion['steps']:
        txt += ("WHEN {instr}\n"
                "THEN {expected}\n"
                "\n"
               ).format(instr=step['instruction'],
                        expected=step['expected'])
    return txt


def main():
    # query = " ".join(sys.argv[1:])
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="action", help="use \"[command] -h\" to see help message for individual command")

    parser_clone = subparsers.add_parser('clone')
    parser_clone.add_argument('resource_type', type=str, choices=['caseversion', 'suite'], help="Resource type")
    parser_clone.add_argument('id', type=int, help="Resource ID")

    parser_diff = subparsers.add_parser('diff')
    parser_diff.add_argument('filename', type=str, help="File to be diffed")

    parser_push = subparsers.add_parser('push')
    parser_push.add_argument('-f', '--force', action="store_true", help="Force overwrite (BE CAREFUL!)")
    parser_push.add_argument('filename', type=str, help="File to be pushed")

    args = parser.parse_args()

    # print args
    if args.action == "clone":
        clone.clone(args)
    elif args.action == "diff":
        raise NotImplementedError
    elif args.action == "push":
        raise NotImplementedError

#def clone(args):
    #output = ""
    #if args.resource_type == "caseversion":
        #query = str(args.id)
        #logging.info("Downloading CaseVersion " + query + " ...")
        #result = downloadCaseversionById(query)
        #output = formatCaseversion(result)
        ##title, url = getFirstResult(result)
        ##if url is None:
            ##print title
        ##else:
            ##print "Found: " + title
            ##print url
            ##openUrl(url)
    #elif args.resource_type == "suite":
        #raise NotImplementedError
#
    #filename = args.resource_type + "_" + str(args.id) + ".json"
    #with open(filename, 'w') as file_:
            #file_.write(output)
    #logging.info(filename + " created")


if __name__ == '__main__':
    main()
