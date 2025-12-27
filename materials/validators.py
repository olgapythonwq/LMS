from rest_framework import serializers


ALLOWED_DOMAINS = ['youtube.com', 'youtu.be']


def validate_video_link(value):
    if not value:  # Если value=None/пустая строка - не проверяется.
        return

    if not any(item in value for item in ALLOWED_DOMAINS):  # any(x in value for x in list)
        raise serializers.ValidationError("Only videos from youtube.com can be added.")
