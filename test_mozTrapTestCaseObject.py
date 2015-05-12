#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'shako'
import unittest
import mtapi #SUT
import orm
import config

mz_user_name = "root"
mz_user_api_key = "10dc62fc-39a2-4e67-be5f-b4403163dc07"

#mz_user_name = "admin-django"
#mz_user_api_key = "c67c9af7-7e07-4820-b686-5f92ae94f6c9"

class TestMTApi(unittest.TestCase):
    def setUp(self):
        self.test_tmp_file = "tmp.txt"
        mtapi.mtorigin = "http://127.0.0.1:8000"
        mtapi.set_user_params(mz_user_name, mz_user_api_key)
        self.test_case_sample = """
        TEST THAT fxos.rocketbar.search-provider.0

        WHEN  I search "star trek" using Yahoo
        THEN  The search page of Yahoo that searches "star trek" is shown correctly

        =====

        TEST THAT fxos.rocketbar.search-provider.1

        WHEN  I search "star wars" using Google
        THEN  The search page of Google that searches "star wars" is shown correctly

        =====

        TEST THAT fxos.rocketbar.search-provider.2

        WHEN  I search "Dr. Who" using DuckDuckGo
        THEN  The search page of DuckDuckGo that searches "Dr. Who" is shown correctly

        =====

        TEST THAT fxos.rocketbar.launch

        WHEN  Tap the rocketbar
        THEN  The rocket bar search window opens

        =====

        """
        self.test_case_sample_2 = {"description": "Able to search test runs",
                                   "name": "Able to search test runs",
                                   "steps": [
                                       {"expected": "then Test run results display matching search results",
                                        "instruction": "when Log in> Manage> Runs> Enter data in search field> click 'update the list'",
                                        "number": 1},
                                       {"expected": "then Test run results display matching search results",
                                        "instruction": "when Enter search criteria for: status, product, testcycle, name, tester, environment, creator> click 'update the list'",
                                        "number": 2}
                                   ]}
        self.test_case_sample_3 = {"description": "Test description",
                                   "name": "Test name",
                                   "steps": [
                                       {"expected": "expected 1",
                                        "instruction": "instruction 1",
                                        "number": 1},
                                       {"expected": "expected 2",
                                        "instruction": "instruction 2",
                                        "number": 2}
                                   ]}

    #@unittest.skip("Pass!")
    def test_mtapi_create(self):
        sample_json = orm.parseSuite(self.test_case_sample)
        for case in sample_json['objects']:
            print case['name']
            print case['steps']
            print case['description']
            # test_case_obj = mtapi.MozTrapTestCase(case['name'], "testProduct", "1.0")
            test_case_obj = mtapi.MozTrapTestCase(case['name'], "MozTrap", "0.8")
            for step in case['steps']:
                print step
                test_case_obj.add_step(step['instruction'], step['expected'])
            # tag is not working when calling moztrap's REST API!!!
            test_case_obj.add_tag("testTag", "testDesc")
            test_case_obj.create()

    def test_tmp_file_create(self):
        mtapi.convert_mark_file_into_moztrap("tmp.txt", {'username': mz_user_name, 'api_key': mz_user_api_key})

    def test_forcePushCaseversion(self):
        # add test data for forcePushCaseversion
        test_case_obj = mtapi.MozTrapTestCase(self.test_case_sample_2['name'],
                                              config.defaultProduct, config.defaultVersion)
        for step in self.test_case_sample_2['steps']:
            test_case_obj.add_step(step['instruction'], step['expected'])
        resp = test_case_obj.create()

        # get the response obj from creating the case obj and pass to forcePushCaseVersion
        # test the forcePushCaseversion can update data correctly with id
        mtapi.forcePushCaseversion(self.test_case_sample_3, {'username': mz_user_name, 'api_key': mz_user_api_key},
                                   case_version_id=resp['id'])

        # test the forcePushCaseversion can update data correctly with case name
        self.test_case_sample_3['description'] = "Test update desc"
        self.test_case_sample_3['steps'] = [{"expected": "Oh ya mom I'm on TV~~~", "instruction": "test another condition for forcepush", "number": 1}]
        mtapi.forcePushCaseversion(self.test_case_sample_3, {'username': mz_user_name, 'api_key': mz_user_api_key})



if __name__ == '__main__':
    unittest.main()

