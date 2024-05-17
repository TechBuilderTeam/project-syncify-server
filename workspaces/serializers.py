from rest_framework import serializers
from .models import *
from accounts.serilalizers import UserRegisterSerializer

# * ================ This Serializer is for the WorkSpace Creation ================ * #
class WorkSpaceSerializer(serializers.ModelSerializer):
    class Meta: 
        model = WorkSpace
        fields = '__all__'


# * ================ This Serializer is for the Timeline Creation ================ * #
class TimeLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timeline
        fields = ['name','assign','details','start_Date','end_Date','duration','comment','status']
    def validate_assign(self, value):
        if value.role != roles_choice.TEAM_LEADER:
            raise serializers.ValidationError("Assigned member must be a Team Leader")
        return value

# * ================ This Serializer is for the Member Search ================ * #
class MemberSerializer(serializers.ModelSerializer):
    user = UserRegisterSerializer

    class Meta: 
        model = Member
        fields = ['workspace_Name','id', 'role', 'user']

# * ================ This Serializer is for the Scrum ================ * #
class ScrumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scrum
        fields = '__all__'
        

# * ================ This Serializer is for the Task ================ * #
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


# * ================ This Serializer is for the Task ================ * #
class TaskCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskComment
        fields = '__all__'