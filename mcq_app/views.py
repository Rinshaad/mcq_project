from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.views import APIView,Response
from rest_framework import status,permissions
from django.contrib.auth import authenticate,login,logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Question, Answer, UserProfile, UserAnswer
from .serializers import QuestionSerializer, UserAnswerSerializer
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@api_view(['POST'])
def user_registration(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if User.objects.filter(username=username).exists():
        return Response({'message': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password)
    return Response({'message': 'User registered successfully.'})

@api_view(['POST'])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({'message': 'Login successful.'})
    return Response({'message': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def user_logout(request):
    logout(request)
    return Response({'message': 'Logout successful.'})

@api_view(['POST'])
def add_question(request):
    serializer = QuestionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Question added successfully.'})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def question_list(request):
    questions = Question.objects.all()
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def answer_question(request):
    user = request.user
    question_id = request.data.get('question_id')
    answer_id = request.data.get('answer_id')

    question = Question.objects.get(id=question_id)
    answer = Answer.objects.get(id=answer_id)

    result = answer.is_correct

    user_answer = UserAnswer(user=user, question=question, answer=answer, is_correct=result)
    user_answer.save()

    return Response({'message': 'Answer submitted successfully.'})

@api_view(['GET'])
def calculate_marks(request):
    user = request.user
    user_answers = UserAnswer.objects.filter(user=user)
    correct_answers = user_answers.filter(is_correct=True).count()
    wrong_answers = user_answers.filter(is_correct=False).count()
    total_marks = correct_answers - (0.25 * wrong_answers)

    user_profile = UserProfile.objects.get(user=user)
    user_profile.marks = total_marks
    user_profile.save()

    return Response({'score': total_marks})