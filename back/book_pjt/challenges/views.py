from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime

from .models import Challenge, ChallengeParticipant, ChallengeComment, BookQuiz, QuizAttempt
from .serializers import (
    ChallengeSerializer,
    ChallengeParticipantSerializer,
    ChallengeCommentSerializer,
    BookQuizSerializer,
    QuizAttemptSerializer
)
from .utils import generate_quizzes_for_book, record_quiz_attempt


class ChallengeViewSet(viewsets.ModelViewSet):
    serializer_class = ChallengeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Challenge.objects.all().order_by('-created_at')
        user = self.request.user
        params = self.request.query_params

        if user.is_authenticated and params.get('joined') == '1':
            queryset = queryset.filter(participants__user=user).distinct()

        if user.is_authenticated and params.get('creator') == 'me':
            queryset = queryset.filter(creator=user)

        return queryset
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def perform_create(self, serializer):
        challenge = serializer.save(creator=self.request.user)


        ChallengeParticipant.objects.create(
            challenge=challenge,
            user=self.request.user
        )


        if challenge.book and BookQuiz.objects.filter(book=challenge.book).count() < 20:
            generate_quizzes_for_book(challenge.book)


    @action(detail=False, methods=['get'], url_path='my', permission_classes=[IsAuthenticated])
    def my_challenges(self, request):
        user = request.user
        queryset = Challenge.objects.filter(participants__user=user).distinct()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ChallengeParticipantViewSet(viewsets.ModelViewSet):
    queryset = ChallengeParticipant.objects.all()
    serializer_class = ChallengeParticipantSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ChallengeCommentViewSet(viewsets.ModelViewSet):
    queryset = ChallengeComment.objects.all().order_by('-created_at')
    serializer_class = ChallengeCommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class QuizViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def start(self, request):
        challenge_id = request.query_params.get('challenge')
        challenge = Challenge.objects.get(id=challenge_id)
        today = datetime.today().date()

        attempts_today = QuizAttempt.objects.filter(
            challenge=challenge,
            user=request.user,
            submitted_at__date=today
        ).count()

        if attempts_today >= 2:
            return Response({'error': '오늘 도전 가능 횟수를 초과했습니다.'}, status=403)

        quizzes = BookQuiz.objects.filter(book=challenge.book).order_by('?')[:5]
        return Response(BookQuizSerializer(quizzes, many=True).data)

    @action(detail=False, methods=['post'])
    def submit(self, request):
        challenge_id = request.data.get('challenge')
        score = request.data.get('score')
        challenge = Challenge.objects.get(id=challenge_id)

        # ✅ record_quiz_attempt를 통해 퀴즈 기록 및 성공 처리
        attempt = record_quiz_attempt(request.user, challenge, score)
        return Response(QuizAttemptSerializer(attempt).data)
