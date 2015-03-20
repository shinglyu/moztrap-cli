#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append("../")

import unittest
import json

import orm #MUT


class TestOrmCaseversion(unittest.TestCase):
    def setUp(self):
        with open('caseversion_88.in.json', 'r') as f:
            self.json_in = ''.join(f.readlines())
        with open('caseversion_88.txt', 'r') as f:
            self.txt = ''.join(f.readlines())
        with open('caseversion_88.out.json', 'r') as f:
            self.json_out = ''.join(f.readlines())

    def test_formatCaseversion(self):
        caseversion_in = json.loads(self.json_in)
        self.assertEqual(orm.formatCaseversion(caseversion_in), self.txt)

    def test_parseCaseversion(self):
        in_txt = self.txt.split('\n',1)[1] # Remove first line
        caseversion_out = json.loads(self.json_out)
        self.assertEqual(type(orm.parseCaseversion(in_txt)), type(caseversion_out))
        self.assertEqual(orm.parseCaseversion(in_txt)['name'], caseversion_out['name'])
        self.assertEqual(orm.parseCaseversion(in_txt)['description'], caseversion_out['description'])
        self.assertEqual(orm.parseCaseversion(in_txt), caseversion_out)

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
