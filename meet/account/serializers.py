from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    def validate_email(self, value):
        # 이메일이 중복되는지 확인
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("이미 등록된 이메일입니다.")
        return value
    class Meta:
        model = User
        fields = ['id', 'username', 'email',]
        read_only_field = ['is_active']
