import urllib2
import json
import os
import httplib
import logging
import requests

import orm

productversion="v2.2" #FIXME: hardcoded

# mtorigin = "https://moztrap.mozilla.org"
#mtorigin = "http://0.0.0.0:8080"
mtorigin = "http://127.0.0.1:8000"
# mtorigin = "http://requestb.in/1b8n1md1"

# Download
def downloadCaseversionById(cid):
    # query = query.replace(" ", "\%20")
    # baseurl = "https://developer.mozilla.org/en-US/search?format=json&q="
    baseURL = mtorigin + "/api/v1/caseversion/"
    url = baseURL + str(cid) + "/"
    url = url + "?format=json"
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


#Upload


def push(filename):
    with open(filename, 'r') as f:
        # Determine its type (caseversion? suite?)
        rtype, rid = orm.parseURL(f.readline())

        if (rtype == 'caseversion'):
            caseversion = orm.parseCaseversion(''.join(f.readlines()))
            # Call forcePushCaseversion or forcePushSuite
            forcePushCaseversion(rid, caseversion, requests)
        elif (rtype == 'suite'):
            raise NotImplementedError

def forcePushCaseversion(rid,  newcaseversion, requestlib):
    # Make sure the number of steps equal
    oldcaseversion = downloadCaseversionById(rid)
    #print len(oldcaseversion['steps'])
    #print len(newcaseversion['steps'])
    credental = {'username': 'admin-django', 'api_key': 'c67c9af7-7e07-4820-b686-5f92ae94f6c9' } # FIXME: hardcode
    if len(oldcaseversion['steps']) != len(newcaseversion['steps']):
        raise Exception("You can't add or remove steps yet. The test case should have exact same number of steps as it remote one.")

    puturl = "{origin}{uri}?username={username}&api_key={apikey}".format(
                    origin=mtorigin, uri=oldcaseversion['resource_uri'],
                    username=credental['username'],
                    apikey=credental['api_key']
                )
    headers = {'Content-Type': 'application/json'}
    r = requestlib.put(puturl, data=json.dumps(newcaseversion), headers=headers)
    logging.info(r.status_code)
    logging.debug(r.text)

    for (oldstep, newstep)in zip(oldcaseversion['steps'], newcaseversion['steps']):

        rtype, rid = orm.parseURL(oldstep['resource_uri'])
        logging.info("Updating " + rtype + " " + rid)

        puturl = "{origin}{uri}?username={username}&api_key={apikey}".format(
                     origin=mtorigin, uri=oldstep['resource_uri'],
                     username=credental['username'],
                     apikey=credental['api_key']
                 )
        headers = {'Content-Type': 'application/json'}
        r = requestlib.put(puturl, data=json.dumps(newstep), headers=headers)
        logging.info(r.status_code)
        logging.debug(r.text)
    #TODO:  update description and title too
