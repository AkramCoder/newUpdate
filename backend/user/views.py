from dataclasses import fields
import json
from django.core.serializers import serialize
from urllib import request
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView
from django.http import JsonResponse
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from .models import (CustomUser,
                     Candidate, 
                     Selectedcandidate, 
                     Skill, 
                     Education, 
                     Experience, 
                     Address, 
                     Manager, 
                     Interview,
                     Question,
                     Event,
                     Cv,
                     Permission,
                     ManagerPermission,
                     History)
from company.models import Company
from .serializers import (CustomUserCreateSerializer, 
                          CustomUserSerializer,
                          CandidateCreateSerializer,
                          CandidateSerializer, 
                          SelectedCandidateSerializer,
                          SkillSerializer,
                          EducationSerializer,
                          ExperienceSerializer,
                          AddressSerializer, 
                          ManagerSerializer,
                          ManagerSelectSerializer,
                          InterviewSerializer,
                          InterviewCreateSerializer,
                          QuestionSerializer,
                          EventSerializer,
                          CvSerializer,
                          ManagerUserSerializer,
                          CandidateEventsSerializer,
                          EventDetailSerializer,
                          CandidateDetailsSerializer,
                          EducationCreateSerializer,
                          InterviewDetailSerializer,
                          InterviewsDetailsListSerializer,
                          EventsDetailsSerializer,
                          ManagerDetailsSerializer,
                          ManagerPermissionSerializer,
                          HistorySerializer,
                          TextSerializer)
from .textType import get_data_type

class CustomUserCreateAPIView(generics.CreateAPIView):
    serializer_class = CustomUserCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AuthView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'You are authenticated'}
        return Response(content)

#@api_view(["GET"])
#def currentUserView(request):
#    user = request.user
#    if user.is_authenticated:
#        user_info = serialize("json", [request.user],fields=['email','first_name','last_name','gender','birthday'])
#        user_info_id = json.loads(user_info)
#        return JsonResponse({"user":user_info_id[0]['fields']})
#    else:
#       return JsonResponse({"user":None})
#    if request.user.is_authenticated:
#        user_info = serialize("json", [request.user],fields=['email','first_name'])
#        user_info_id = json.loads(user_info)
#        return JsonResponse({"user":user_info_id[0]['fields']})
#    else:
#        return JsonResponse({"user":None})

class CustomUserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    
class UserUpdateView(APIView):
    # authentication_classes = [SessionAuthentication, TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    def put(self, request):
        try:
            user = CustomUser.objects.get(id=request.data.get('id'))
        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Update user fields
        user.first_name = request.data.get('first_name', user.first_name)
        user.last_name = request.data.get('last_name', user.last_name)
        user.gender = request.data.get('gender', user.gender)
        user.birthday = request.data.get('birthday', user.birthday)
        user.phone_number = request.data.get('phone_number', user.phone_number)
        user.profile_picture = request.data.get('profile_picture', user.profile_picture)
        user.language = request.data.get('language', user.language)

        # Save updated user
        user.save()

        return Response({"detail": "User updated successfully."}, status=status.HTTP_200_OK)
    

# class CustomUserUpdateAPIView(generics.UpdateAPIView):
#     serializer_class = CustomUserSerializer
#     queryset = CustomUser.objects.all()
#     permission_classes = [AllowAny]
    
#     def get_queryset(self):
#         return self.request.user
        

#     def update(self, request, *args, **kwargs):
#         print("=================11")
#         partial = kwargs.pop('partial', False)
#         instance = CustomUser.objects.get(id=17)
#         print("===========>", instance)
#         print("===========>", request.data)
#         print("===========>", partial)

#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)

#         if getattr(instance, '_prefetched_objects_cache', None):
#             instance._prefetched_objects_cache = {}

#         return Response(serializer.data)
    
class DetailCustomUserCreateAPIView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CandidateList(generics.ListCreateAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateCreateSerializer


class CandidateDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateDetailsSerializer


class CandidateViewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer


class SelectedCandidateListCreateAPIView(generics.ListCreateAPIView):
    queryset = Selectedcandidate.objects.all()
    serializer_class = SelectedCandidateSerializer
    permission_classes = (IsAuthenticated,)


class SelectedCandidateRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Selectedcandidate.objects.all()
    serializer_class = SelectedCandidateSerializer
    permission_classes = (IsAuthenticated,)

class SkillListCreateView(generics.ListCreateAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class SkillRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class EducationListCreateView(generics.ListCreateAPIView):
    queryset = Education.objects.all()
    serializer_class = EducationCreateSerializer


class EducationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer

class ExperienceList(generics.ListCreateAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer

class ExperienceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer

class AddressListCreateView(generics.ListCreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

class AddressRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

class ManagerListCreateView(generics.ListCreateAPIView):
    """
    API endpoint that allows managers to be listed or created.
    """
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer

# to display in select fields
class ManagerListSelectView(generics.ListCreateAPIView):
    """
    API endpoint that allows managers to be listed or created.
    """
    queryset = Manager.objects.all()
    serializer_class = ManagerSelectSerializer


class ManagerRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows a manager to be retrieved, updated or deleted.
    """
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer

class InterviewList(generics.ListCreateAPIView):
    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer
    permission_classes = (AllowAny,)

class InterviewCreateList(generics.ListCreateAPIView):
    queryset = Interview.objects.all()
    serializer_class = InterviewCreateSerializer
    permission_classes = (AllowAny,)

class InterviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Interview.objects.all()
    serializer_class = InterviewCreateSerializer
    permission_classes = (AllowAny,)

# interview with its questions
class InterviewDetailQuestions(generics.RetrieveUpdateDestroyAPIView):
    queryset = Interview.objects.all()
    serializer_class = InterviewDetailSerializer

class QuestionListCreateAPIView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        # automatically set the interview based on the URL parameter
        interview_id = self.kwargs.get('interview_id')
        interview = get_object_or_404(Interview, id=interview_id)
        serializer.save(interview=interview)


class QuestionRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (AllowAny,)

class EventListCreateAPIView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (AllowAny,)

class EventRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class CvListCreateView(generics.ListCreateAPIView):
    queryset = Cv.objects.all()
    serializer_class = CvSerializer

class CvDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cv.objects.all()
    serializer_class = CvSerializer



#---------------------------------------------------------------

class Managercurrent(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ManagerUserSerializer
    permission_classes = [IsAuthenticated]

class CandidateEventList(generics.ListCreateAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateEventsSerializer

class EventDetailView(APIView):
    def get(self, request, event_id):
        try:
            event = Event.objects.select_related('responsable', 'candidate').get(id=event_id)
        except Event.DoesNotExist:
            return Response({"detail": "Event not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = EventDetailSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
class EventsDetailsView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventsDetailsSerializer


class InterviewDetailView(APIView):
    def get(self, request, pk):
        try:
            interview = Interview.objects.prefetch_related('responsable').get(id=pk)
        except Event.DoesNotExist:
            return Response({"detail": "Event not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = InterviewDetailSerializer(interview)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CandidateCompanyListCreateAPIView(generics.ListCreateAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        return self.queryset.filter(company = self.request.user.company)
    
class ManagerDetailsListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ManagerDetailsSerializer

    def get_queryset(self):
        selected_manager_id = self.kwargs['manager_id']  
        managers_with_same_parent = Manager.objects.filter(parent=selected_manager_id)
        return managers_with_same_parent

class InterviewDetailList(generics.ListCreateAPIView):
    queryset = Interview.objects.all()
    serializer_class = InterviewsDetailsListSerializer

class ManagerPermissionCreateView(CreateAPIView):
    queryset = ManagerPermission.objects.all()
    serializer_class = ManagerPermissionSerializer

class ManagerPermissionDeleteView(DestroyAPIView):
    queryset = ManagerPermission.objects.all()

class ManagerPermissionListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ManagerPermissionSerializer

    def get_queryset(self):
        manager_id = self.request.query_params.get('managerId')
        queryset = ManagerPermission.objects.filter(manager_id=manager_id)
        return queryset

class PermissionListAPIView(APIView):
    def get(self, request):
        permissions = Permission.objects.all()
        data = [{'id': p.id, 'name': p.name, 'text': p.text} for p in permissions]
        return Response(data)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_update_manager_permission(request):
    if request.method == 'POST':
        data = request.data
        print("data----->", request.data['managerId'])
        manager = Manager.objects.get(id=int(data['managerId'])) 
        if manager.managerpermission_set.exists():
            # manager permissions exist 
            temp = manager.managerpermission_set.all()
            for item in temp: 
                item.delete()

            for p in data.getlist('permissions[]'):
                permission = Permission.objects.get(id=int(p))  # Get the desired permission
                manager_permission = ManagerPermission(manager=manager, permission=permission)
                manager_permission.save()
            return Response({"message": "manager permissions created successfully"}, status=status.HTTP_201_CREATED)
        else: 
            print("manager permission doesn't exist")
            for p in data.getlist('permissions[]'):
                permission = Permission.objects.get(id=int(p))  # Get the desired permission
                manager_permission = ManagerPermission(manager=manager, permission=permission)
                manager_permission.save()
            return Response({"message": "manager permissions created successfully"}, status=status.HTTP_201_CREATED)

    return Response({"message": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)

class HistoryListView(generics.ListAPIView):
    queryset = History.objects.all()
    serializer_class = HistorySerializer
    permission_classes = [IsAuthenticated]

class TextProcessingView(APIView):
    def post(self, request):
        serializer = TextSerializer(data=request.data)

        if serializer.is_valid():
            input_text = serializer.validated_data['input_text']
            result = get_data_type(input_text)

            response_data = {'entities': result}

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)