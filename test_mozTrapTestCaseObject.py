#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'shako'
import unittest
import mtapi #SUT
import orm

mz_user_name = "root"
mz_user_api_key = "10dc62fc-39a2-4e67-be5f-b4403163dc07"


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
            print case['steps']
            print case['description']
            test_case_obj = mtapi.MozTrapTestCase(case['name'], "testProduct", "1.0")
            for step in case['steps']:
                test_case_obj.add_step(step['instruction'], step['expected'])
            # tag is not working when calling moztrap's REST API!!!
            test_case_obj.add_tag("testTag", "testDesc")
            test_case_obj.create()

if __name__ == '__main__':
    unittest.main()

