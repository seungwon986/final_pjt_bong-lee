from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User
from books.models import Category, Book

# ✅ 회원가입 시 사용자 추가 필드 입력
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

    class Meta:
        model = User
        fields = ['id', 'username', 'nickname', 'preferred_books']
