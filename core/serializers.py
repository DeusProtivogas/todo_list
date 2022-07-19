import serializers as serializers
from django.contrib.auth.password_validation import validate_password


class CreateUserSerializer(serializers.ModelSerialzer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_repeat = serializers.CharField(write_only=True)

