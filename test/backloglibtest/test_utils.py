#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2009 - 2010 Takashi SOMEDA
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

from test import test_support

from backloglib import utils
from backloglib.model import Status

import unittest

class UtilsTest(unittest.TestCase):
    
    def test_classwrap1(self):
        actual = utils.classwrap(None, Status)
        self.assertTrue(not actual)
        
    def test_classwrap2(self):
        actual = utils.classwrap({"id":1,"name":"hoge"}, Status)
        self.assertTrue(isinstance(actual,Status))
                
    def test_classwrap3(self):
        status = Status(1,"hoge")
        actual = utils.classwrap(status, Status)
        self.assertTrue(isinstance(actual,Status))                

def test_main():
    test_support.run_unittest(UtilsTest)
        
if __name__ == '__main__' :
    test_main()