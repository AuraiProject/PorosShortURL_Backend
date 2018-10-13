from datetime import datetime, timedelta

from rest_framework import serializers


def validate_expired_time(value):
    if value:
        now = datetime.now()

        if datetime.timestamp(now) > value:
            raise serializers.ValidationError("The expired time must be greater than now.")
        elif datetime.timestamp(now + timedelta(days=50 * 365)) < value:
            raise serializers.ValidationError("The expired time must be less than 50 years.")


class UrlSerializer(serializers.Serializer):
    url = serializers.URLField(max_length=255, required=True)
    short_url = serializers.CharField(max_length=255, required=False)
    created_timestamp = serializers.IntegerField(required=False)
    expired_timestamp = serializers.IntegerField(required=False, validators=[validate_expired_time])
    password = serializers.CharField(max_length=16, required=False)
    digit = serializers.IntegerField(required=False)


class ShortUrlSerializer(serializers.Serializer):
    short_url = serializers.URLField(max_length=255, required=True)
    password = serializers.CharField(max_length=16, required=False)
