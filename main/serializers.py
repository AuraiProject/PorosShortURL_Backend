from rest_framework import serializers


class UrlSerializer(serializers.Serializer):
    url = serializers.URLField(max_length=255, required=True)
    short_url = serializers.CharField(max_length=255, required=False)
    created_time = serializers.DateTimeField(required=False)
    expired_time = serializers.IntegerField(required=False)
    password = serializers.CharField(max_length=16, required=False)
    digit = serializers.IntegerField(required=False)


class ShortUrlSerializer(serializers.Serializer):
    short_url = serializers.URLField(max_length=255, required=True)
    password = serializers.CharField(max_length=16, required=False)
