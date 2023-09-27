from rest_framework import serializers
from .models import Plan, Group


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = (
            "id",
            "owner",
            "title",
            "time",
            "latitude",
            "longitude",
            "memo",
            "created_at",
            "updated_at",
        )

    def create(self, validated_data):
        plan = Plan.objects.create(**validated_data)
        return plan

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.time = validated_data.get("time", instance.time)
        instance.latitude = validated_data.get("latitude", instance.latitude)
        instance.longitude = validated_data.get("longitude", instance.longitude)
        instance.memo = validated_data.get("memo", instance.memo)
        instance.save()
        return instance


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
