# -*- coding: utf-8 -*-

__author__ = 'contee'

"""
test_force
~~~~~~~~~~~~~~

file commment here.

"""

import unittest

import os
import sys
import codecs
sys.path.append('..')

from sengokustat.spiders import force

class test_force(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_XXX_Test_Name(self):

        with codecs.open("../log/20140101/ranking_force.html", "r", "shift_jis" ) as f:
            parser = force.ForceRankParser()
            parser.parse(body=f.read())

        # raise NotImplementedError('Insert test code here.')
        #  Examples:
        # self.assertEqual(fp.readline(), 'This is a test')
        # self.assertFalse(os.path.exists('a'))
        # self.assertTrue(os.path.exists('a'))
        # self.assertTrue('already a backup server' in c.stderr)
        # self.assertIn('fun', 'disfunctional')
        # self.assertNotIn('crazy', 'disfunctional')
        # with self.assertRaises(Exception):
        #	raise Exception('test')
        #
        # Unconditionally fail, for example in a try block that should raise
        # self.fail('Exception was not raised')

    @unittest.skipIf('SKIP_SLOW_TESTS' in os.environ, 'Requested fast tests')
    def test_XXX_Slow_Test_Name(self):
        pass
        # raise NotImplementedError('Insert test code here.')

if __name__ == '__main__':
    unittest.main()