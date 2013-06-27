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

"""
このモジュールのクラスは変更の可能性があります。

各メソッドでこのモデルモジュールのクラスを利用するのは、XML-RPC の呼び出し前に
手軽に型チェックを行うためです
"""
import types

from utils import classwrap

class Serializable(object):
    """
    XML-RPC 用に marshall するためのメソッドを持つクラス
    """    
    def serialize(self):
        return self._do_convert(vars(self))
        
    def _do_convert(self, obj):
        if isinstance(obj, types.DictType) :
            return dict([(k, self._do_convert(v)) for k, v in obj.iteritems() if v])
        elif isinstance(obj, types.ListType) or isinstance(obj, types.TupleType) : 
            return [self._do_convert(v) for v in obj]
        elif hasattr(obj, "__dict__"):
            return self._do_convert(vars(obj))
        else :
            return obj
        
class BacklogObject(Serializable):
    
    _REPR_FORMAT_ = "[%(id)s] %(name)s"
    
    def __init__(self, id, name):
        self.id = id
        self.name = name
    
    def __repr__(self):        
        return (self.__class__._REPR_FORMAT_ % vars(self)).encode('utf-8')

    __str__ = __repr__

Component = type("Component", (BacklogObject,), {})

class AddComponent(BacklogObject):
    
    _REPR_FORMAT_ = "[%(project_id)s] %(name)s"    
    
    def __init__(self, project_id, name):
        self.project_id = project_id
        self.name = name

User = type("User", (BacklogObject,), {})
Priority = type("Priority", (BacklogObject,), {"HIGH":2, "MIDDLE":3, "LOW":4})
Resolution = type("Resolution", (BacklogObject,), {"UNSET":-1, "DONE":0, "IGNORE":1, "INVALID":2, "DUPLICATE":3, "WORKWELL":4})
Status = type("Status", (BacklogObject,), {"UNDONE":1, "PROGRESS":2, "COMPLETED":3, "DONE":4})

class Project(BacklogObject):
    
    _REPR_FORMAT_ = "[%(id)s][%(key)s] %(url)s"
    
    def __init__(self, id, key, name, url, archived, text_formatting_rule=None,use_parent_child_issue=False):
        self.id = id
        self.key = key
        self.name = name
        self.url = url
        self.archived = archived
        self.text_formatting_rule = text_formatting_rule
        self.use_parent_child_issue = use_parent_child_issue
                    
class Version(BacklogObject):
    
    _REPR_FORMAT_ = "[%(id)s] %(name)s %(date)s"    
    
    def __init__(self, id, name, date):
        self.id = id
        self.name = name
        self.date = date
        
Milestone = type("Milestone", (Version,), {})

class AddVersion(BacklogObject):
    
    _REPR_FORMAT_ = "[%(project_id)s] %(name)s %(start_date)s %(due_date)s"    
    
    def __init__(self, project_id, name, start_date=None, due_date=None):
        self.project_id = project_id
        self.name = name
        self.start_date = start_date
        self.due_date = due_date

class UpdateVersion(BacklogObject):
    
    _REPR_FORMAT_ = "[%(id)s] %(name)s %(start_date)s %(due_date)s %(archived)s"    
    
    def __init__(self, id, name, start_date=None, due_date=None, archived=False):
        self.id = id
        self.name = name
        self.start_date = start_date
        self.due_date = due_date
        self.archived = archived

class IssueType(BacklogObject):
    
    _REPR_FORMAT_ = "[%(id)s] %(name)s %(color)s"    
    
    def __init__(self, id, name, color=None):
        """
        color は get_issue_types と get_issue/find_issue で
        前者の場合は設定され、後者の場合は設定されない。    
        """
        self.id = id
        self.name = name
        self.color = color

class AddIssueType(BacklogObject):

    _REPR_FORMAT_ = "[%(project_id)s] %(name)s %(color)s"    
    
    def __init__(self, project_id, name, color):
        self.project_id = project_id
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
    
    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():            
            val = v
            if Issue._CONVERTERS_.has_key(k) :
                converter = Issue._CONVERTERS_[k]
                if isinstance(v, types.ListType) or isinstance(v, types.TupleType) :
                    val = [converter(**x) for x in v]
                else :
                    val = converter(**v)
            self.__dict__[k] = val

class Comment(BacklogObject):
    
    _REPR_FORMAT_ = "[%(id)s] %(content)s"
    
    def __init__(self, id, content, created_user, created_on, updated_on):
        self.id = id
        self.content = content
        self.created_user = User(**created_user)
        self.created_on = created_on
        self.udpated_on = updated_on
        
class UpdateStatus(BacklogObject):
    
    _REPR_FORMAT_ = "[%(key)s] %(statusId)s"
    
    def __init__(self, key, statusId, assignerId, resolutionId, comment):
        self.key = key
        self.statusId = statusId
        self.assignerId = assignerId
        self.resolutionId = resolutionId
        self.comment = comment

class FindCondition(Serializable):
    
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
    
    def __init__(self, params):
        for k, v in params.iteritems():
            if k in self.COND_KEYS :
                self.__dict__[k] = v
                
    def __repr__(self):
        return ":".join([k + "=" + repr(v) for k, v in vars(self).iteritems()])
    
    __str__ = __repr__

ActivityType = type("ActivityType", (BacklogObject,), {"CREATE_ISSUE":1, "UPDATE_ISSUE":2, "CREATE_COMMENT":3})

class DetailUser(User):
    
    _REPR_FORMAT_ = "[%(id)s] %(name)s %(lang)s"
        
    def __init__(self,id,name,lang,updated_on):
        super(DetailUser,self).__init__(id,name)
        self.lang = lang
        self.updated_on = updated_on

class UserIcon(BacklogObject):
      
    _REPR_FORMAT_ = "[%(id)s] %(content_type)s"
            
    def __init__(self,id,content_type,data,updated_on):
        self.id = id
        self.content_type = content_type
        self.data = data
        self.updated_on = updated_on

class TimelineIssue(BacklogObject):
    
    _REPR_FORMAT_ = "[%(id)s][%(key)s] %(summary)s"
        
    def __init__(self,id,key,summary,description,priority):
        self.id = id
        self.key = key
        self.summary = summary
        self.description = description
        self.priority = classwrap(priority,Priority)

class Timeline(BacklogObject):
    
    _REPR_FORMAT_ = "[%(updated_on)s] %(content)s %(user)s"    
    
    def __init__(self,type,content,updated_on,user,issue):
        self.type = classwrap(type, ActivityType)
        self.content = content
        self.updated_on = updated_on
        self.user = classwrap(user,User)
        self.issue = classwrap(issue, TimelineIssue)

class StatusSummary(Status):
    
    _REPR_FORMAT_ = "[%(id)s] %(name)s %(count)s"    
    
    def __init__(self,id,name,count):
        super(StatusSummary,self).__init__(id,name)
        self.count = count

class MilestoneSummary(BacklogObject):
    
    _REPR_FORMAT_ = "[%(id)s] %(name)s %(due_date)s %(statuses)s"    
    
    def __init__(self,id,name,due_date,statuses=None,burndown_chart=None):
        self.id = id
        self.name = name
        self.due_date = due_date
        self.statuses = [classwrap(x, StatusSummary) for x in statuses] if statuses else None
        self.burndown_chart = burndown_chart

class ProjectSummary(BacklogObject):
    
    _REPR_FORMAT_ = "[%(id)s] %(name)s %(key)s %(url)s %(statuses)s %(milestones)s %(current_milestone)s"
        
    def __init__(self,id,name,key,url,statuses,milestones,current_milestone=None):
        self.id = id
        self.name = name
        self.key = key
        self.url = url
        self.statuses = [classwrap(x, StatusSummary) for x in statuses] if statuses else None
        self.milestones = [classwrap(x, MilestoneSummary) for x in milestones] if milestones else None        
        self.current_milestone = classwrap(current_milestone, MilestoneSummary)

class AddComment(BacklogObject):
    
    _REPR_FORMAT_ = "[%(key)s] %(content)s"
    
    def __init__(self,key,content):
        self.key = key
        self.content = content

###
### 以下 BacklogAdmin 用のモデルオブジェクト
###
     
class AdminUser(BacklogObject):
    
    _REPR_FORMAT_ = "[%(id)s] %(user_id)s %(mail_address)s %(role)s"    
    
    def __init__(self,id,user_id,name,mail_address,role,mail_setting,created_on,updated_on):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.mail_address = mail_address
        self.role = role
        self.mail_setting = mail_setting
        self.created_on = created_on
        self.updated_on = updated_on
        
class AdminAddUser(AdminUser):
    
    _REPR_FORMAT_ = "[%(user_id)s] %(mail_address)s %(role)s"        
    
    def __init__(self,user_id,password_md5,name,mail_address,role,mail_setting=None,icon=None):
        super(AdminAddUser,self).__init__(None,user_id,name,mail_address,role,mail_setting,None,None)
        self.password_md5 = password_md5
        self.icon = icon

class AdminUpdateUser(AdminAddUser):
    
    _REPR_FORMAT_ = "[%(id)s] %(mail_address)s %(role)s"        
            
    def __init__(self,id,password_md5=None,name=None,mail_address=None,role=None,mail_setting=None,icon=None):
        super(AdminUpdateUser,self).__init__(None,password_md5,name,mail_address,role,mail_setting,icon)
        self.id = id
        
class AdminProject(Project):
    
    def __init__(self,id,name,key,url,use_chart=False,archived=False,created_on=None,updated_on=None,text_formatting_rule=None,use_parent_child_issue=False):
        super(AdminProject,self).__init__(id,key,name,url,archived,text_formatting_rule,use_parent_child_issue)
        self.use_chart = use_chart
        self.created_on = created_on
        self.updated_on = updated_on

class AdminAddProject(BacklogObject):

    _REPR_FORMAT_ = "[%(key)s] %(name)s %(use_chart)s"            
    
    def __init__(self,name,key,use_chart=False):
        self.name = name
        self.key = key
        self.use_char = use_chart
        
class AdminUpdateProject(AdminProject):
    
    def __init__(self,id,name=None,key=None,use_chart=False,archived=False):
        super(AdminUpdateProject,self).__init__(id,name,key,None,use_chart,archived)
        
class AdminProjectUser(BacklogObject):
    
    _REPR_FORMAT_ = "[%(id)s] %(user_id)s %(name)s"    
    
    def __init__(self,id,user_id,name):
        self.id = id
        self.user_id = user_id
        self.name = name

class AdminAddProjectUser(BacklogObject):
    
    _REPR_FORMAT_ = "[%(project_id)s][%(user_id)s]"        
    
    def __init__(self,project_id,user_id):
        self.project_id = project_id
        self.user_id = user_id
        
class AdminUpdateProjectUsers(BacklogObject):
    
    _REPR_FORMAT_ = "[%(project_id)s]"        
    
    def __init__(self,project_id,user_id):
        self.project_id = project_id
        # 以下の user_id は配列
        self.user_id = user_id    
    