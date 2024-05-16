from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q


#* ============ There will be All the Functions of the WorkSpace   ============ *# 


#* ============ This is the worksapce viewset   ============ *# 
class workSpaceViewSet(viewsets.ModelViewSet):
    queryset =  WorkSpace.objects.all()
    serializer_class = WorkSpaceSerializer


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


#* ============ This the  of the Timeline viewset   ============ *# 


