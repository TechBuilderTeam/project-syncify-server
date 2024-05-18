from rest_framework import generics, status
from rest_framework.response import Response
from .models import Member,roles_choice,WorkSpace
from .serializers import MemberSerializer
from django.db.models import Case, When, Value, IntegerField
from .utils import *
from accounts.models import User
from django.utils.encoding import force_str
from django.shortcuts import redirect

from django.core.signing import SignatureExpired

# Add new member to  workspaces
class AddMember(generics.GenericAPIView):
    #method: POST, body: workspace_name=workspace.id,user,role
    # queryset = Member.objects.all()
    serializer_class = MemberSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        workspace = serializer.validated_data['workspace_Name']
        user = serializer.validated_data['user']
        # Check if the user is the manager of the workspace
        if workspace.workSpace_manager == user:
            return Response({"error": "Workspace manager cannot be assigned as a member."}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=user.email).exists():
            # Send an email to the user to accept the join request
            send_join_request_email(user,workspace)
        else:
            # Send a registration link to the email
            registration_link = generate_registration_link(user.email)
            send_registration_email(user.email, registration_link)
            # Set the user's status to "pending" since they haven't registered yet
            
        
        # Save the member with the appropriate status
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

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
      
    
class ActivateMemberView(generics.GenericAPIView):
    def get(self, request, uid64, token):
        try:
            uid = urlsafe_base64_decode(uid64).decode()
            user = User._default_manager.get(pk=uid)
        except User.DoesNotExist:
            user = None 
        
        if user is not None and default_token_generator.check_token(user, token):
            member = Member.objects.get(user=user, pending=True)
            member.pending = False
            member.save()
            return Response({'message': 'Member activated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)
