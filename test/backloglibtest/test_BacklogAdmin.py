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

from backloglibtest import BacklogAdminTestCase, test_Backlog

from test import test_support
from backloglib import BacklogAdmin

import md5

class BacklogAdminTest(BacklogAdminTestCase):
    
    def test_get_users(self):
        actual = self.backlog.get_users()
        self.assertEquals(3,len(actual))
        
    def test_manage_user1(self):
        passwd = md5.new()
        passwd.update("password")
        actual = self.backlog.add_user({"user_id":u"uid",
                                        "password_md5":passwd.hexdigest(),
                                        "name":"name",
                                        "mail_address":u"someda@isenshi.com",
                                        "role":BacklogAdmin.ROLE_NORMAL_USER})        
        print actual
        actual.name = u"mod"
        actual.mail_setting = {"mail":True,"comment":False}
        actual = self.backlog.update_user(actual)
        self.assertEqual("mod",actual.name)
        self.backlog.delete_user(actual.id)
        
    def test_get_projects1(self):
        actual = self.backlog.get_projects()
        self.assertEquals(1,len(actual))
        
    def test_get_project_users1(self):
        actual = self.backlog.get_project_users(test_Backlog._AVAILABLE_PROJECT_ID_)
        self.assertEquals(3,len(actual))

def test_main():
    test_support.run_unittest(BacklogAdminTest)
        
if __name__ == '__main__' :
    test_main()