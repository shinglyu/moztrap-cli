#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'shako'
import unittest
import mtapi #SUT
import orm

# mz_user_name = "root"
# mz_user_api_key = "10dc62fc-39a2-4e67-be5f-b4403163dc07"

mz_user_name = "admin-django"
mz_user_api_key = "c67c9af7-7e07-4820-b686-5f92ae94f6c9"

class TestMTApi(unittest.TestCase):
    def setUp(self):
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

    def test_create(self):

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

if __name__ == '__main__':
    unittest.main()

