#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = "0.1"

#
# Backlog (http://www.backlog.jp) CLIENT LIBRARY
#
from xmlrpclib import ServerProxy
import types

_URI_FORMAT_ = "https://%(username)s:%(password)s@%(space)s.backlog.jp/XML-RPC"

class Backlog(object):
    
    def __init__(self,space,username,password):
        uri = _URI_FORMAT_ % {"username":username,"password":password,"space":space}
        self.server = ServerProxy(uri)    
    
    def get_projects(self):
        projects = self.server.backlog.getProjects()
        return [Project(**x) for x in projects]
    
    def get_project(self,key):
        project = self.server.backlog.getProject(key)
        return Project(**project)
    
    def get_components(self,project_id):
        components = self.server.backlog.getComponents(project_id)
        return [Component(**x) for x in components]
    
    def get_versions(self,project_id):
        versions = self.server.backlog.getVersions(project_id)
        return [Version(**x) for x in versions]
    
    def get_users(self,project_id):
        users = self.server.backlog.getUsers(project_id)
        return [User(**x) for x in users]

    def get_issue_types(self,project_id):
        issue_types = self.server.backlog.getIssueTypes(project_id)
        return [IssueType(**v) for v in issue_types]    
    
    def get_issue(self,key):
        issue = self.server.backlog.getIssue(key)
        return Issue(**issue)
    
    def get_comments(self,issue_id):
        comments = self.server.backlog.getComments(issue_id)
        return [Comment(**x) for x in comments]
    
    def count_issue(self,condition):
        if not isinstance(condition, FindCondition) :
            condition = FindCondition(condition)
        return self.server.backlog.countIssue(condition)
    
    def find_issue(self,condition):
        if not isinstance(condition, FindCondition) :
            condition = FindCondition(condition)
        issues = self.server.backlog.findIssue(condition)
        return [Issue(**x) for x in issues]
    
    def create_issue(self,issue):
        if not isinstance(issue, Issue) :
            issue = Issue(**issue)
        ret = self.server.backlog.createIssue(issue)
        return Issue(**ret)
    
    def update_issue(self,issue):
        if not isinstance(issue, Issue) :
            issue = Issue(**issue)
        ret = self.server.backlog.updateIssue(issue)
        return Issue(**ret)
    
    def switch_status(self,status):
        if not isinstance(status,UpdateStatus) :
            status = UpdateStatus(**status)
        ret = self.server.backlog.switchStatus(status)
        return Issue(**ret)

class BacklogObject(object):
    
    _REPR_FORMAT_ = "[%(id)s] %(name)s"
    
    def __init__(self,id,name):
        self.id = id
        self.name = name
    
    def __repr__(self):        
        return self.__class__._REPR_FORMAT_ % self.__dict__
    
    __str__ = __repr__

Component = type("Component",(BacklogObject,),{})
User = type("User",(BacklogObject,),{})
Priority = type("Priority",(BacklogObject,),{"HIGH":2,"MIDDLE":3,"LOW":4})
Resolution = type("Resolution",(BacklogObject,),{"UNSET":-1,"DONE":0,"IGNORE":1,"INVALID":2,"DUPLICATE":3,"WORKWELL":4})
Status = type("Status",(BacklogObject,),{"UNDONE":1,"PROGRESS":2,"COMPLETED":3,"DONE":4})

class Project(BacklogObject):
    
    _REPR_FORMAT_ = "[%(id)s][%(key)s] %(url)s"
    
    def __init__(self,id,key,name,url):
        self.id = id
        self.key = key
        self.name = name
        self.url = url
                    
class Version(BacklogObject):
    
    _REPR_FORMAT_ = "[%(id)s] %(name)s %(date)s"    
    
    def __init__(self,id,name,date):
        self.id = id
        self.name = name
        self.date = date
        
Milestone = type("Milestone",(Version,),{})

class IssueType(BacklogObject):
    
    _REPR_FORMAT_ = "[%(id)s] %(name)s %(color)s"    
    
    def __init__(self,id,name,color=None):
        """
        color は get_issue_types と get_issue/find_issue で
        前者の場合は設定され、後者の場合は設定されない。    
        """
        self.id = id
        self.name = name
        self.color = color
                
class Issue(BacklogObject):
    
    _REPR_FORMAT_ = "[%(id)s][%(key)s] %(summary)s"
    
    _CONVERTERS_ = {"assigner":User,
                    "created_user":User,
                    "priority":Priority,
                    "version":Version,
                    "versions":Version,
                    "milestone":Milestone,
                    "milestones":Milestone,
                    "component":Component,
                    "components":Component,
                    "issueType":IssueType,
                    "status":Status,
                    "resolution":Resolution}
    
    def __init__(self,**kwargs):
        for k,v in kwargs.iteritems():            
            val = v
            if Issue._CONVERTERS_.has_key(k) :
                converter =Issue._CONVERTERS_[k]
                if type(v) == types.ListType :
                    val = map(lambda x : converter(**x), v)
                else :
                    val = converter(**v)
            self.__dict__[k] = val

class Comment(BacklogObject):
    
    _REPR_FORMAT_ = "[%(id)s] %(content)s"
    
    def __init__(self,id,content,created_user,created_on,updated_on):
        self.id = id
        self.content = content
        self.created_user = User(**created_user)
        self.created_on = created_on
        self.udpated_on = updated_on
        
class UpdateStatus(BacklogObject):
    
    _REPR_FORMAT_ = "[%(key)s] %(statusId)s"
    
    def __init__(self,key,statusId,assignerId,resolutionId,comment):
        self.key = key
        self.statusId = statusId
        self.assignerId = assignerId
        self.resolutionId = resolutionId
        self.comment = comment

class FindCondition():
    
    COND_KEYS = [
                 "projectId",
                 "issueTypeId",
                 "issueType",
                 "componentId",
                 "versionId",
                 "milestoneId",
                 "statusId",
                 "priorityId",
                 "assignerId",
                 "createdUserId",
                 "resolutionId",
                 "created_on_min",
                 "created_on_max",
                 "updated_on_min",
                 "updated_on_max",
                 "start_date_min",
                 "start_date_max",
                 "due_date_min",
                 "due_date_max",
                 "query",
                 "sort",
                 "order",
                 "offset",
                 "limit"
                 ]
    
    def __init__(self,params):
        for k,v in params.iteritems():
            if k in self.COND_KEYS :
                self.__dict__[k] = v
                
    def __repr__(self):
        return ":".join([k+"="+repr(v) for k,v in self.__dict__.iteritems()])
    
    __str__ = __repr__