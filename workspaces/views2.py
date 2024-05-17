from rest_framework import generics, status
from rest_framework.response import Response
from .models import Member,roles_choice
from .serializers import MemberSerializer
from django.db.models import Case, When, Value, IntegerField

class AddMember(generics.CreateAPIView):
    #method: POST, body: workspace_name=workspace.id,user,role
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class RemoveMember(generics.DestroyAPIView):
    queryset = Member.objects.all()

    def destroy(self, request, *args, **kwargs):
        # method: DELETE, body:workspace_id,user_id 
        workspace_id = request.data.get('workspace_id')
        user_id = request.data.get('user_id')
        if workspace_id is None or user_id is None:
            return Response({"error": "workspace_id and user_id are required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            member = self.get_queryset().get(workspace_Name_id=workspace_id, user_id=user_id)
            member.delete() #Delete the member
            return Response(status=status.HTTP_200_OK)
        except Member.DoesNotExist:
            return Response({"error": "Member not found"}, status=status.HTTP_404_NOT_FOUND)

class ChangeRole(generics.UpdateAPIView):
    # method: PATCH/PUT, body:workspace_id,user_id,new_role
    
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    def update(self, request, *args, **kwargs):
        workspace_id = request.data.get('workspace_id')
        user_id = request.data.get('user_id')
        new_role = request.data.get('new_role')
        if workspace_id is None or user_id is None or new_role is None:
            return Response({"error": "workspace_id, user_id, and new_role are required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            member = self.get_queryset().get(workspace_Name_id=workspace_id, user_id=user_id)
            member.role = new_role
            member.save()
            return Response(MemberSerializer(member).data)
        except Member.DoesNotExist:
            return Response({"error": "Member not found"}, status=status.HTTP_404_NOT_FOUND)
        
class WorkspaceMembersList(generics.ListAPIView): #method: GET
    serializer_class = MemberSerializer

    def get_queryset(self):
        workspace_id = self.kwargs['workspace_id']
        order_by_roles = Case(
            When(role=roles_choice.ASSOCIATE_MANAGER, then=Value(1)),
            When(role=roles_choice.TEAM_LEADER, then=Value(2)),
            default=Value(3),
            output_field=IntegerField(),
        )
        queryset = Member.objects.filter(workspace_Name_id=workspace_id).order_by(order_by_roles)
        return queryset
