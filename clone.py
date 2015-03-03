import urllib2
import json
import logging

import orm

productversion="v2.2" #FIXME: hardcoded

def downloadCaseversionById(cid):
    # query = query.replace(" ", "\%20")
    # baseurl = "https://developer.mozilla.org/en-US/search?format=json&q="
    baseURL = "https://moztrap.mozilla.org/api/v1/caseversion/"
    url = baseURL + str(cid) + "/"
    url = url + "/?format=json"
    data = urllib2.urlopen(url).read()
    return json.loads(data)


def downloadSuiteById(sid):
    # query = query.replace(" ", "\%20")
    # baseurl = "https://developer.mozilla.org/en-US/search?format=json&q="
    url = ("https://moztrap.mozilla.org/api/v1/caseversion/"
           "?case__suites={sid}&productversion__version={productversion}"
           "&limit=0&format=json"
          ).format(sid=sid, productversion=productversion)
    data = urllib2.urlopen(url).read()
    return json.loads(data)


def clone(args):
    output = ""
    if args.resource_type == "caseversion":
        query = str(args.id)
        logging.info("Downloading CaseVersion " + query + " ...")
        result = downloadCaseversionById(query)
        output = orm.formatCaseversion(result)

    elif args.resource_type == "suite":
        query = str(args.id)
        logging.info("Downloading Suite " + query + " ...")
        result = downloadSuiteById(query)
        output = orm.formatSuite(result)

    filename = args.resource_type + "_" + str(args.id) + ".txt"
    # TODO: confirm before overwrite
    with open(filename, 'w') as file_:
            file_.write(output)
    logging.info(filename + " created")
