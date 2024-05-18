from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status,generics
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.decorators import action

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

# View to handle Get all Timeline for a single workspace 
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
        return WorkSpace.objects.filter(
            Q(workSpace_manager_id=user_id) | Q(member__user_id=user_id)
        ).distinct()

#* ============ View for creating the scurm ============ *# 
class scrumViewset(viewsets.ModelViewSet):
    queryset =  Scrum.objects.all()
    serializer_class = ScrumSerializer

# Find all the scurms for an timeline 
@api_view(['GET'])
def timeline_scrums(request, timeline_id):
    try:
        scrums = Scrum.objects.filter(timeline_Name_id=timeline_id)
        serializer = ScrumSerializer(scrums, many=True)
        return Response(serializer.data)
    except Scrum.DoesNotExist:
        return Response({"message": "Timeline scrums not found"}, status=404)
    

#* ============ View for creating the task ============ *# 
class taskViewset(viewsets.ModelViewSet):
    queryset =  Task.objects.all()
    serializer_class = TaskSerializer

#Get all task for single scurm 
@api_view(['GET'])
def scrum_tasks(request, scrum_id):
    try:
        tasks = Task.objects.filter(scrum_Name_id=scrum_id)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    except Task.DoesNotExist:
        return Response({"message": "Scrum tasks not found"}, status=404)

   
#* ============ View for creating the taskComment ============ *# 
class taskCommentViewset(viewsets.ModelViewSet):
    queryset =  TaskComment.objects.all()
    serializer_class = TaskCommentSerializer

#Get all commments for task 
@api_view(['GET'])
def task_comments(request, task_id):
    try:
        comments = TaskComment.objects.filter(task_Name_id=task_id)
        serializer = TaskCommentSerializer(comments, many=True)
        return Response(serializer.data)
    except TaskComment.DoesNotExist:
        return Response({"message": "Task comments not found"}, status=404)
    
#GET the user role for the workpsace
@api_view(['GET'])
def user_position_in_workspace(request, user_id, workspace_id):
    try:
        member = Member.objects.get(user_id=user_id, workspace_Name_id=workspace_id)
        serializer = MemberSerializerForRoleFind(member)
        return Response(serializer.data)
    except Member.DoesNotExist:
        return Response({"message": "Member not found in the specified workspace"}, status=404)

#* ============== This function for change the task priority =====================*#
class TaskPriorityUpdateView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializerPriority

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data, status=status.HTTP_200_OK)


#* ============== This function for change the task status =====================*#
class TaskPriorityUpdateView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializerStatus

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data, status=status.HTTP_200_OK)