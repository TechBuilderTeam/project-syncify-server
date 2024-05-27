from rest_framework import serializers
from .models import *
from accounts.serializers import UserRegisterSerializer
from datetime import date

# * ================ This Serializer is for the WorkSpace Creation ================ * #
class WorkSpaceSerializer(serializers.ModelSerializer):
    class Meta: 
        model = WorkSpace
        fields = '__all__'

# * ================ This Serializer is for the Timeline Creation ================ * #
class TimelineCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timeline
        fields = ['workspace_Name','name', 'details', 'start_Date', 'end_Date']
        read_only_fields = ['id', 'assign', 'remaining_time', 'duration', 'status']

    def validate(self, attrs):
        # Validate start and end dates
        if attrs.get('start_Date') and attrs.get('end_Date'):
            if attrs['start_Date'] > attrs['end_Date']:
                raise serializers.ValidationError("Start date cannot be after end date.")
        return attrs

    def create(self, validated_data):
        # Automatically set the status to "To Do"
        validated_data['status'] = Timeline_Status.TO_DO
        return super().create(validated_data)

# * ================ This Serializer is for the Get the Timeline  ================ * #
class AssignedUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Member
        fields = ['id', 'first_name', 'last_name', 'email']

class TimelineDetailSerializer(serializers.ModelSerializer):
    workspace_name = serializers.CharField(source='workspace_Name.name', read_only=True)
    assign = AssignedUserSerializer(read_only=True)
    remaining_time = serializers.SerializerMethodField()

    class Meta:
        model = Timeline
        fields = ['id', 'name', 'details', 'start_Date', 'end_Date', 'workspace_name', 'assign', 'remaining_time', 'duration', 'status']

    def get_remaining_time(self, obj):
        if obj.end_Date:
            remaining_days = (obj.end_Date - date.today()).days
            return remaining_days if remaining_days >= 0 else 0
        return None

class TimelineStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timeline
        fields = ['status']

class TimelineAssignSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)

    class Meta: 
        model = Timeline
        fields = ['email']

    def validate_email(self, value):
        # Check if user exists with this email
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("No user found with this email address.")
        
        # Check if the user is a member of the workspace related to the Timeline instance
        timeline = self.instance
        try:
            member = Member.objects.get(user=user, workspace_Name=timeline.workspace_Name)
        except Member.DoesNotExist:
            raise serializers.ValidationError("User is not a member of the workspace.")
        
        return {'user': user, 'member': member}

    def update(self, instance, validated_data):
        member = validated_data['email']['member']
        instance.assign = member
        instance.save()
        return instance
       
# * ================ This Serializer is for the Member Search ================ * #
class MemberSerializer(serializers.ModelSerializer):
    user = UserRegisterSerializer

    class Meta: 
        model = Member
        fields = ['workspace_Name','id', 'role', 'user']

class MemberSerializerForRoleFind(serializers.ModelSerializer):
    user = UserRegisterSerializer

    class Meta: 
        model = Member
        fields = ['role']


# * ================ This Serializer is for the Scrum ================ * #
class ScrumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scrum
        fields = ['timeline_Name', 'name', 'details']

class CreateScrumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scrum
        fields = ['timeline_Name', 'name', 'details']

    def create(self, validated_data):
        return Scrum.objects.create(**validated_data)

# * ================ This Serializer is for the Task ================ * #
class TaskCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['scrum_Name', 'name', 'details', 'assign']
        read_only_fields = ['status', 'priority', 'which_Type', 'task_Value']

    def create(self, validated_data):
        validated_data['status'] = Task_Status.TO_DO
        validated_data['priority'] = TaskPriority.LOW
        validated_data['which_Type'] = TaskType.TASK
        validated_data['task_Value'] = None
        return super().create(validated_data)

class TaskDetailSerializer(serializers.ModelSerializer):
    assign = AssignedUserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'scrum_Name', 'name', 'details', 'assign', 'status', 'priority', 'which_Type', 'task_Value']


# * ================ This Serializer is for the Task assign ================ * #
class TaskAssignUserSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist.")
        return value

    def assign_user_to_task(self, task, email):
        user = User.objects.get(email=email)
        workspace = task.scrum_Name.timeline_Name.workspace_Name
        
        try:
            member = Member.objects.get(user=user, workspace_Name=workspace)
        except Member.DoesNotExist:
            raise serializers.ValidationError("User is not a member of this workspace.")
        
        task.assign = member
        task.save()
        return task

# * ================ This Serializer is for the Task ================ * #
class TaskSerializerPriority(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['priority']


# * ================ This Serializer is for the Task ================ * #
class TaskSerializerStatus(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['status']


# * ================ This Serializer is for the Task ================ * #
class TaskCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskComment
        fields = '__all__'
