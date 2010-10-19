# -*- coding: utf-8 -*-

import unittest

import backloglib

class BacklogTestCase(unittest.TestCase):
    
    def setUp(self):
        self.backlog = backloglib.Backlog("space","user","password")         
        