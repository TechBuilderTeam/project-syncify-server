from django.urls import path, include
from rest_framework import routers
from .views import *

#* ============= There will be all the routers ========== *#

router = routers.DefaultRouter()

router.register('list' , workSpaceViewSet)
router.register('member' , MemberViewSet)
router.register('create/timeline' , TimelineViewSet)
router.register('create/scrum' , scrumViewset)
router.register('create/task' , taskViewset)
router.register('create/taskcomments' , taskCommentViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('api/search-member/', search_member, name='search-member'),

    path('userWorkspace/<int:workspace_id>/user/<int:user_id>/is_member/', IsUserMember.as_view(), name='is-user-member'),
    path('singleWorkspace/<int:pk>/', WorkSpaceDetailView.as_view(), name='workspace_detail'),
    path('user/<int:user_id>/workspaces/', UserWorkspaces.as_view(), name='user-workspaces'),
    path('user/<int:user_id>/workspace/<int:workspace_id>/position/', user_position_in_workspace, name='user-position-in-workspace'),

    path('singleworkspace/<int:workspace_id>/members/', WorkspaceMembersList.as_view(), name='workspace-members'), 
    path('workspace/<int:workspace_id>/members/', WorkspaceMembersList.as_view(), name='workspace-members'),
    
    path('singleworkspace/<int:workspace_id>/timelines/list/', WorkspaceTimelinesList.as_view(), name='workspace-timelines'),
    path('singletimeline/<int:timeline_id>/scrums/list/', timeline_scrums, name='timeline-scrums'),
    
    path('singlescrum/<int:scrum_id>/tasks/list/', scrum_tasks, name='scrum-tasks'),
    path('task/<int:pk>/priority/update/', TaskPriorityUpdateView.as_view(), name='task-priority-update'),
    path('task/<int:pk>/status/update/', TaskPriorityUpdateView.as_view(), name='task-priority-update'),
    
    path('taskcomments/<int:task_id>/comments/list/', task_comments, name='task-comments'),
    
    
]


