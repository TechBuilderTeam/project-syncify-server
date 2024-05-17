from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status,generics
from django.db.models import Q
from rest_framework.views import APIView

#* ============ There will be All the Functions of the WorkSpace   ============ *# 


#* ============ This is the worksapce viewset   ============ *# 
class workSpaceViewSet(viewsets.ModelViewSet):
    queryset =  WorkSpace.objects.all()
    serializer_class = WorkSpaceSerializer


class WorkspaceMembersList(generics.ListAPIView):
    serializer_class = MemberSerializer

    def get_queryset(self):
        workspace_id = self.kwargs['workspace_id']
        return Member.objects.filter(workspace_Name_id=workspace_id)


# @api_view(['POST'])
# class createWorkSpaceView(request):


#* ============ This is for search members and find them   ============ *# 
@api_view(['GET'])
def search_member(request):
    search_query = request.GET.get('search', '')

    if search_query:
        members = Member.objects.filter(
            Q(role__icontains=search_query) | 
            Q(id__icontains=search_query) | 
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query)| 
            Q(user__email__icontains=search_query)
        )
    else:
        members = Member.objects.all()
    serializer = MemberSerializer(members, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


#* ============ This the Creation of the Member viewset   ============ *# 
class MemberViewSet(viewsets.ModelViewSet):
    queryset =  Member.objects.all()
    serializer_class = MemberSerializer


#* ============ This the Creation of the Timeline viewset   ============ *# 
class TimelineViewSet(viewsets.ModelViewSet):
    queryset =  Timeline.objects.all()
    serializer_class = TimeLineSerializer

class WorkspaceTimelinesList(generics.ListAPIView):
    serializer_class = TimeLineSerializer

    def get_queryset(self):
        workspace_id = self.kwargs['workspace_id']
        return Timeline.objects.filter(workspace_Name_id=workspace_id)

#* ============ View to check if a user is a member of a specific workspace ============ *# 
class IsUserMember(APIView):

    def get(self, request, workspace_id, user_id):
        try:
            member = Member.objects.get(workspace_Name_id=workspace_id, user_id=user_id)
            is_member = True if member else False
        except Member.DoesNotExist:
            is_member = False
        return Response({'is_member': is_member}, status=status.HTTP_200_OK)


#* ============ View to list all workspaces associated with a user ============ *# 
class UserWorkspaces(generics.ListAPIView):
    serializer_class = WorkSpaceSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return WorkSpace.objects.filter(member__user_id=user_id)