#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'shako'
import unittest
import mtapi #SUT

mz_user_name = "root"
mz_user_api_key = "10dc62fc-39a2-4e67-be5f-b4403163dc07"


class TestMTApi(unittest.TestCase):
    def setUp(self):
        mtapi.mtorigin = "http://127.0.0.1:8000"
        mtapi.set_user_params(mz_user_name, mz_user_api_key)

    def test_create(self):
        test_case_obj = mtapi.MozTrapTestCase("test2", "testProduct", "1.0")
        test_case_obj.add_step("test instruction 1", "test expected 1")
        test_case_obj.add_step("test instruction 2", "test expected 2")
        test_case_obj.add_tag("testTag", "testDesc")
        test_case_obj.create()



if __name__ == '__main__':
    unittest.main()

