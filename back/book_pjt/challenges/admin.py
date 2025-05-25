from django.contrib import admin
from .models import Challenge, ChallengeParticipant, ChallengeComment


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'start_date', 'end_date', 'target_books')
    search_fields = ('title', 'creator__username')
    list_filter = ('start_date', 'end_date')


@admin.register(ChallengeParticipant)
class ChallengeParticipantAdmin(admin.ModelAdmin):
    list_display = ('challenge', 'user', 'joined_at')
    search_fields = ('challenge__title', 'user__username')
    list_filter = ('joined_at',)


@admin.register(ChallengeComment)
class ChallengeCommentAdmin(admin.ModelAdmin):
    list_display = ('challenge', 'user', 'created_at')
    search_fields = ('challenge__title', 'user__username', 'content')
    list_filter = ('created_at',)
