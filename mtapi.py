import urllib2
import json
import os
import httplib
import logging
import requests

import config
import orm

productversion=config.productversion
mtorigin = config.mtorigin

# Download
def downloadCaseversionById(cid):
    # query = query.replace(" ", "\%20")
    # baseurl = "https://developer.mozilla.org/en-US/search?format=json&q="
    baseURL = mtorigin + "/api/v1/caseversion/"
    url = baseURL + str(cid) + "/"
    url = url + "?format=json"
    data = urllib2.urlopen(url).read()
    return json.loads(data)

def downloadCaseversionByCaseId(cid):
    # query = query.replace(" ", "\%20")
    # baseurl = "https://developer.mozilla.org/en-US/search?format=json&q="
    url = "{orig}/api/v1/caseversion/?format=json&case={cid}"\
          "&productversion__version={pversion}".format(orig=mtorigin,
                                                       cid=cid,
                                                       pversion=productversion)
    data = urllib2.urlopen(url).read()
    parsed = json.loads(data)
    return parsed['objects'][0]


def downloadSuiteById(sid):
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

    elif resource_type == "case":
        query = str(sid)
        logging.info("Downloading Case" + query + " ...")
        logging.warning("Only the CaseVersion for {v} was downloaded".format(v=productversion))
        result = downloadCaseversionByCaseId(query)
        output = orm.formatCaseversion(result)

    filename = dirname + resource_type + "_" + str(sid) + ".txt"
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    with open(filename, 'w') as file_:
            file_.write(output)
    logging.info(filename + " created")

    return filename


def cloneByURL(url, dirname="./"):
    (resource_type, rid) = orm.parseURL(url)

    return clone(resource_type, rid, dirname)


#Upload
def push(filename, credental):
    with open(filename, 'r') as f:
        # Determine its type (caseversion? suite?)
        rtype, rid = orm.parseURL(f.readline())

        if (rtype == 'caseversion'):
            caseversion = orm.parseCaseversion(''.join(f.readlines()))
            # Call forcePushCaseversion or forcePushSuite
            forcePushCaseversion(rid, caseversion, requests, credental)
        elif (rtype == 'suite'):
            raise NotImplementedError

def forcePushCaseversion(rid,  newcaseversion, requestlib, credental):
    # Make sure the number of steps equal
    oldcaseversion = downloadCaseversionById(rid)
    if len(oldcaseversion['steps']) != len(newcaseversion['steps']):
        raise Exception("You can't add or remove steps yet. The test case should have exact same number of steps as it remote one.")

    # Update each steps
    for (oldstep, newstep)in zip(oldcaseversion['steps'], newcaseversion['steps']):

        rtype, rid = orm.parseURL(oldstep['resource_uri'])
        logging.info("Updating " + rtype + " " + rid)

        puturl = "{origin}{uri}?username={username}&api_key={apikey}".format(
                     origin=mtorigin, uri=oldstep['resource_uri'],
                     username=credental['username'],
                     apikey=credental['api_key']
                 )
        headers = {'Content-Type': 'application/json'}
        r = requestlib.put(puturl, data=json.dumps(newstep), headers=headers, timeout=config.networktimeout)
        logging.info(r.status_code)
        logging.debug(r.text)

    # Update case name and descriptions
    puturl = "{origin}{uri}?username={username}&api_key={apikey}".format(
                    origin=mtorigin, uri=oldcaseversion['resource_uri'],
                    username=credental['username'],
                    apikey=credental['api_key']
                )
    headers = {'Content-Type': 'application/json'}
    logging.debug(puturl)
    # FIXME: 504 timeout, don't know why
    r = requestlib.put(puturl, data=json.dumps(newcaseversion), headers=headers, timeout=config.networktimeout)
    logging.info(r.status_code)
    logging.debug(r.text)

