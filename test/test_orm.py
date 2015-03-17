#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append("../")

import unittest
import json

import orm #MUT


class TestOrm(unittest.TestCase):
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
        caseversion_out = json.loads(self.json_out)
        self.assertEqual(type(orm.parseCaseversion(self.txt)), type(caseversion_out))
        self.assertEqual(orm.parseCaseversion(self.txt)['name'], caseversion_out['name'])
        self.assertEqual(orm.parseCaseversion(self.txt)['description'], caseversion_out['description'])
        self.assertEqual(orm.parseCaseversion(self.txt), caseversion_out)

if __name__ == '__main__':
    unittest.main()
