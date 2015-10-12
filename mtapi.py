import urllib2
import json
import os
import logging
import requests
import copy

import config
import orm

logging.getLogger("urllib3").setLevel(logging.WARNING)

productversion = config.productversion
mtorigin = config.mtorigin

namespace_api_base = "/api/v1"
namespace_api_product = namespace_api_base + "/product/"
namespace_api_case = namespace_api_base + "/case/"
namespace_api_suitecase = namespace_api_base + "/suitecase/"
namespace_api_suite = namespace_api_base + "/suite/"
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
        logging.info("Retriving product information from " + base_url)
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
    product_name = None
    product_uri = None
    product_version = None
    product_version_uri = None
    description = None
    id_prefix = None
    status = None
    suites = []
    steps = []
    tags = []
    step_current_no = 0
    case_version_objs = None
    case_version_id = None
    case_uri = None

    def __init__(self, name, product_name, product_version, case_version_id=None,
                 status="active", description=None, steps=None, id_prefix=mz_case_id_prefix, suites=None):
        self.name, self.description, self.status, self.case_version_id = name, description, status, case_version_id
        self.suites = copy.deepcopy(suites)
        self.product_name, self.product_version = product_name, product_version
        self.product_uri, self.product_version_uri = get_product_uri(product_name, product_version)
        if (steps is None): #http://stackoverflow.com/questions/1132941/least-astonishment-in-python-the-mutable-default-argument
            self.steps = []
        else:
            self.steps = steps
        self.id_prefix = id_prefix
        if user_params is None:
            logging.error("Please set user params before init the MozTrapTest case!!!")
        logging.info("Test case \"" + name + "\" created")

    def _create_test_steps(self, case_version_uri):
        base_url = mtorigin + namespace_api_case_step
        for step in self.steps:
            logging.info("Creating step for case " + self.name)

            data = {"caseversion": case_version_uri,
                    "instruction": step['instruction'],
                    "expected": step['expected'],
                    "number": step['number']}
            logging.info('POST ' + base_url)
            resp = requests.post(base_url, params=user_params, data=json.dumps(data), headers=headers)
            step['resource_uri'] = resp.json()['resource_uri']
            step['caseversion'] = resp.json()['caseversion']
            _check_respone_code(resp)
        return

    def _create_test_case(self):
        test_data = {'product': self.product_uri, 'idprefix': self.id_prefix}
        base_url = mtorigin + namespace_api_case
        logging.info('POST ' + base_url)
        resp = requests.post(base_url, params=user_params, data=json.dumps(test_data), headers=headers)
        _check_respone_code(resp)
        return resp

    def _create_suite_case_relation(self, case_uri, suite_uri):
        logging.info("Adding the case " + case_uri + "to suite " + suite_uri)
        test_data = {'case': case_uri, 'suite': suite_uri}
        base_url = mtorigin + namespace_api_suitecase
        logging.info('POST ' + base_url)
        resp = requests.post(base_url, params=user_params, data=json.dumps(test_data), headers=headers)
        _check_respone_code(resp)
        return resp

    def _delete_suite_case_relation(self, case_uri, suite_uri):
        logging.info("Removing the case " + case_uri + "from suite " + suite_uri)
        case_id = os.path.basename(os.path.dirname(case_uri))
        suite_id = os.path.basename(os.path.dirname(suite_uri))

        base_url = mtorigin + namespace_api_suitecase
        params = {'case': case_id, 'suite': suite_id}
        suitecase_resp = requests.get(base_url, params=params, headers=headers)
        _check_respone_code(suitecase_resp)

        suitecase_id = suitecase_resp.json()['objects'][0]['id']
        logging.info('DELETE ' + base_url + str(suitecase_id) + "/")
        params = copy.deepcopy(user_params)
        params['permanent'] = True
        resp = requests.delete(base_url + str(suitecase_id) + "/", params=params, headers=headers)
        _check_respone_code(resp)
        return resp

    def _create_test_case_version(self, case_uri):
        test_data = {"productversion": self.product_version_uri, "case": case_uri, "name": self.name,
                     "description": self.description, "status": self.status, "tags": self.tags}
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

    def existing_in_moztrap(self):
        logging.info("Checking if the test case exists in moztrap")
        self.case_version_objs = self._get_case_version_objs()
        if len(self.case_version_objs) > 0:
            if len(self.case_version_objs) == 1:
                self.case_version_id = self.case_version_objs[0]['id']
            return True
        else:
            return False

    def clean_steps(self):
        self.steps = []
        self.step_current_no = 0

    def update_step(self, instruction, expected, number):
        update_success = False
        for step in self.steps:
            if step['number'] == number:
                step['instruction'] = instruction
                step['expected'] = expected
                update_success = True
        if update_success is False:
            logging.error("can't find the step number in current steps: " + str(self.steps))

    def add_step(self, instruction, expected, number=0):
        logging.info("Adding test step to case " + self.name)
        if number == 0:
            self.step_current_no += 1
            number = self.step_current_no
        self.steps.append({"instruction": instruction, "expected": expected, "number": number})

    def add_tag(self, name, description=None):
        logging.info("Adding tag to case " + self.name)
        tag_uri_resp = self._get_tag_uri(name).json()
        if len(tag_uri_resp['objects']) > 0:
            tag_uri = tag_uri_resp['objects'][0]['resource_uri']
        else:
            tag_uri = self._create_tag(name, description).json()['resource_uri']
        self.tags.append(tag_uri)

    def create(self):
        logging.info("Creating the test case in moztrap")

        case_uri_resp = self._create_test_case().json()
        case_uri = case_uri_resp['resource_uri']
        for suite_uri in self.suites:
            self._create_suite_case_relation(case_uri, suite_uri)
        case_version_uri_resp = self._create_test_case_version(case_uri).json()
        case_version_uri = case_version_uri_resp['resource_uri']
        self._create_test_steps(case_version_uri)
        return case_version_uri_resp

    def delete(self):
        logging.info("Delete the test case in moztrap")

        if self.case_version_id is None:
            logging.error("Please specify the suite id want to kill!")

        base_url = mtorigin + namespace_api_case_version
        request_url = base_url + str(self.case_version_id) + "/"
        logging.info('DELETE' + request_url)
        resp = requests.delete(request_url, params=user_params, headers=headers)
        _check_respone_code(resp)
        return resp

    def _get_case_version_objs(self):
        return_objs = None
        if self.case_version_id is None:
            query_params = {"name": self.name, "productversion__product__name": self.product_name,
                            "productversion__version": self.product_version, "format": data_format}
            base_url = mtorigin + namespace_api_case_version
        else:
            query_params = {"format": data_format}
            base_url = mtorigin + namespace_api_case_version + str(self.case_version_id) + "/"

        resp = requests.get(base_url, params=query_params, headers=headers)



        if self.case_version_id is None:
            _check_respone_code(resp)
            return_objs = resp.json()['objects']
        else:
            if resp.status_code == 404:
                logging.error("can't find the test case version with specify id: " + str(self.case_version_id))
                return_objs = []
            else:
                return_objs = [resp.json()]
        return return_objs

    def _get_case_uri(self):
        if self.case_uri is not None:
            return self.case_uri
        else:
            self.case_uri = self.case_version_objs[0]['case']
            return self.case_uri
        #return_objs = None
        #query_params = {"name": self.name, "product__name": self.product_name, "format": data_format}
        #base_url = mtorigin + namespace_api_case
        #resp = requests.get(base_url, params=query_params, headers=headers)
        #if resp.status_code == 404:
            #logging.error("can't find the test case with specify name: " + str(self.name))
            #return_objs = []
        #else:
            #return_objs = resp.json()['objects']
        ##print return_objs
        #self.case_uri = return_objs[0]['resource_uri']
        #return self.case_uri

    def _clean_old_steps(self, case_steps):
        for step in case_steps:
            base_url = mtorigin + step['resource_uri']
            params = copy.deepcopy(user_params)
            params['permanent'] = True
            resp = requests.delete(base_url, params=params)
            _check_respone_code(resp)

    def _update_case_steps(self, case_version_uri, case_steps):
        #self.caseversion_objs is retrived in update()
        remote_steps = self.case_version_objs[0]['steps']
        step_no = 1
        for local_step, remote_step in map(None, case_steps, remote_steps):
            if remote_step is None:
                base_url = mtorigin + namespace_api_case_step
                logging.info("Creating step for case " + self.name)

                data = {"caseversion": case_version_uri,
                        "instruction": local_step['instruction'],
                        "expected": local_step['expected'],
                        "number": step_no}
                logging.info('POST ' + base_url)
                resp = requests.post(base_url, params=user_params, data=json.dumps(data), headers=headers)
                #step['resource_uri'] = resp.json()['resource_uri']
                #step['caseversion'] = resp.json()['caseversion']
                _check_respone_code(resp)
            elif local_step is None: #and remote_step is not None:
                base_url = mtorigin + remote_step['resource_uri']
                params = copy.deepcopy(user_params)
                params['permanent'] = True
                resp = requests.delete(base_url, params=params)
                _check_respone_code(resp)
                #delete remote step
            else:
                base_url = mtorigin + remote_step['resource_uri']
                resp = requests.put(base_url, params=user_params, data=json.dumps(local_step), headers=headers)
                _check_respone_code(resp)

            step_no += 1


        #import pdb
        #pdb.set_trace()
        #self._clean_old_steps(case_steps) # just put, dont' delete
        #self._create_test_steps(case_version_uri)
        return

    def _update_case_version(self, case_version_uri, new_case_version_info):
        base_url = mtorigin + case_version_uri
        resp = requests.put(base_url, params=user_params, data=json.dumps(new_case_version_info), headers=headers)
        _check_respone_code(resp)
        for key_name in ["name", "description", "status", "tags", "steps"]:
            if key_name in new_case_version_info.keys():
                self.__dict__.__setitem__(key_name, new_case_version_info[key_name])
        return resp

    #def _update_case_suite_relation(self):
    #    if self.suites is not None:
    #        case_info_list = self._get_case_uri()
    #        for case_info in case_info_list:
    #            for suite_uri in self.suites:
    #                test_data = {'case': case_info['resource_uri'], 'suite': suite_uri}
    #                base_url = mtorigin + namespace_api_suitecase + str(case_info['id']) #BUG HERE
    #                resp = requests.put(base_url, params=user_params, data=json.dumps(test_data), headers=headers)
    #                _check_respone_code(resp)

    def update(self, new_case_version_info=None, suites_added=None, suites_removed=None): #perhaps we need the suites here,
        #The self.suites should reflect the upstram suites, suites here should be what it want it to be
        logging.info("Updating the test case on moztrap")
        #self._update_case_suite_relation()
        #import pdb
        #pdb.set_trace()
        self.case_version_objs = self._get_case_version_objs()
        if len(self.case_version_objs) == 1:
            case_version_uri = self.case_version_objs[0]['resource_uri']
            #case_steps = self.case_version_objs[0]['steps']
            case_steps = self.steps
            self._update_case_steps(case_version_uri, case_steps)
            if new_case_version_info:
                self._update_case_version(case_version_uri, new_case_version_info)
            if (suites_added is not None):
                case_uri = self._get_case_uri()
                for suite in suites_added:
                    self._create_suite_case_relation(case_uri, suite)
            if (suites_removed is not None):
                case_uri = self._get_case_uri()
                for suite in suites_removed:
                    self._delete_suite_case_relation(case_uri, suite)

        elif len(self.case_version_objs) == 0:
            logging.error("Can't find any case fulfill the attributes (%s,%s,%s)" % (self.name, self.product_name, self.product_version))
        else:
            for case_version_obj in self.case_version_objs:
                logging.error("Duplicate case name exist in system, can't do the update! case version uri: " + case_version_obj['productversion'])


class MozTrapTestSuite(object):
    name = None
    product_name = None
    product_uri = None
    product_version = None
    product_version_uri = None
    description = None
    status = None
    suite_id = None
    suite_uri = None
    suite_objs = None

    def __init__(self, name, product_name, product_version, status="active", description=None):
        self.name, self.description, self.status = name, description, status
        self.product_name, self.product_version = product_name, product_version
        self.product_uri, self.product_version_uri = get_product_uri(product_name, product_version)
        if user_params is None:
            logging.error("Please set user params before init the MozTrapTest case!!!")
        logging.info("Suite " + name + " created")

    def _get_suite_objs(self):
        return_objs = None
        query_params = {"name": self.name, "product__name": self.product_name, "format": data_format}
        base_url = mtorigin + namespace_api_suite
        resp = requests.get(base_url, params=query_params, headers=headers)
        if resp.status_code == 404:
            logging.error("can't find the test suite with specify name: " + str(self.name) + " and specify product:" + str(self.product_name))
            return_objs = []
        else:
            return_objs = copy.deepcopy(resp.json()['objects'])
        return return_objs

    def _create_test_suite(self):
        test_data = {'product': self.product_uri, 'name': self.name, 'description': self.description, 'status': self.status}
        base_url = mtorigin + namespace_api_suite
        logging.info('POST ' + base_url)
        resp = requests.post(base_url, params=user_params, data=json.dumps(test_data), headers=headers)
        _check_respone_code(resp)
        return resp

    def _delete_test_suite(self, specify_id=None):
        if specify_id is None and self.suite_id is None:
            logging.error("Please specify the suite id want to kill!")
        if specify_id is None:
            request_id = self.suite_id
        else:
            request_id = specify_id
        base_url = mtorigin + namespace_api_suite
        request_url = base_url + str(request_id)
        logging.info('DELETE' + base_url)
        resp = requests.delete(request_url, params=user_params, headers=headers)
        _check_respone_code(resp)
        return resp

    def _update_test_suite(self, name=None, description=None, status=None, product_info=None):
        test_data = {}
        if product_info is not None:
            self.product_uri, self.product_version_uri = get_product_uri(product_info['product_name'], product_info['product_version'])
            test_data['product'] = self.product_uri
        if name is not None:
            self.name = name
            test_data['name'] = self.name
        if description is not None:
            self.description = description
            test_data['description'] = self.description
        if status is not None:
            self.status = status
            test_data['status'] = self.status
        request_url = mtorigin + namespace_api_suite + str(self.suite_id)
        logging.info('DELETE ' + request_url)
        resp = requests.put(request_url, params=user_params, data=json.dumps(test_data), headers=headers)
        _check_respone_code(resp)
        return resp

    def create(self):
        logging.info("Creating the suite on moztrap")
        suite_uri_resp = self._create_test_suite().json()
        self.suite_id = suite_uri_resp['id']
        self.suite_uri = suite_uri_resp['resource_uri']
        return suite_uri_resp

    def delete(self, specify_id=None):
        logging.info("Deleting the suite on moztrap")
        suite_delete_resp = self._delete_test_suite(specify_id)
        return suite_delete_resp

    def update(self, name=None, description=None, status=None, product_info=None):
        logging.info("Updating the suite on moztrap")
        suite_update_resp = self._update_test_suite(name, description, status, product_info)
        return suite_update_resp

    def should_update(self):
        logging.info("Checking if the suite has been modified")
        if (self.suite_objs[0]['name'] != self.name or
            self.suite_objs[0]['status'] != self.status or
            self.suite_objs[0]['description'] != self.description):
            logging.info("Suite has been modified")
            return True
        else:
            logging.info("Suite has not been modified")
            return False

    def existing_in_moztrap(self):
        logging.info("Checking if the suite exists in moztrap")
        self.suite_objs = self._get_suite_objs()
        if len(self.suite_objs) == 1:
            self.suite_id = self.suite_objs[0]['id']
            self.suite_uri = self.suite_objs[0]['resource_uri']
            return True
        elif len(self.suite_objs) > 1:
            raise Exception("The suite is ambiguous, please make sure the suite is unique on the MozTrap server")
        else:
            return False



# Download
def downloadCaseversionById(cid): # query = query.replace(" ", "\%20")
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
    #logging.debug(url)
    data = urllib2.urlopen(url).read()
    parsed = json.loads(data)
    #logging.debug(parsed)
    return parsed['objects'][0]

def downloadSuiteById(sid):
    # TODO: move "Downloading..." to here
    url = (mtorigin + "/api/v1/caseversion/"
           "?case__suites={sid}"
           "&limit=0&format=json"
          ).format(sid=sid, productversion=productversion)
    #logging.debug(url)
    data = urllib2.urlopen(url).read()
    return json.loads(data)

def getSuiteName(sid):
    url = (mtorigin + "/api/v1/suite/{sid}"
           "?limit=0&format=json"
          ).format(sid=sid)
    data = urllib2.urlopen(url).read()
    return json.loads(data)['name']

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
        sname = getSuiteName(sid)
        output = orm.formatSuite(result, sname)

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

def forcePushCaseversion(newcaseversion, credential, case_version_id=None, product_info=None):
    set_user_params(credential['username'], credential['api_key'])
    if product_info is None:
        product_info = {'name': config.defaultProduct, 'version': config.defaultVersion}
    test_case_obj = MozTrapTestCase(newcaseversion['name'], product_info['name'], product_info['version'],
                                    case_version_id=case_version_id)
    for step in newcaseversion['steps']:
        test_case_obj.add_step(step['instruction'], step['expected'])
    if test_case_obj.existing_in_moztrap():
        test_case_obj.update(newcaseversion)
    else:
        logging.error("Can't find test case on moztrap!")

def forcePushSuite(sid, newsuite, requestlib, credental):
    oldsuite = downloadSuiteById(sid)
    if len(oldsuite['objects']) != len(newsuite['objects']):
        raise Exception("You can't add or remove cases from a suite yet. Remote version has {0} cases, local version has {1} cases".format(len(oldsuite['objects']), len(newsuite['objects'])))

    # FIXME: potential ordering problem, text is sorted by id
    for (oldcaseversion, newcaseversion) in map(None,
                                                sorted(oldsuite['objects'], key=lambda x: x['id']),
                                                newsuite['objects']):
        rtype, rid = orm.parseURL(oldcaseversion['resource_uri'])
        ##print(newcaseversion['name'])
        oldcaseversionCmp = copy.deepcopy(oldcaseversion)
        oldcaseversionCmp.pop('resource_uri', None) #FIXME: don't do this after resource_uri is parsed
        if(orm.formatCaseversion(oldcaseversionCmp) == orm.formatCaseversion(newcaseversion)):
            logging.info("No change for caseversion {0}, skipping".format(oldcaseversion['id']))
        else:
            forcePushCaseversion(rid, newcaseversion, requestlib, credental)


def convert_mark_file_into_moztrap(filename, credential, product_info=None):
    set_user_params(credential['username'], credential['api_key']) #TODO
    if product_info is None:
        # TODO: read product from test case namespace id
        product_info = {'name': config.defaultProduct, 'version': config.defaultVersion}
    with open(filename, 'r') as f:
        # Determine its type (caseversion? suite?)
        cases = orm.parseSuite(''.join(f.readlines()))
        for case in cases['objects']:
            # FIXME:  HRADCODE                                  v---------------
            test_case_obj = MozTrapTestCase(case['name'], product_info['name'], product_info['version'])
            for step in case['steps']:
                test_case_obj.add_step(step['instruction'], step['expected'])
            if test_case_obj.existing_in_moztrap():
                test_case_obj.update()
            else:
                test_case_obj.create()

def load_json_into_moztrap(filename, credential, product_info=None):
    set_user_params(credential['username'], credential['api_key']) #TODO
    if product_info is None:
        # TODO: read product from test case namespace id
        product_info = {'name': config.defaultProduct, 'version': config.defaultVersion}
    with open(filename, 'r') as f:
        # Determine its type (caseversion? suite?)
        suites = json.load(f)
        for suite in suites:
            test_suite_obj = MozTrapTestSuite(suite['name'], product_info['name'], product_info['version'])
            if test_suite_obj.existing_in_moztrap() is False:
                test_suite_obj.create()
            for case in suite['testcases']:
                test_case_obj = MozTrapTestCase(case['id'], product_info['name'], product_info['version'], status=case['state'], suites=[test_suite_obj.suite_uri])

                test_case_obj.add_step(case['instructions'], "")
                _add_all_type_of_variables_if_exist(test_case_obj, case)

                if test_case_obj.existing_in_moztrap():
                    test_case_obj.update(new_case_version_info={"name": case['id'], "status": case['state'], "tags":[]}, suites=[suite['name']])
                else:
                    test_case_obj.create()

def _create_case_obj_from_parser_output(parser_output, product_info, suite_name_to_uri):
    if not isinstance(parser_output['instructions'], list):
        steps = [{'instruction':parser_output['instructions'],
                  'expected': "",
                  'number': 0
                  }]
    else:
        steps = parser_output['instructions']
    return MozTrapTestCase(name=parser_output['id'],
                           product_name=product_info['name'],
                           product_version=product_info['version'],
                           status=parser_output['state'],
                           suites=map(lambda x: suite_name_to_uri[x], parser_output['suites']),
                           steps=steps
                          )

def sync_diff_to_moztrap(diffs, credential, product_info=None):
    set_user_params(credential['username'], credential['api_key']) #TODO
    if product_info is None:
        # TODO: read product from test case namespace id
        product_info = {'name': config.defaultProduct, 'version': config.defaultVersion}
    suite_name_to_uri = {}
    suite_remove_queue = []
    for diff in diffs:
        for newsuite in diff['suite']['added']:
            #TODO: use different product for different suite?
            test_suite_obj = MozTrapTestSuite(newsuite, product_info['name'], product_info['version'])
            test_suite_obj.create()
            if newsuite not in suite_name_to_uri:
                suite_name_to_uri[newsuite] = test_suite_obj.suite_uri

        for suite in diff['suite']['existing']:
            #TODO: use different product for different suite?
            test_suite_obj = MozTrapTestSuite(suite, product_info['name'], product_info['version'])
            test_suite_obj.existing_in_moztrap()
            if (suite not in suite_name_to_uri):
                suite_name_to_uri[suite] = test_suite_obj.suite_uri

        for suite in diff['suite']['removed']:
            #TODO: use different product for different suite?
            test_suite_obj = MozTrapTestSuite(suite, product_info['name'], product_info['version'])
            test_suite_obj.existing_in_moztrap()
            suite_name_to_uri[suite] = test_suite_obj.suite_uri
            suite_remove_queue.append(test_suite_obj)

        for newcase in diff['case']['added']:
            #TODO: use different product for different suite?
            test_case_obj= _create_case_obj_from_parser_output(newcase, product_info, suite_name_to_uri)
            test_case_obj.create()

        for modifiedcase in diff['case']['modified']:
            #TODO: use different product for different suite?
            test_case_obj = _create_case_obj_from_parser_output(modifiedcase, product_info, suite_name_to_uri)
            #test_case_obj.existing_in_moztrap()
            #TODO: add modifiedcase['suites-added/removed '] to update paramter
            new_case_version_info = {
                "name": modifiedcase['id'],
                "status": modifiedcase['state'],
                "tags": [],#TODO
            }
            test_case_obj.update(new_case_version_info=new_case_version_info,
                                 suites_added = map(lambda x: suite_name_to_uri[x], modifiedcase['suites_added']),
                                 suites_removed = map(lambda x: suite_name_to_uri[x], modifiedcase['suites_removed']))

        for removecase in diff['case']['removed']:
            #TODO: use different product for different suite?
            test_case_obj = _create_case_obj_from_parser_output(removecase, product_info, suite_name_to_uri)
            #test_case_obj.existing_in_moztrap()
            #TODO: add modifiedcase['suites-added/removed '] to update paramter
            test_case_obj.existing_in_moztrap()
            test_case_obj.delete()

        # Suites need to removed last, since it's suitecase relation will be
        # deleted in previous steps
        for suite_obj in suite_remove_queue:
            suite_obj.delete()

def _add_all_type_of_variables_if_exist(test_case_obj, case):
    for i in ('variables', 'variablesFromSuite'):
        try:
            _add_variables_if_exist(test_case_obj, case[i])
        except KeyError:
            # We accept jsons that don't contain a (or any) key mentioned above
            pass

def _add_variables_if_exist(test_case_obj, variables):
    for variable in variables:
        test_case_obj.add_step(variable, '')
