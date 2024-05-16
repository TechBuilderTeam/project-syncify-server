from django.urls import path, include
from rest_framework import routers
from .views import *

#* ============= There will be all the routers ========== *#

router = routers.DefaultRouter()

router.register('list' , workSpaceViewSet)
router.register('member' , MemberViewSet)
router.register('timeline' , TimelineViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/search-member/', search_member, name='search-member'),
]
