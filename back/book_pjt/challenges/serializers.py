from rest_framework import serializers
from .models import Challenge, ChallengeParticipant, ChallengeComment, BookQuiz, QuizAttempt


class ChallengeSerializer(serializers.ModelSerializer):
    creator_username = serializers.CharField(source='creator.username', read_only=True)
    is_completed = serializers.SerializerMethodField()

    class Meta:
        model = Challenge
        fields = [
            'id', 'title', 'description', 'start_date', 'end_date',
            'target_books', 'created_at', 'creator', 'creator_username', 'book',
            'is_completed',
        ]
        read_only_fields = ['id', 'created_at', 'creator']

    def get_is_completed(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return ChallengeParticipant.objects.filter(challenge=obj, user=user, success=True).exists()
        return False

class ChallengeParticipantSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ChallengeParticipant
        fields = ['id', 'challenge', 'user', 'username', 'joined_at']
        read_only_fields = ['id', 'joined_at', 'user']


class ChallengeCommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = ChallengeComment
        fields = ['id', 'challenge', 'username', 'content', 'created_at']
        read_only_fields = ['id', 'created_at']


class BookQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookQuiz
        fields = ['id', 'book', 'question', 'choices', 'answer']


class QuizAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAttempt
        fields = ['id', 'challenge', 'user', 'score', 'submitted_at']
        read_only_fields = ['user', 'submitted_at']
