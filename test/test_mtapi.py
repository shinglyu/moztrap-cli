#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append("../")

import unittest
import mock
import json

import urllib2
import requests
import responses # mock requests

import mtapi #SUT


class TestMTApi(unittest.TestCase):
    def setUp(self):
        self.base_url = "https://moztrap-dev.allizom.org"
        mtapi.mtorigin = self.base_url # BAD, see https://trello.com/c/mgl1USB4/69-cleanup-mtapi-mtorigin-settings
#        with open('caseversion_88.out.json', 'r') as f:
#            # self.json_out = ''.join(f.readlines())
#            # self.json_out = ''.join(f.readlines())
#            self.json_out = json.loads(''.join(f.readlines()))
#            #self.json_out = json.dumps(json.load(f))

#    def test_forcePushCaseversion(self):
#        #BODY = "***filecontents***"
#        #conn = Mock(httplib.HTTPConnection("localhost", 8080))
#        #conn.request("PUT", "/file", BODY)
#        #response = conn.getresponse()
#        #print response.status, response.reason
#        mock_conn = mock.Mock(spec=requests)
#        mtapi.forcePushCaseversion(self.json_out, mock_conn)
#        # mock_conn.assert_called_with(mtapi.mtorigin)
#        mock_conn.put.assert_called_with(mtapi.mtorigin, data=json.dumps(self.json_out))
#        # mock_conn.open.assert_called_with('foo')

    def _verify_call_order(self, expecteds, actuals):
        self.assertEqual(len(expecteds), len(actuals))
        for expected, actual in zip(expecteds, actuals):
            self.assertEqual(expected[0] , actual.request.method)
            self.assertIn(expected[1]    , actual.request.url)
    @responses.activate
    def test_init_testcase_object_wout_suite(self):
        responses.add(responses.GET, self.base_url + "/api/v1/" + "product/",# + "?name=Firefox+OS&format=json",
                      body='{ "meta": { "limit": 20, "next": null, "offset": 0, "previous": null, "total_count": 1 }, "objects": [ { "description": "", "id": 115540, "name": "Firefox OS", "productversions": [ { "codename": "", "id": 142229, "product": "/api/v1/product/115540/", "resource_uri": "/api/v1/productversion/142229/", "version": "v2.2" } ], "resource_uri": "/api/v1/product/115540/" } ] }',
                      status=200,
                      content_type="application/json")
        responses.add(responses.POST, self.base_url + "/api/v1/" + "case/",
                      body='{"resource_uri": "/api/v1/case/123"}',
                      status=201, content_type="application/json")
        responses.add(responses.POST, self.base_url + "/api/v1/" + "caseversion/",
                      body='{"resource_uri": "/api/v1/caseversion/12345"}',
                      status=201, content_type="application/json")
        responses.add(responses.POST, self.base_url + "/api/v1/" + "casestep/",
                      body='{"caseversion": "/api/v1/caseversion/12345","resource_uri": "/api/v1/casestep/12"}',
                      status=201, content_type="application/json")
        case = {
            'id': '12345',
            'productname': "Firefox OS",
            'version': 'v2.2',
            'status': 'active',
            'suites': [],
        }
        test_case_obj = mtapi.MozTrapTestCase(case['id'],
                                        case['productname'],
                                        case['version'],
                                        status=case['status'],
                                        suites=case['suites'])
        test_case_obj.add_step("open foo", "see bar")
        test_case_obj.add_step("close foo", "don't see bar")
        #if test_case_obj.existing_in_moztrap():
        #    test_case_obj.update(new_case_version_info={"name": case['id'], "status": case['state'], "tags":[]}, suites=[suite['name']])
        #else:
        test_case_obj.create()

        expecteds = [
            ("GET" , "product"),
            ("POST", "case"),
            ("POST", "caseversion"),
            ("POST", "casestep"),
            ("POST", "casestep"),
        ]
        self._verify_call_order(expecteds, responses.calls)

    @responses.activate
    def test_init_testcase_object_w_suite(self):
        responses.add(responses.GET, self.base_url + "/api/v1/" + "product/",# + "?name=Firefox+OS&format=json",
                      body='{ "meta": { "limit": 20, "next": null, "offset": 0, "previous": null, "total_count": 1 }, "objects": [ { "description": "", "id": 115540, "name": "Firefox OS", "productversions": [ { "codename": "", "id": 142229, "product": "/api/v1/product/115540/", "resource_uri": "/api/v1/productversion/142229/", "version": "v2.2" } ], "resource_uri": "/api/v1/product/115540/" } ] }',
                      status=200,
                      content_type="application/json")
        responses.add(responses.POST, self.base_url + "/api/v1/" + "case/",
                      body='{"resource_uri": "/api/v1/case/123"}',
                      status=201, content_type="application/json")
        responses.add(responses.POST, self.base_url + "/api/v1/" + "suitecase/",
                      body='{"resource_uri": "/api/v1/suitecase/654"}',
                      status=201, content_type="application/json")
        responses.add(responses.POST, self.base_url + "/api/v1/" + "caseversion/",
                      body='{"resource_uri": "/api/v1/caseversion/12345"}',
                      status=201, content_type="application/json")
        responses.add(responses.POST, self.base_url + "/api/v1/" + "casestep/",
                      body='{"caseversion": "/api/v1/caseversion/12345","resource_uri": "/api/v1/casestep/12"}',
                      status=201, content_type="application/json")
        case = {
            'id': '12345',
            'productname': "Firefox OS",
            'version': 'v2.2',
            'status': 'active',
            'suites': ["/api/v1/suite/543"],
        }
        test_case_obj = mtapi.MozTrapTestCase(case['id'],
                                        case['productname'],
                                        case['version'],
                                        status=case['status'],
                                        suites=case['suites'])
        test_case_obj.add_step("open foo", "see bar")
        test_case_obj.add_step("close foo", "don't see bar")
        #if test_case_obj.existing_in_moztrap():
        #    test_case_obj.update(new_case_version_info={"name": case['id'], "status": case['state'], "tags":[]}, suites=[suite['name']])
        #else:
        test_case_obj.create()

        expecteds = [
            ("GET" , "product"),
            ("POST", "case"),
            ("POST", "suitecase"),
            ("POST", "caseversion"),
            ("POST", "casestep"),
            ("POST", "casestep"),
        ]
        self._verify_call_order(expecteds, responses.calls)

    @responses.activate
    def test_init_testcase_object_w_suite(self):
        responses.add(responses.GET, self.base_url + "/api/v1/" + "product/",# + "?name=Firefox+OS&format=json",
                      body='{ "meta": { "limit": 20, "next": null, "offset": 0, "previous": null, "total_count": 1 }, "objects": [ { "description": "", "id": 115540, "name": "Firefox OS", "productversions": [ { "codename": "", "id": 142229, "product": "/api/v1/product/115540/", "resource_uri": "/api/v1/productversion/142229/", "version": "v2.2" } ], "resource_uri": "/api/v1/product/115540/" } ] }',
                      status=200,
                      content_type="application/json")
        responses.add(responses.POST, self.base_url + "/api/v1/" + "case/",
                      body='{"resource_uri": "/api/v1/case/123"}',
                      status=201, content_type="application/json")
        responses.add(responses.POST, self.base_url + "/api/v1/" + "suitecase/",
                      body='{"resource_uri": "/api/v1/suitecase/654"}',
                      status=201, content_type="application/json")
        responses.add(responses.POST, self.base_url + "/api/v1/" + "caseversion/",
                      body='{"resource_uri": "/api/v1/caseversion/12345"}',
                      status=201, content_type="application/json")
        responses.add(responses.POST, self.base_url + "/api/v1/" + "casestep/",
                      body='{"caseversion": "/api/v1/caseversion/12345","resource_uri": "/api/v1/casestep/12"}',
                      status=201, content_type="application/json")
        case = {
            'id': '12345',
            'productname': "Firefox OS",
            'version': 'v2.2',
            'status': 'active',
            'suites': ["/api/v1/suite/543"],
        }
        test_case_obj = mtapi.MozTrapTestCase(case['id'],
                                        case['productname'],
                                        case['version'],
                                        status=case['status'],
                                        suites=case['suites'])
        test_case_obj.add_step("open foo", "see bar")
        test_case_obj.add_step("close foo", "don't see bar")
        #if test_case_obj.existing_in_moztrap():
        #    test_case_obj.update(new_case_version_info={"name": case['id'], "status": case['state'], "tags":[]}, suites=[suite['name']])
        #else:
        test_case_obj.create()

        expecteds = [
            ("GET" , "product"),
            ("POST", "case"),
            ("POST", "suitecase"),
            ("POST", "caseversion"),
            ("POST", "casestep"),
            ("POST", "casestep"),
        ]
        self._verify_call_order(expecteds, responses.calls)

if __name__ == '__main__':
    unittest.main()
