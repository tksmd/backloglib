#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2009 - 2014 Takashi SOMEDA
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
Backlog (http://www.backlog.jp/) client libarary

Backlog のクライアントライブラリです。
XML-RPC で提供されている API に対してアクセスを行い、オブジェクトにラッピングして
返す機能を提供します。
"""

__version__ = "0.2.2"
__author__ = "someda@isenshi.com"

__all__ = ["Backlog", "BacklogAdmin"]

#
# Backlog (http://www.backlog.jp) CLIENT LIBRARY
#
from xmlrpclib import ServerProxy

from utils import classwrap
from models import *

_URI_FORMAT_ = "https://%(username)s:%(password)s@%(space)s.backlog.jp/XML-RPC"


class BacklogBase(object):
    def __init__(self, space, username, password):
        uri = _URI_FORMAT_ % {"username": username, "password": password, "space": space}
        self.server = ServerProxy(uri)


class Backlog(BacklogBase):
    """
    @since: 0.1.1 (Backlog R2009-01-30)
    """

    def get_projects(self):
        projects = self.server.backlog.getProjects()
        return [Project(**x) for x in projects]

    def get_project(self, key):
        project = self.server.backlog.getProject(key)
        return Project(**project)

    def get_components(self, project_id):
        components = self.server.backlog.getComponents(project_id)
        return [Component(**x) for x in components]

    def get_versions(self, project_id):
        versions = self.server.backlog.getVersions(project_id)
        return [Version(**x) for x in versions]

    def get_users(self, project_id):
        users = self.server.backlog.getUsers(project_id)
        return [User(**x) for x in users]

    def get_issue_types(self, project_id):
        issue_types = self.server.backlog.getIssueTypes(project_id)
        return [IssueType(**v) for v in issue_types]

    def get_issue(self, key):
        issue = self.server.backlog.getIssue(key)
        return Issue(**issue)

    def get_comments(self, issue_id):
        comments = self.server.backlog.getComments(issue_id)
        return [Comment(**x) for x in comments]

    def count_issue(self, condition):
        if not isinstance(condition, FindCondition):
            condition = FindCondition(condition)
        return self.server.backlog.countIssue(condition.serialize())

    def find_issue(self, condition):
        if not isinstance(condition, FindCondition):
            condition = FindCondition(condition)
        issues = self.server.backlog.findIssue(condition.serialize())
        return [Issue(**x) for x in issues]

    def create_issue(self, issue):
        issue = classwrap(issue, Issue)
        ret = self.server.backlog.createIssue(issue.serialize())
        return Issue(**ret)

    def update_issue(self, issue):
        issue = classwrap(issue)
        ret = self.server.backlog.updateIssue(issue.serialize())
        return Issue(**ret)

    def switch_status(self, status):
        status = classwrap(status, UpdateStatus)
        ret = self.server.backlog.switchStatus(status.serialize())
        return Issue(**ret)

    def add_issue_type(self, issueType):
        """
        @since: 0.2.1 (Backlog R2010-03-31)
        """
        issueType = classwrap(issueType, AddIssueType)
        ret = self.server.backlog.addIssueType(issueType.serialize())
        return IssueType(**ret)

    def update_issue_type(self, issueType):
        """
        @since: 0.2.1 (Backlog R2010-03-31)
        """
        issueType = classwrap(issueType, IssueType)
        ret = self.server.backlog.updateIssueType(issueType.serialize())
        return IssueType(**ret)

    def delete_issue_type(self, id, substitute_id=None):
        """
        @since: 0.2.1 (Backlog R2010-03-31)
        """
        args = {"id": id}
        if substitute_id:
            args["substitute_id"] = substitute_id
        ret = self.server.backlog.deleteIssueType(args)
        return IssueType(**ret)

    def add_version(self, version):
        """
        @since: 0.2.1 (Backlog R2010-03-31)
        """
        version = classwrap(version, AddVersion)
        ret = self.server.backlog.addVersion(version.serialize())
        return UpdateVersion(**ret)

    def update_version(self, version):
        """
        @since: 0.2.1 (Backlog R2010-03-31)
        """
        version = classwrap(version, UpdateVersion)
        ret = self.server.backlog.updateVersion(version.serialize())
        return UpdateVersion(**ret)

    def delete_version(self, id):
        """
        @since: 0.2.1 (Backlog R2010-03-31)
        """
        ret = self.server.backlog.deleteVersion(id)
        return UpdateVersion(**ret)

    def add_component(self, component):
        """
        @since: 0.2.1 (Backlog R2010-03-31)
        """
        component = classwrap(component, AddComponent)
        ret = self.server.backlog.addComponent(component.serialize())
        return Component(**ret)

    def update_component(self, component):
        """
        @since: 0.2.1 (Backlog R2010-03-31)
        """
        component = classwrap(component, Component)
        ret = self.server.backlog.updateComponent(component.serialize())
        return Component(**ret)

    def delete_component(self, id):
        """
        @since: 0.2.1 (Backlog R2010-03-31)
        """
        ret = self.server.backlog.deleteComponent(id)
        return Component(**ret)

    def get_timeline(self):
        """
        @since: 0.2.1 (Backlog R2010-10-28)        
        """
        ret = self.server.backlog.getTimeline()
        return [Timeline(**x) for x in ret]

    def get_activity_types(self):
        """
        @since: 0.2.1 (Backlog R2010-10-28)        
        """
        ret = self.server.backlog.getActivityTypes();
        return [ActivityType(**x) for x in ret]

    def add_comment(self, comment):
        """
        @since: 0.2.1 (Backlog R2010-10-28)        
        """
        comment = classwrap(comment, AddComment)
        ret = self.server.backlog.addComment(comment.serialize())
        return Comment(**ret)

    def get_project_summary(self, project_id):
        """
        @since: 0.2.1 (Backlog R2010-10-28)        
        """
        ret = self.server.backlog.getProjectSummary(project_id)
        return ProjectSummary(**ret)

    def get_project_summaries(self):
        """
        @since: 0.2.1 (Backlog R2010-10-28)        
        """
        ret = self.server.backlog.getProjectSummaries()
        return [ProjectSummary(**x) for x in ret]

    def get_user(self, user_id):
        """
        @since: 0.2.1 (Backlog R2010-10-28)        
        """
        ret = self.server.backlog.getUser(user_id)
        return DetailUser(**ret)

    def get_user_icon(self, user_id):
        """
        @since: 0.2.1 (Backlog R2010-10-28)        
        """
        ret = self.server.backlog.getUserIcon(user_id)
        return UserIcon(**ret)

    def get_statuses(self):
        """
        @since: 0.2.1 (Backlog R2010-10-28)        
        """
        statuses = self.server.backlog.getStatuses()
        return [Status(**x) for x in statuses]

    def get_resolutions(self):
        """
        @since: 0.2.1 (Backlog R2010-10-28)        
        """
        resolutions = self.server.backlog.getResolutions()
        return [Resolution(**x) for x in resolutions]

    def get_priorities(self):
        """
        @since: 0.2.1 (Backlog R2010-10-28)        
        """
        priorities = self.server.backlog.getPriorities()
        return [Priority(**x) for x in priorities]


class BacklogAdmin(BacklogBase):
    """
    @since: 0.2.1 (Backlog R2010-03-31)
    """
    ROLE_ADMIN = "admin"
    ROLE_NORMAL_USER = "normal-user"
    ROLE_REPORTER = "reporter"
    ROLE_VIEWER = "viewer"
    ROLE_GUEST_REPORTER = "guest-reporter"
    ROLE_GUEST_VIEWER = "guest-viewer"

    def get_users(self):
        users = self.server.backlog.admin.getUsers()
        return [AdminUser(**x) for x in users]

    def add_user(self, user):
        user = classwrap(user, AdminAddUser)
        ret = self.server.backlog.admin.addUser(user.serialize())
        return AdminUser(**ret)

    def update_user(self, user):
        if isinstance(user, AdminUser):
            user = vars(user)
            del user["created_on"]
            del user["updated_on"]
            del user["user_id"]
            user = AdminUpdateUser(**user)
        elif not isinstance(user, AdminUpdateUser):
            user = AdminUpdateUser(**user)
        ret = self.server.backlog.admin.updateUser(user.serialize())
        return AdminUser(**ret)

    def delete_user(self, id):
        user = self.server.backlog.admin.deleteUser(id)
        return AdminUser(**user)

    def get_projects(self):
        projects = self.server.backlog.admin.getProjects()
        return [AdminProject(**x) for x in projects]

    def add_project(self, project):
        project = classwrap(project, AdminAddProject)
        ret = self.server.backlog.admin.addProject(project.serialize())
        return AdminProject(**ret)

    def update_project(self, project):
        if isinstance(project, AdminProject):
            project = vars(project)
            del project["created_on"]
            del project["updated_on"]
            del project["url"]
            project = AdminUpdateProject(**project)
        elif not isinstance(project, AdminUpdateProject):
            project = AdminUpdateProject(**project)
        ret = self.server.backlog.admin.updateProject(project.serialize())
        return AdminProject(**ret)

    def delete_project(self, id):
        ret = self.server.backlog.admin.deleteProject(id)
        return AdminProject(**ret)

    def get_project_users(self, project_id):
        ret = self.server.backlog.admin.getProjectUsers(project_id)
        return [AdminProjectUser(**x) for x in ret]

    def add_project_user(self, project_user):
        project_user = classwrap(project_user, AdminAddProjectUser)
        ret = self.server.backlog.admin.addProjectUser(project_user.serialize())
        return [AdminProjectUser(**x) for x in ret]

    def update_project_users(self, project_users):
        project_users = classwrap(project_users, AdminUpdateProjectUsers)
        ret = self.server.backlog.admin.updateProjectUsers(project_users.serialize())
        return [AdminProjectUser(**x) for x in ret]

    def delete_project_user(self, project_user):
        project_user = classwrap(project_user, AdminAddProjectUser)
        ret = self.server.backlog.admin.deleteProjectUser(project_user.serialize())
        return [AdminProjectUser(**x) for x in ret]
