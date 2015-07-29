#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append("../")

import unittest
import mock
# import json

# import urllib2
# import requests
import responses  # mock requests

import mtapi  # SUT


class TestMTApi(unittest.TestCase):
    def setUp(self):
        self.base_url = "https://moztrap-dev.allizom.org"
        mtapi.mtorigin = self.base_url  # BAD,
        # see https://trello.com/c/mgl1USB4/69-cleanup-mtapi-mtorigin-settings

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
    def test_create_suite_obj(self):
        responses.add(responses.GET, self.base_url + "/api/v1/" + "product/",# + "?name=Firefox+OS&format=json",
                      body='{ "meta": { "limit": 20, "next": null, "offset": 0, "previous": null, "total_count": 1 }, "objects": [ { "description": "", "id": 115540, "name": "Firefox OS", "productversions": [ { "codename": "", "id": 142229, "product": "/api/v1/product/115540/", "resource_uri": "/api/v1/productversion/142229/", "version": "v2.2" } ], "resource_uri": "/api/v1/product/115540/" } ] }',
                      status=200,
                      content_type="application/json")
        responses.add(responses.POST, self.base_url + "/api/v1/" + "suite/",
                      body='{ "description": "This is an awesome suite", "id": 888, "name": "Test Suite", "product": "/api/v1/product/115540/", "resource_uri": "/api/v1/suite/888/", "status": "active" }',
                      status=201, content_type="application/json")
        suite = [
            'Test Suite',
            'Firefox OS',
            'v2.2',
            'active',
            'This is an awesome suite'
        ]
        test_suite_obj= mtapi.MozTrapTestSuite(*suite)
        #if test_case_obj.existing_in_moztrap():
        #    test_case_obj.update(new_case_version_info={"name": case['id'], "status": case['state'], "tags":[]}, suites=[suite['name']])
        #else:
        test_suite_obj.create()

        expecteds = [
            ("GET" , "product"),
            ("POST", "suite"),
        ]
        self._verify_call_order(expecteds, responses.calls)
        self.assertEqual(test_suite_obj.suite_uri, "/api/v1/suite/888/")

    @responses.activate
    def test_suite_init_doesnt_exist(self):
        responses.add(responses.GET, self.base_url + "/api/v1/" + "product/",# + "?name=Firefox+OS&format=json",
                      body='{ "meta": { "limit": 20, "next": null, "offset": 0, "previous": null, "total_count": 1 }, "objects": [ { "description": "", "id": 115540, "name": "Firefox OS", "productversions": [ { "codename": "", "id": 142229, "product": "/api/v1/product/115540/", "resource_uri": "/api/v1/productversion/142229/", "version": "v2.2" } ], "resource_uri": "/api/v1/product/115540/" } ] }',
                      status=200,
                      content_type="application/json")
        responses.add(responses.GET, self.base_url + "/api/v1/" + "suite/",# + "?format=json&name=Test+Suite&product__name=Firefox+OS",
                      body='{ "meta": { "limit": 20, "next": null, "offset": 0, "previous": null, "total_count": 0 }, "objects": []}',
                      status=200,
                      content_type="application/json")
        responses.add(responses.POST, self.base_url + "/api/v1/" + "suite/",
                      body='{ "description": "This is an awesome suite", "id": 888, "name": "Test Suite", "product": "/api/v1/product/115540/", "resource_uri": "/api/v1/suite/888/", "status": "active" }',
                      status=201, content_type="application/json")
        suite = [
            'Test Suite',
            'Firefox OS',
            'v2.2',
            'active',
            'This is an awesome suite'
        ]
        test_suite_obj= mtapi.MozTrapTestSuite(*suite)
        self.assertFalse(test_suite_obj.existing_in_moztrap())

        fields = [
            'name',
            'product_name',
            'product_uri',
            'product_version',
            'product_version_uri',
            'description',
            'status',
            #'suite_id',
            #'suite_uri',
            'suite_objs',
        ]
        for field in fields:
            self.assertNotEqual(getattr(test_suite_obj, field), None, field + " should not be None")

        test_suite_obj.create()

        fields = [
            'name',
            'product_name',
            'product_uri',
            'product_version',
            'product_version_uri',
            'description',
            'status',
            'suite_id',
            'suite_uri',
            'suite_objs',
        ]
        for field in fields:
            self.assertNotEqual(getattr(test_suite_obj, field), None, field + " should not be None")

        self.assertEqual(test_suite_obj.suite_uri, "/api/v1/suite/888/")
        #if test_case_obj.existing_in_moztrap():
        #    test_case_obj.update(new_case_version_info={"name": case['id'], "status": case['state'], "tags":[]}, suites=[suite['name']])
        #else:

        expecteds = [
            ("GET" , "product"),
            ("GET", "suite"),
            ("POST", "suite"),
        ]
        self._verify_call_order(expecteds, responses.calls)
        self.assertEqual(test_suite_obj.suite_uri, "/api/v1/suite/888/")

    @responses.activate
    def test_suite_init_exist_noupdate(self):
        responses.add(responses.GET, self.base_url + "/api/v1/" + "product/",# + "?name=Firefox+OS&format=json",
                      body='{ "meta": { "limit": 20, "next": null, "offset": 0, "previous": null, "total_count": 1 }, "objects": [ \
                      { "description": "", "id": 115540, "name": "Firefox OS", "productversions": [ { "codename": "", "id": 142229, "product": "/api/v1/product/115540/", "resource_uri": "/api/v1/productversion/142229/", "version": "v2.2" } ], "resource_uri": "/api/v1/product/115540/" } ] }',
                      status=200,
                      content_type="application/json")
        responses.add(responses.GET, self.base_url + "/api/v1/" + "suite/",# + "?format=json&name=Test+Suite&product__name=Firefox+OS",
                      body='{ "meta": { "limit": 20, "next": null, "offset": 0, "previous": null, "total_count": 1 }, "objects": [{\
                              "created_by": null,\
                              "description": "This is an awesome suite",\
                              "id": 888,\
                              "modified_by": null,\
                              "modified_on": "2012-03-01T19:38:14",\
                              "name": "Test Suite",\
                              "product": "/api/v1/product/115540/",\
                              "resource_uri": "/api/v1/suite/888/",\
                              "status": "active"\
                      }]}',
                      status=200,
                      content_type="application/json")
        responses.add(responses.POST, self.base_url + "/api/v1/" + "suite/",
                      body='{ "description": "This is an awesome suite", "id": 888, "name": "Test Suite", "product": "/api/v1/product/115540/", "resource_uri": "/api/v1/suite/888/", "status": "active" }',
                      status=201, content_type="application/json")
        suite = [
            'Test Suite',
            'Firefox OS',
            'v2.2',
            'active',
            'This is an awesome suite'
        ]
        test_suite_obj= mtapi.MozTrapTestSuite(*suite)
        self.assertTrue(test_suite_obj.existing_in_moztrap())

        fields = [
            'name',
            'product_name',
            'product_uri',
            'product_version',
            'product_version_uri',
            'description',
            'status',
            'suite_id',
            'suite_uri',
            'suite_objs',
        ]
        for field in fields:
            self.assertNotEqual(getattr(test_suite_obj, field), None, field + " should not be None")

        self.assertFalse(test_suite_obj.should_update())
        #test_suite_obj.update()

        fields = [
            'name',
            'product_name',
            'product_uri',
            'product_version',
            'product_version_uri',
            'description',
            'status',
            'suite_id',
            'suite_uri',
            'suite_objs',
        ]
        for field in fields:
            self.assertNotEqual(getattr(test_suite_obj, field), None, field + " should not be None")

        self.assertEqual(test_suite_obj.suite_uri, "/api/v1/suite/888/")
        #if test_case_obj.existing_in_moztrap():
        #    test_case_obj.update(new_case_version_info={"name": case['id'], "status": case['state'], "tags":[]}, suites=[suite['name']])
        #else:

        expecteds = [
            ("GET" , "product"),
            ("GET", "suite"),
        ]
        self._verify_call_order(expecteds, responses.calls)
        self.assertEqual(test_suite_obj.suite_uri, "/api/v1/suite/888/")

    @responses.activate
    def test_suite_init_exist_update(self):
        responses.add(responses.GET, self.base_url + "/api/v1/" + "product/",# + "?name=Firefox+OS&format=json",
                      body='{ "meta": { "limit": 20, "next": null, "offset": 0, "previous": null, "total_count": 1 }, "objects": [ \
                      { "description": "", "id": 115540, "name": "Firefox OS", "productversions": [ { "codename": "", "id": 142229, "product": "/api/v1/product/115540/", "resource_uri": "/api/v1/productversion/142229/", "version": "v2.2" } ], "resource_uri": "/api/v1/product/115540/" } ] }',
                      status=200,
                      content_type="application/json")
        responses.add(responses.GET, self.base_url + "/api/v1/" + "suite/",# + "?format=json&name=Test+Suite&product__name=Firefox+OS",
                      body='{ "meta": { "limit": 20, "next": null, "offset": 0, "previous": null, "total_count": 1 }, "objects": [{\
                              "created_by": null,\
                              "description": "This is an awesome suite",\
                              "id": 888,\
                              "modified_by": null,\
                              "modified_on": "2012-03-01T19:38:14",\
                              "name": "Test Suite",\
                              "product": "/api/v1/product/115540/",\
                              "resource_uri": "/api/v1/suite/888/",\
                              "status": "active"\
                      }]}',
                      status=200,
                      content_type="application/json")
        responses.add(responses.PUT, self.base_url + "/api/v1/" + "suite/888",
                      body='{ "description": "This is an awesome suite", "id": 888, "name": "Test Suite", "product": "/api/v1/product/115540/", "resource_uri": "/api/v1/suite/888/", "status": "active" }',
                      status=201, content_type="application/json")
        suite = [
            'Test Suite',
            'Firefox OS',
            'v2.2',
            'active',
            'This is a MODIFIED awesome suite'
        ]
        test_suite_obj= mtapi.MozTrapTestSuite(*suite)
        self.assertTrue(test_suite_obj.existing_in_moztrap())

        fields = [
            'name',
            'product_name',
            'product_uri',
            'product_version',
            'product_version_uri',
            'description',
            'status',
            'suite_id',
            'suite_uri',
            'suite_objs',
        ]
        for field in fields:
            self.assertNotEqual(getattr(test_suite_obj, field), None, field + " should not be None")

        self.assertTrue(test_suite_obj.should_update())
        test_suite_obj.update()

        fields = [
            'name',
            'product_name',
            'product_uri',
            'product_version',
            'product_version_uri',
            'description',
            'status',
            'suite_id',
            'suite_uri',
            'suite_objs',
        ]
        for field in fields:
            self.assertNotEqual(getattr(test_suite_obj, field), None, field + " should not be None")

        self.assertEqual(test_suite_obj.suite_uri, "/api/v1/suite/888/")
        #if test_case_obj.existing_in_moztrap():
        #    test_case_obj.update(new_case_version_info={"name": case['id'], "status": case['state'], "tags":[]}, suites=[suite['name']])
        #else:

        expecteds = [
            ("GET" , "product"),
            ("GET", "suite"),
            ("PUT", "suite"),
        ]
        self._verify_call_order(expecteds, responses.calls)
        self.assertEqual(test_suite_obj.suite_uri, "/api/v1/suite/888/")


    def _prepare_empty_diff(self):
        return ([
                    {
                        'suite': {
                            'added': [],
                            'removed': []
                        },
                        'case': {
                            'added': [],
                            'modified': [],
                            'removed': []
                        }
                    }
                ])

    def _fill_steps(self, step_str):
        return ([{
            'instruction': step_str,
            'expected': "",
            'number': 0
        }])

    @mock.patch('mtapi.MozTrapTestSuite', autospec=True)
    def test_sync_diff_to_moztrap_add_suite(self, mock_mttestsuite):

        diff_outs = self._prepare_empty_diff()
        diff_outs[0]['suite']['added'] = ["Launch suite"]

        mock_suites = [mock.Mock()]
        mock_mttestsuite.side_effect = mock_suites
        mtapi.sync_diff_to_moztrap(diff_outs, {'username': "foo", 'api_key': "bar"})
        #self.assertTrue(mock_suites[0].create.called, "Create function was not called")
        mock_suites[0].create.assert_called_once()

    # The order of decorator is the opposite of the functon parameters
    @mock.patch('mtapi.MozTrapTestCase', autospec=True)
    @mock.patch('mtapi.MozTrapTestSuite', autospec=True)
    def test_sync_diff_to_moztrap_add_case(self, mock_mttestsuite, mock_mttestcase):

        diff_outs = self._prepare_empty_diff()
        expected_add = {
                            "bug": 2,
                            "id": "fxos.func.sanity.launch_foobar",
                            "instructions": "Launch FOOBAR",
                            "state": "draft",
                            "userStory": 1,
                            "suites": ["Launch suite"]}
        diff_outs[0]['case']['added'] = [expected_add]
        #mock_suites = [mock.Mock()]
        #mock_mttestsuite.side_effect = mock_suites
        mock_cases= [mock.Mock()]
        mock_mttestcase.side_effect = mock_cases
        mtapi.sync_diff_to_moztrap(diff_outs, {'username': "foo", 'api_key': "bar"})
        #self.assertTrue(mock_suites[0].create.called, "Create function was not called")
        mock_mttestcase.assert_called_once_with(name=expected_add['id'],
                                                product_name="Firefox OS",
                                                product_version="v2.2",
                                                status=expected_add['state'],
                                                suites=expected_add['suites'],
                                                steps=self._fill_steps(expected_add['instructions'])
                                                )

        mock_cases[0].create.assert_called_once()

    @mock.patch('mtapi.MozTrapTestCase', autospec=True)
    @mock.patch('mtapi.MozTrapTestSuite', autospec=True)
    def test_sync_diff_to_moztrap_update_case(self, mock_mttestsuite, mock_mttestcase):

        diff_outs = self._prepare_empty_diff()
        expected_modify = {
                            "bug": 2,
                            "id": "fxos.func.sanity.launch_foobar",
                            "instructions": "Launch FOOBAR",
                            "state": "draft",
                            "userStory": 1,
                            "suites": ["Launch suite"]}
        diff_outs[0]['case']['modified'] = [expected_modify]
        #mock_suites = [mock.Mock()]
        #mock_mttestsuite.side_effect = mock_suites
        mock_cases= [mock.Mock()]
        mock_mttestcase.side_effect = mock_cases
        mtapi.sync_diff_to_moztrap(diff_outs, {'username': "foo", 'api_key': "bar"})
        #self.assertTrue(mock_suites[0].create.called, "Create function was not called")
        mock_mttestcase.assert_called_once_with(name=expected_modify['id'],
                                                product_name="Firefox OS",
                                                product_version="v2.2",
                                                status=expected_modify['state'],
                                                suites=expected_modify['suites'],
                                                steps=self._fill_steps(expected_modify['instructions'])
                                                )

        mock_cases[0].update.assert_called_once()


if __name__ == '__main__':
    unittest.main()
