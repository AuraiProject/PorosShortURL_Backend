from datetime import datetime, timedelta

from rest_framework import serializers


def validate_expired_time(value):
    if value:
        now = datetime.now()

        if datetime.timestamp(now) > value:
            raise serializers.ValidationError("The expired time must be greater than now.")
        elif datetime.timestamp(now + timedelta(days=50 * 365)) < value:
            raise serializers.ValidationError("The expired time must be less than 50 years.")


def validate_short_url_length(value):
    if value not in [3, 4, 5, 6, 7]:
        raise serializers.ValidationError("The digit of the short url must be one of 4, 5, 6, 7")


def validate_specify_short_url(value):
    if len(value) < 3 or len(value) > 7:
        raise serializers.ValidationError("Specify url’s length must be 4~7.")

    if not value.isalnum():
        raise serializers.ValidationError("Specify url can only have number and letter.")


class UrlSerializer(serializers.Serializer):
    url = serializers.URLField(max_length=255, required=True)
    short_url = serializers.CharField(max_length=255, required=False, validators=[validate_specify_short_url])
    created_timestamp = serializers.IntegerField(required=False)
    expired_timestamp = serializers.IntegerField(required=False, validators=[validate_expired_time])
    password = serializers.CharField(max_length=16, required=False)
    digit = serializers.IntegerField(required=False, validators=[validate_short_url_length])


class ShortUrlSerializer(serializers.Serializer):
    short_url = serializers.URLField(max_length=255, required=True)
