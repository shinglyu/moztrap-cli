import urllib2
import json
import os
import logging

import orm

productversion="v2.2" #FIXME: hardcoded

mtorigin = "https://moztrap.mozilla.org"

def downloadCaseversionById(cid):
    # query = query.replace(" ", "\%20")
    # baseurl = "https://developer.mozilla.org/en-US/search?format=json&q="
    baseURL = mtorigin + "/api/v1/caseversion/"
    url = baseURL + str(cid) + "/"
    url = url + "/?format=json"
    data = urllib2.urlopen(url).read()
    return json.loads(data)


def downloadSuiteById(sid):
    # query = query.replace(" ", "\%20")
    # baseurl = "https://developer.mozilla.org/en-US/search?format=json&q="
    url = (mtorigin + "/api/v1/caseversion/"
           "?case__suites={sid}&productversion__version={productversion}"
           "&limit=0&format=json"
          ).format(sid=sid, productversion=productversion)
    data = urllib2.urlopen(url).read()
    return json.loads(data)


def clone(resource_type, sid, dirname="./"):
    output = ""
    if resource_type == "caseversion":
        query = str(sid)
        logging.info("Downloading CaseVersion " + query + " ...")
        result = downloadCaseversionById(query)
        output = orm.formatCaseversion(result)

    elif resource_type == "suite":
        query = str(sid)
        logging.info("Downloading Suite " + query + " ...")
        result = downloadSuiteById(query)
        output = orm.formatSuite(result, sid)

    filename = dirname + resource_type + "_" + str(sid) + ".txt"
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    with open(filename, 'w') as file_:
            file_.write(output)
    logging.info(filename + " created")


def cloneByURL(url, dirname="./"):
    (resource_type, rid) = orm.parseURL(url)

    clone(resource_type, rid, dirname)


