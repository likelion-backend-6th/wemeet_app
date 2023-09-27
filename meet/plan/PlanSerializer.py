from rest_framework import serializers
from .models import Plan


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
