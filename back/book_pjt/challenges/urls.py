from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChallengeViewSet, ChallengeParticipantViewSet, ChallengeCommentViewSet, QuizViewSet

router = DefaultRouter()
router.register(r'challenges', ChallengeViewSet, basename='challenge')
router.register(r'participants', ChallengeParticipantViewSet, basename='participant')
router.register(r'comments', ChallengeCommentViewSet, basename='comment')
router.register(r'quiz', QuizViewSet, basename='quiz')

urlpatterns = [
    path('', include(router.urls)),
]
