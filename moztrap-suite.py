#!/usr/bin/python
import urllib2
import json
import sys
import os
import platform

import moztrap

productversion="v2.2" #FIXME: hardcoded

def downloadSuiteById(sid):
    # query = query.replace(" ", "\%20")
    # baseurl = "https://developer.mozilla.org/en-US/search?format=json&q="
    url = ("https://moztrap.mozilla.org/api/v1/caseversion/"
           "?case__suites={sid}&productversion__version={productversion}"
           "&limit=0&format=json"
          ).format(sid=sid, productversion=productversion)
    data = urllib2.urlopen(url).read()
    return json.loads(data)


def format(suite):
    # TODO: sort by product version
    sortedCaseVersions= sorted(suite['objects'], key=lambda k: k['productversion'])
    txt = ""
    for caseversion in sortedCaseVersions:
        txt += moztrap.format(caseversion)
        txt += "\n=====\n\n"
    return txt

def main():
    # query = " ".join(sys.argv[1:])
    query = sys.argv[1]
    print "Downloading Suite " + query + " ..."
    result = downloadSuiteById(query)
    print format(result)
    #title, url = getFirstResult(result)
    #if url is None:
        #print title
    #else:
        #print "Found: " + title
        #print url
        #openUrl(url)

if __name__ == '__main__':
    main()
