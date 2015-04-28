import urllib2
import json
import os
import httplib
import logging
import requests
import copy

import config
import orm

productversion = config.productversion
mtorigin = config.mtorigin

namespace_api_base = "/api/v1"
namespace_api_product = namespace_api_base + "/product/"
namespace_api_case = namespace_api_base + "/case/"
namespace_api_case_version = namespace_api_base + "/caseversion/"
namespace_api_case_step = namespace_api_base + "/casestep/"
namespace_api_tag = namespace_api_base + "/tag/"

headers = {'Content-Type': 'application/json'}
data_format = "json"
mz_case_id_prefix = "git"
user_params = None


def set_user_params(uname, akey, format=None):
    global user_params
    if format is None:
        format = data_format
    user_params = {"username": uname, "api_key": akey, "format": format}


def _check_respone_code(check_response):
    if check_response.status_code not in [200, 201]:
        logging.error("Send the request to url: %s" % str(check_response.url))
        logging.error("Got the return code: %s, the response is: %s" % (str(check_response.status_code), str(check_response.text)))
        return False
    return True


def get_product_uri(name, version):
        return_val = None
        params = {"name": name, "format": data_format}
        base_url = mtorigin + namespace_api_product
        resp = requests.get(base_url, params=params)
        if _check_respone_code(resp):
            product_obj_json = resp.json()['objects'][0]
            product_uri = product_obj_json['resource_uri']
            for product_version in product_obj_json['productversions']:
                if product_version['version'] == unicode(version):
                    product_version_uri = product_version['resource_uri']
            if product_version_uri is None:
                logging.error("can't get product_version!!")
            return_val = (product_uri, product_version_uri)
        return return_val


class MozTrapTestCase(object):
    name = None
    product_uri = None
    product_version_uri = None
    description = None
    id_prefix = None
    steps = []
    tags = []
    step_current_no = 0

    def __init__(self, name, product_name, product_version, steps=[], id_prefix=mz_case_id_prefix):
        self.name = name
        self.product_uri, self.product_version_uri = get_product_uri(product_name, product_version)
        self.steps = steps
        self.id_prefix = id_prefix
        if user_params is None:
            logging.error("Please set user params before init the MozTrapTest case!!!")

    def _create_test_steps(self, case_version_uri):
        base_url = mtorigin + namespace_api_case_step
        for step in self.steps:
            data = {"caseversion": case_version_uri, "instruction": step['instruction'],
                    "expected": step['expected'], "number": step['number']}
            resp = requests.post(base_url, params=user_params, data=json.dumps(data), headers=headers)
            _check_respone_code(resp)
        return resp

    def _create_test_case(self):
        test_data = {'product': self.product_uri, 'idprefix': self.id_prefix}
        base_url = mtorigin + namespace_api_case
        resp = requests.post(base_url, params=user_params, data=json.dumps(test_data), headers=headers)
        _check_respone_code(resp)
        return resp

    def _create_test_case_version(self, case_uri):
        test_data = {"productversion": self.product_version_uri, "case": case_uri, "name": self.name,
                     "description": self.description, "status": "active", "tags": self.tags}
        base_url = mtorigin + namespace_api_case_version
        resp = requests.post(base_url, params=user_params, data=json.dumps(test_data), headers=headers)
        _check_respone_code(resp)
        return resp

    def _get_tag_uri(self, name):
        params = {"name": name, "format": data_format}
        base_url = mtorigin + namespace_api_tag
        resp = requests.get(base_url, params=params)
        _check_respone_code(resp)
        return resp

    def _create_tag(self, name, description):
        test_data = {"name": name, "product": self.product_uri, "description": description}
        base_url = mtorigin + namespace_api_tag
        resp = requests.post(base_url, params=user_params, data=json.dumps(test_data), headers=headers)
        _check_respone_code(resp)
        return resp

    def add_step(self, instruction, expected, number=0):
        if number == 0:
            self.step_current_no += 1
            number = self.step_current_no
        self.steps.append({"instruction": instruction, "expected": expected, "number": number})

    def add_tag(self, name, description=None):
        tag_uri_resp = self._get_tag_uri(name).json()
        if len(tag_uri_resp['objects']) > 0:
            tag_uri = tag_uri_resp['objects'][0]['resource_uri']
        else:
            tag_uri = self._create_tag(name, description).json()['resource_uri']
        self.tags.append(tag_uri)

    def create(self):
        case_uri_resp = self._create_test_case().json()
        case_uri = case_uri_resp['resource_uri']
        case_version_uri_resp = self._create_test_case_version(case_uri).json()
        case_version_uri = case_version_uri_resp['resource_uri']
        self._create_test_steps(case_version_uri)

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
    logging.debug(url)
    data = urllib2.urlopen(url).read()
    parsed = json.loads(data)
    logging.debug(parsed)
    return parsed['objects'][0]


def downloadSuiteById(sid):
    # TODO: move "Downloading..." to here
    url = (mtorigin + "/api/v1/caseversion/"
           "?case__suites={sid}"
           "&limit=0&format=json"
          ).format(sid=sid, productversion=productversion)
    logging.debug(url)
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
        logging.info("Downloading Case " + query + " ...")
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
        rtype, rid = orm.parseURL(f.readline()) # TODO: do we need to extract the first line here? or in parse*

        if (rtype == 'caseversion'):
            caseversion = orm.parseCaseversion(''.join(f.readlines()))
            # Call forcePushCaseversion or forcePushSuite
            forcePushCaseversion(rid, caseversion, requests, credental)
        elif (rtype == 'suite'):
            suite = orm.parseSuite(''.join(f.readlines()))
            forcePushSuite(rid, suite, requests, credental)

def forcePushCaseversion(rid,  newcaseversion, requestlib, credental):
    # Make sure the number of steps equal
    oldcaseversion = downloadCaseversionById(rid)
    #if len(oldcaseversion['steps']) > len(newcaseversion['steps']):
        #raise Exception("You can't remove steps yet. The test case should have the same number or moreof steps as it remote one.")

    # Update each steps
    # map(None, ...) is a padding version of zip()
    number = 1
    for (oldstep, newstep) in map(None, oldcaseversion['steps'], newcaseversion['steps']):

        if oldstep is None:
            #rtype, rid = orm.parseURL(oldstep['resource_uri'])
            logging.info("Creating new step")

            puturl = "{origin}{uri}?username={username}&api_key={apikey}".format(
                        origin=mtorigin, uri="/api/v1/casestep/",
                        username=credental['username'],
                        apikey=credental['api_key']
                    )
            logging.debug(puturl)
            newstep['caseversion'] = oldcaseversion['resource_uri'] # TODO: move this to orm::parseCaseversion?
            r = requestlib.post(puturl, data=json.dumps(newstep), headers=headers, timeout=config.networktimeout)
            logging.info(r.status_code)
            logging.debug(r.text)

        elif newstep is None:
            logging.info("Deleting old step")

            puturl = "{origin}{uri}?username={username}&api_key={apikey}".format(
                        origin=mtorigin,
                        uri=oldstep['resource_uri'],
                        username=credental['username'],
                        apikey=credental['api_key']
                    )
            logging.debug(puturl)
            r = requestlib.delete(puturl, headers=headers, timeout=config.networktimeout)
            logging.info(r.status_code)
            logging.debug(r.text)

        else:
            rtype, rid = orm.parseURL(oldstep['resource_uri'])
            logging.info("Updating " + rtype + " " + rid)

            puturl = "{origin}{uri}?username={username}&api_key={apikey}".format(
                        origin=mtorigin,
                        uri=oldstep['resource_uri'],
                        username=credental['username'],
                        apikey=credental['api_key']
                    )
            r = requestlib.put(puturl, data=json.dumps(newstep), headers=headers, timeout=config.networktimeout)
            logging.info(r.status_code)
            logging.debug(r.text)
        number += 1

    # Update case name and descriptions
    puturl = "{origin}{uri}?username={username}&api_key={apikey}".format(
                    origin=mtorigin, uri=oldcaseversion['resource_uri'],
                    username=credental['username'],
                    apikey=credental['api_key']
                )
    logging.debug(puturl)
    # FIXME: 504 timeout, don't know why
    r = requestlib.put(puturl, data=json.dumps(newcaseversion), headers=headers, timeout=config.networktimeout)
    logging.info(r.status_code)
    logging.debug(r.text)

def forcePushSuite(sid, newsuite, requestlib, credental):
    oldsuite = downloadSuiteById(sid)
    if len(oldsuite['objects']) != len(newsuite['objects']):
        raise Exception("You can't add or remove cases from a suite yet. Remote version has {0} cases, local version has {1} cases".format(len(oldsuite['objects']), len(newsuite['objects'])))

    # FIXME: potential ordering problem, text is sorted by id
    for (oldcaseversion, newcaseversion) in map(None,
                                                sorted(oldsuite['objects'], key=lambda x: x['id']),
                                                newsuite['objects']):
        rtype, rid = orm.parseURL(oldcaseversion['resource_uri'])
        #print(newcaseversion['name'])
        oldcaseversionCmp = copy.deepcopy(oldcaseversion)
        oldcaseversionCmp.pop('resource_uri', None) #FIXME: don't do this after resource_uri is parsed
        if(orm.formatCaseversion(oldcaseversionCmp) == orm.formatCaseversion(newcaseversion)):
            logging.info("No change for caseversion {0}, skipping".format(oldcaseversion['id']))
        else:
            forcePushCaseversion(rid, newcaseversion, requestlib, credental)
