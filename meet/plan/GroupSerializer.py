from rest_framework import serializers
from .models import Group


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = (
            "id",
            "plan",
            "user",
            "created_at",
        )

    def create(self, validated_data):
        group = Group.objects.create(**validated_data)
        return group

    def update(self, instance, validated_data):
        instance.plan = validated_data.get("plan", instance.plan)
        instance.user = validated_data.get("user", instance.user)
        instance.save()
        return instance
