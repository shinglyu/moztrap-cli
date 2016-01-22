#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append("../")

import unittest
import json
import difflib

import orm #MUT


class TestOrmCaseversion(unittest.TestCase):
    def setUp(self):
        with open('caseversion_88.in.json', 'r') as f:
            self.json_in = ''.join(f.readlines())
        #with open('caseversion_88.txt', 'r') as f:
        #    self.txt = ''.join(f.readlines())
        with open('caseversion_88.formatted.json', 'r') as f:
            self.txt = ''.join(f.readlines())
        with open('caseversion_88.out.json', 'r') as f:
            self.json_out = ''.join(f.readlines())

    def test_formatCaseversion(self):
        caseversion_in = json.loads(self.json_in)
        caseversion_formatted = json.loads(self.txt)
        print ''.join(difflib.unified_diff(orm.formatCaseversion(caseversion_in)[4], caseversion_formatted[4]))
        #print ''.join(difflib.ndiff(orm.formatCaseversion(caseversion_in)[4], caseversion_formatted[4]))
        self.assertEqual(orm.formatCaseversion(caseversion_in), caseversion_formatted)

    def test_parseCaseversion(self):
        #in_txt = self.txt.split('\n',1)[1] # Remove first line
        in_txt = json.loads(self.txt)
        caseversion_out = json.loads(self.json_out)
        self.assertEqual(type(orm.parseCaseversion(in_txt)), type(caseversion_out))
        #self.assertEqual(orm.parseCaseversion(in_txt)['resource_uri'], caseversion_out['resource_uri'])
        self.assertEqual(orm.parseCaseversion(in_txt)['name'], caseversion_out['name'])
        self.assertEqual(orm.parseCaseversion(in_txt)['description'], caseversion_out['description'])
        self.assertEqual(orm.parseCaseversion(in_txt), caseversion_out)

    def test_parseCaseStep(self):
        #in_txt = self.txt.split('\n',1)[1] # Remove first line
        in_txt = json.loads(self.txt)
        caseversion_out = json.loads(self.json_out)
        self.assertEqual(orm.parseCaseStep(in_txt[4]), caseversion_out['steps'])
        #self.assertEqual(orm.parseCaseversion(in_txt)['resource_uri'], caseversion_out['resource_uri'])

    def test_parseCaseStep_no_expected(self):
        #in_txt = self.txt.split('\n',1)[1] # Remove first line
        in_txt = "1. Hello\n 2. World"
        out_json = [{'instruction': 'Hello', 'expected':'', 'number':1},
                    {'instruction': 'World', 'expected':'', 'number':2}]
        self.assertEqual(orm.parseCaseStep(in_txt), out_json)
        #self.assertEqual(orm.parseCaseversion(in_txt)['resource_uri'], caseversion_out['resource_uri'])

class TestOrmSuite(unittest.TestCase):
    def setUp(self):
        self.sid = 6 #FIXME: magic number
        with open('suite_6.in.json', 'r') as f:
            self.json_in = ''.join(f.readlines())
        with open('suite_6.txt', 'r') as f:
            self.txt = ''.join(f.readlines())
        with open('suite_6.out.json', 'r') as f:
            self.json_out = ''.join(f.readlines())

    def test_formatSuite(self):
        suite_in = json.loads(self.json_in)
        self.assertEqual(orm.formatSuite(suite_in, self.sid), self.txt)

    def test_parseSuite(self):
        in_txt = self.txt.split('\n',1)[1] # Remove first line
        suite_out = json.loads(self.json_out)
        self.assertEqual(type(orm.parseSuite(in_txt)), type(suite_out))
        self.assertEqual(orm.parseSuite(in_txt)['objects'], suite_out['objects'])
        #self.assertEqual(orm.parseSuite(self.txt)['description'], suite_out['description'])
        self.assertEqual(orm.parseSuite(in_txt), suite_out)
if __name__ == '__main__':
    unittest.main()
