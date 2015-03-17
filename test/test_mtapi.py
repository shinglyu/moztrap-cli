#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append("../")

import unittest
import mock
import json

import urllib2
import requests

import mtapi #SUT


class TestMTApi(unittest.TestCase):
    def setUp(self):
        with open('caseversion_88.out.json', 'r') as f:
            # self.json_out = ''.join(f.readlines())
            # self.json_out = ''.join(f.readlines())
            self.json_out = json.loads(''.join(f.readlines()))
            #self.json_out = json.dumps(json.load(f))

    def test_forcePushCaseversion(self):
        #BODY = "***filecontents***"
        #conn = Mock(httplib.HTTPConnection("localhost", 8080))
        #conn.request("PUT", "/file", BODY)
        #response = conn.getresponse()
        #print response.status, response.reason
        mock_conn = mock.Mock(spec=requests)
        mtapi.forcePushCaseversion(self.json_out, mock_conn)
        # mock_conn.assert_called_with(mtapi.mtorigin)
        mock_conn.put.assert_called_with(mtapi.mtorigin, data=json.dumps(self.json_out))
        # mock_conn.open.assert_called_with('foo')

if __name__ == '__main__':
    unittest.main()
