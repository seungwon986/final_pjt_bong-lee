from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Challenge, ChallengeParticipant, ChallengeComment
from .serializers import (
    ChallengeSerializer,
    ChallengeParticipantSerializer,
    ChallengeCommentSerializer
)


class ChallengeViewSet(viewsets.ModelViewSet):

    serializer_class = ChallengeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Challenge.objects.all().order_by('-created_at')
        user = self.request.user
        params = self.request.query_params

        # ?joined=1 → 내가 참여한 챌린지
        if user.is_authenticated and params.get('joined') == '1':
            queryset = queryset.filter(participants__user=user).distinct()

        # ?creator=me → 내가 만든 챌린지
        if user.is_authenticated and params.get('creator') == 'me':
            queryset = queryset.filter(creator=user)

        return queryset

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


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
