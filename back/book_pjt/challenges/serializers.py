from rest_framework import serializers
from .models import Challenge, ChallengeParticipant, ChallengeComment


class ChallengeSerializer(serializers.ModelSerializer):
    creator_username = serializers.CharField(source='creator.username', read_only=True)

    class Meta:
        model = Challenge
        fields = [
            'id', 'title', 'description', 'start_date', 'end_date',
            'target_books', 'created_at', 'creator', 'creator_username'
        ]
        read_only_fields = ['id', 'created_at', 'creator']


class ChallengeParticipantSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = ChallengeParticipant
        fields = ['id', 'challenge', 'user', 'username', 'joined_at']
        read_only_fields = ['id', 'joined_at']


class ChallengeCommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = ChallengeComment
        fields = ['id', 'challenge', 'username', 'content', 'created_at']
        read_only_fields = ['id', 'created_at']
