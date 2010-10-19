#!/usr/bin/env python
# -*- coding: utf-8 -*-
import backloglibtest

import unittest
import backloglib

from test import test_support

_AVAILABLE_PROJECT_ID_ = 12016

class BacklogTest(backloglibtest.BacklogTestCase):
        
    def test_get_projects1(self):
        projects = self.backlog.get_projects()
        # ZAKU
        self.assertEquals(1,len(projects))
            
    def test_get_project1(self):
        project = self.backlog.get_project("ZAKU")
        print project
        
    def test_get_project2(self):
        project = self.backlog.get_project(_AVAILABLE_PROJECT_ID_)
        print project    
    
    def test_get_components1(self):
        components = self.backlog.get_components(_AVAILABLE_PROJECT_ID_)
        for c in components :
            print c
    
    def test_get_versions1(self):
        versions = self.backlog.get_versions(_AVAILABLE_PROJECT_ID_)        
        for v in versions :
            print v
    
    def test_get_users1(self):
        users = self.backlog.get_users(_AVAILABLE_PROJECT_ID_)
        # tksmd yuhei07 api
        self.assertEquals(3,len(users))
        
    def test_get_issue_types1(self):
        issue_types = self.backlog.get_issue_types(_AVAILABLE_PROJECT_ID_)
        self.assertEquals(4,len(issue_types))
            
    def test_get_issue1(self):
        issue = self.backlog.get_issue("ZAKU-1")
        print issue
        
    def test_get_issue2(self):
        issue = self.backlog.get_issue(472153)
        print issue        
    
    def test_get_comments1(self):
        comments = self.backlog.get_comments(472153)
        print comments        
        
    def test_count_issue1(self):
        count = self.backlog.count_issue({"projectId":_AVAILABLE_PROJECT_ID_})
        self.assertNotEquals(0,count)

    def test_find_issue1(self):
        issues = self.backlog.find_issue({"projectId":_AVAILABLE_PROJECT_ID_})
        for i in issues:
            print i
            
    def test_manage_issue_type1(self):
        """
        @since: 0.2.1
        """
        actual = self.backlog.add_issue_type({"project_id":_AVAILABLE_PROJECT_ID_,"name":u"テスト","color":"#007e9a"})
        self.assertEquals(u"テスト",actual.name)
        actual.name = u"mod"
        actual = self.backlog.update_issue_type(actual)
        self.assertEquals(u"mod",actual.name)        
        actual = self.backlog.delete_issue_type(actual.id)
    
    def test_manage_version1(self):
        """
        @since: 0.2.1
        """        
        actual = self.backlog.add_version({"project_id":_AVAILABLE_PROJECT_ID_,"name":u"テスト"})  
        self.assertEquals(u"テスト",actual.name)
        actual.name = u"mod"
        actual = self.backlog.update_version(actual)
        self.assertEquals(u"mod",actual.name)
        self.backlog.delete_version(actual.id)
        
    def test_manage_component1(self):
        """
        @since: 0.2.1
        """
        actual = self.backlog.add_component({"project_id":_AVAILABLE_PROJECT_ID_,"name":u"テスト"})        
        self.assertEquals(u"テスト",actual.name)
        print actual
        actual.name = u"mod"
        actual = self.backlog.update_component(actual)                         
        self.assertEquals(u"mod",actual.name)
        self.backlog.delete_component(actual.id)

class FindConditionTest(unittest.TestCase):
    
    def test_init_1(self):
        condition = backloglib.FindCondition({"projectId":1,"componentId":1})
        self.assertEquals("projectId=1:componentId=1",repr(condition))

def test_main():
    test_support.run_unittest(BacklogTest,
                              FindConditionTest)
        
if __name__ == '__main__' :
    test_main()        