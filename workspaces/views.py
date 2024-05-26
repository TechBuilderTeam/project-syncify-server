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
from django.db.models import Avg, Max, Min
from rest_framework.exceptions import NotFound

#* ============ There will be All the Functions of the WorkSpace   ============ *# 


#* ============ This is the worksapce viewset   ============ *# 
class workSpaceViewSet(viewsets.ModelViewSet):
    queryset =  WorkSpace.objects.all()
    serializer_class = WorkSpaceSerializer
#* ======== Get Workspace name ====== #
class WorkSpaceDetailView(generics.RetrieveAPIView):
    queryset = WorkSpace.objects.all()
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


#* ============ This the GET of the Timeline viewset   ============ *# 
class TimelineDetailView(generics.RetrieveAPIView):
    queryset = Timeline.objects.all()
    serializer_class = TimelineDetailSerializer

#* ============ This the Creation of the Timeline viewset   ============ *# 
class TimelineCreateView(generics.CreateAPIView):
    queryset = Timeline.objects.all()
    serializer_class = TimelineCreationSerializer

#* ============ This the Update of the Timeline viewset   ============ *# 
class TimelineUpdateView(generics.UpdateAPIView):
    queryset = Timeline.objects.all()
    serializer_class = TimelineCreationSerializer

#* ============ This the Delete  of the Timeline viewset   ============ *# 
class TimelineDeleteView(generics.DestroyAPIView):
    queryset = Timeline.objects.all()
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"detail": "Timeline deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except NotFound:
            return Response({"detail": "Timeline not found."}, status=status.HTTP_404_NOT_FOUND)


# * ============ View to Change the timeline staus    ================
class UpdateTimelineStatusView(generics.UpdateAPIView):
    queryset = Timeline.objects.all()
    serializer_class = TimelineStatusSerializer



# * ============ View to handle Get all Timeline for a single workspace ================
class WorkspaceTimelinesList(generics.ListAPIView):
    serializer_class = TimelineDetailSerializer

    def get_queryset(self):
        workspace_id = self.kwargs['workspace_id']
        return Timeline.objects.filter(workspace_Name_id=workspace_id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        max_duration = queryset.aggregate(Max('duration'))['duration__max']
        min_duration = queryset.aggregate(Min('duration'))['duration__min']
        avg_duration = queryset.aggregate(Avg('duration'))['duration__avg']

        # Find the timeline with the longest duration
        if max_duration is not None:
            max_duration_timeline = queryset.filter(duration=max_duration).first()
            max_duration_timeline_name = max_duration_timeline.name if max_duration_timeline else None
        else:
            max_duration_timeline_name = None

        response_data = {
            'max_duration_timeline_name': max_duration_timeline_name,
            'max_duration': max_duration,
            'min_duration': min_duration,
            'avg_duration': avg_duration,
            'timelines': serializer.data,
        }

        return Response(response_data)
    

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

class ScrumCreateAPIView(generics.CreateAPIView):
    queryset = Scrum.objects.all()
    serializer_class = CreateScrumSerializer

class ScrumRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Scrum.objects.all()
    serializer_class = ScrumSerializer

class ScrumUpdateAPIView(generics.UpdateAPIView):
    queryset = Scrum.objects.all()
    serializer_class = ScrumSerializer

class ScrumDeleteAPIView(generics.DestroyAPIView):
    queryset = Scrum.objects.all()
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"detail": "Scrum deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except NotFound:
            return Response({"detail": "Scrum not found."}, status=status.HTTP_404_NOT_FOUND)

class ScrumListByTimelineAPIView(generics.ListAPIView):
    serializer_class = ScrumSerializer

    def get_queryset(self):
        timeline_id = self.kwargs['timeline_id']
        return Scrum.objects.filter(timeline_Name_id=timeline_id)

# * ============== Create Task =================
class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskCreationSerializer

class TaskDetailView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer
    lookup_field = 'pk'

class TaskUpdateView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskCreationSerializer
    lookup_field = 'pk'

class TaskDeleteView(generics.DestroyAPIView):
    queryset = Task.objects.all()
    lookup_field = 'pk'

    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"detail": "Task deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Task.DoesNotExist:
            return Response({"detail": "Task not found."}, status=status.HTTP_404_NOT_FOUND)

#Get all task for single scurm 
class ScrumTasksListView(generics.ListAPIView):
    serializer_class = TaskDetailSerializer

    def get_queryset(self):
        scrum_id = self.kwargs['scrum_id']
        return Task.objects.filter(scrum_Name_id=scrum_id).order_by('-priority')

#* ======================= view for assgin user to task ============ 
class TaskUpdateAssignedUserView(generics.GenericAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskAssignUserSerializer

    def put(self, request, *args, **kwargs):
        task = self.get_object()
        serializer = TaskAssignUserSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                updated_task = serializer.assign_user_to_task(task, serializer.validated_data['email'])
                response_serializer = TaskDetailSerializer(updated_task)
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            except serializers.ValidationError as e:
                return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
class TaskStatusUpdateView(generics.UpdateAPIView):
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