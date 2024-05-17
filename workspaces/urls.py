from django.urls import path, include
from rest_framework import routers
from .views import *
from .views2 import AddMember, RemoveMember, ChangeRole,WorkspaceMembersList

#* ============= There will be all the routers ========== *#

router = routers.DefaultRouter()

router.register('list' , workSpaceViewSet)
router.register('member' , MemberViewSet)
router.register('timeline' , TimelineViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/search-member/', search_member, name='search-member'),
    path('members/add/', AddMember.as_view(), name='add-member'),
    path('members/remove/', RemoveMember.as_view(), name='remove-member'),
    path('members/change-role/', ChangeRole.as_view(), name='change-role'),
    path('workspaces/<int:workspace_id>/members/', WorkspaceMembersList.as_view(), name='workspace-members-list'),
]

