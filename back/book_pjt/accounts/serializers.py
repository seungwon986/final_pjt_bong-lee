from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User
from books.models import Category, Book
from django.contrib.auth import get_user_model

class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(max_length=30, required=False)
    last_name = serializers.CharField(max_length=30, required=False)
    gender = serializers.ChoiceField(choices=User.GENDER_CHOICES)
    birth = serializers.DateField(required=True)
    profile_image = serializers.ImageField(required=False)
    nickname = serializers.CharField(
        max_length=20,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="이미 사용 중인 닉네임입니다.")]
    )

    preferred_categories = serializers.ListField(
        child=serializers.IntegerField(), required=False
    )
    preferred_books = serializers.ListField(
        child=serializers.IntegerField(), required=False
    )

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data["first_name"] = self.validated_data.get("first_name")
        data["last_name"] = self.validated_data.get("last_name")
        data["gender"] = self.validated_data.get("gender")
        data["birth"] = self.validated_data.get("birth")
        data["profile_image"] = self.validated_data.get("profile_image")
        data["nickname"] = self.validated_data.get("nickname")
        data["preferred_categories"] = self.validated_data.get("preferred_categories", [])
        data["preferred_books"] = self.validated_data.get("preferred_books", [])
        return data

    def save(self, request):
        cleaned_data = self.get_cleaned_data()

        user = User.objects.create_user(
            username=cleaned_data.get("username"),
            email=cleaned_data.get("email"),
            password=cleaned_data.get("password1"),
            first_name=cleaned_data.get("first_name"),
            last_name=cleaned_data.get("last_name"),
            birth=cleaned_data.get("birth"),
            gender=cleaned_data.get("gender"),
            profile_image=cleaned_data.get("profile_image"),
            nickname=cleaned_data.get("nickname"),
        )

        if cleaned_data.get("preferred_categories"):
            user.preferred_categories.set(Category.objects.filter(id__in=cleaned_data["preferred_categories"]))

        if cleaned_data.get("preferred_books"):
            user.preferred_books.set(Book.objects.filter(id__in=cleaned_data["preferred_books"]))

        return user



class CustomUserSerializer(serializers.ModelSerializer):
    preferred_books = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Book.objects.all()
    )
    profile_image = serializers.ImageField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'nickname', 'profile_image', 'preferred_books', 'first_name', 'last_name']

class UserSerializer(serializers.ModelSerializer):
    completed_challenges_count = serializers.SerializerMethodField()
    joined_challenges_count = serializers.SerializerMethodField()
    created_challenges_count = serializers.SerializerMethodField()

    preferred_books = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True
    )

    class Meta:
        model = get_user_model()
        fields = [
            'id', 'username', 'nickname', 'email', 'profile_image',
            'preferred_books',
            'completed_challenges_count',
            'joined_challenges_count',
            'created_challenges_count',
        ]

    def get_completed_challenges_count(self, user):
        return user.challengeparticipant_set.filter(success=True).count()

    def get_joined_challenges_count(self, user):
        return user.challengeparticipant_set.count()

    def get_created_challenges_count(self, user):
        return user.created_challenges.count()