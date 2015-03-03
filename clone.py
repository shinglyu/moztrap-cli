import urllib2
import json
import logging

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


def formatCaseversion(caseversion):
    txt = ("TEST THAT {name}\n"
           "{desc}\n"
           "\n"
          ).format(name=caseversion['name'],
                   desc=caseversion['description'])
    for step in caseversion['steps']:
        txt += ("WHEN {instr}\n"
                "THEN {expected}\n"
                "\n"
               ).format(instr=step['instruction'],
                        expected=step['expected'])
    return txt


def formatSuite(suite):
    # TODO: sort by product version
    sortedCaseVersions= sorted(suite['objects'], key=lambda k: k['productversion'])
    txt = ""
    for caseversion in sortedCaseVersions:
        txt += formatCaseversion(caseversion)
        txt += "\n=====\n\n"
    return txt


def clone(args):
    output = ""
    if args.resource_type == "caseversion":
        query = str(args.id)
        logging.info("Downloading CaseVersion " + query + " ...")
        result = downloadCaseversionById(query)
        output = formatCaseversion(result)

    elif args.resource_type == "suite":
        query = str(args.id)
        logging.info("Downloading Suite " + query + " ...")
        result = downloadSuiteById(query)
        output = formatSuite(result)

    filename = args.resource_type + "_" + str(args.id) + ".txt"
    # TODO: confirm before overwrite
    with open(filename, 'w') as file_:
            file_.write(output)
    logging.info(filename + " created")
