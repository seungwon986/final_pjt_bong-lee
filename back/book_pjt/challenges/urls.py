from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChallengeViewSet, ChallengeParticipantViewSet, ChallengeCommentViewSet

router = DefaultRouter()
router.register(r'challenges', ChallengeViewSet, basename='challenge')
router.register(r'participants', ChallengeParticipantViewSet, basename='participant')
router.register(r'comments', ChallengeCommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
]
