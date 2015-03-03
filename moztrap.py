#!/usr/bin/python
import urllib2
import json
import sys
import os
import platform


def downloadCaseversionById(cid):
    # query = query.replace(" ", "\%20")
    # baseurl = "https://developer.mozilla.org/en-US/search?format=json&q="
    baseURL = "https://moztrap.mozilla.org/api/v1/caseversion/"
    url = baseURL + str(cid) + "/"
    url = url + "/?format=json"
    data = urllib2.urlopen(url).read()
    return json.loads(data)


def getFirstResult(searchResult):
    if len(searchResult['documents']) == 0:
        return ("Not Found", None)
    firstEntry = searchResult['documents'][0]
    return (firstEntry['title'], firstEntry['url'])

def format(caseversion):
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

def openUrl(url):
    if url is None:
        return

    if platform.system() == 'Darwin':
        os.system("open " + url)
    else:
        os.system("firefox " + url)


def main():
    # query = " ".join(sys.argv[1:])
    query = sys.argv[1]
    print "Downloading CaseVersion " + query + " ..."
    result = downloadCaseversionById(query)
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
