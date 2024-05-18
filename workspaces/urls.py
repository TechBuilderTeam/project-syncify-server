from django.urls import path, include
from rest_framework import routers
from .views import *

#* ============= There will be all the routers ========== *#

router = routers.DefaultRouter()

router.register('list' , workSpaceViewSet)
router.register('member' , MemberViewSet)
router.register('timeline' , TimelineViewSet)
router.register('scrum' , scrumViewset)
router.register('task' , taskViewset)
router.register('taskcomments' , taskCommentViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('api/search-member/', search_member, name='search-member'),
    path('userWorkspace/<int:workspace_id>/user/<int:user_id>/is_member/', IsUserMember.as_view(), name='is-user-member'),
    path('user/<int:user_id>/workspaces/', UserWorkspaces.as_view(), name='user-workspaces'),
    path('singleworkspace/<int:workspace_id>/members/', WorkspaceMembersList.as_view(), name='workspace-members'), path('workspace/<int:workspace_id>/members/', WorkspaceMembersList.as_view(), name='workspace-members'),
    path('singleworkspace/<int:workspace_id>/timelines/', WorkspaceTimelinesList.as_view(), name='workspace-timelines'),
    path('timeline/<int:timeline_id>/scrums/', timeline_scrums, name='timeline-scrums'),
    path('scrum/<int:scrum_id>/tasks/', scrum_tasks, name='scrum-tasks'),
    path('taskcomments/<int:task_id>/comments/', task_comments, name='task-comments'),
    path('user/<int:user_id>/workspace/<int:workspace_id>/position/', user_position_in_workspace, name='user-position-in-workspace'),
    path('task/<int:pk>/priority/', TaskPriorityUpdateView.as_view(), name='task-priority-update'),
    path('task/<int:pk>/status/', TaskPriorityUpdateView.as_view(), name='task-priority-update'),
    
]


