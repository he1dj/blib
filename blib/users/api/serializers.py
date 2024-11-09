from rest_framework import serializers

from blib.users.models import User


class UserSerializer(serializers.ModelSerializer[User]):
    
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=8, write_only=True, required=True)
    password2 = serializers.CharField(min_length=8, write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ["email", "password", "password2"]

    def validate(self, data):
        if data["password"]!= data["password2"]:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create_user(
            email=validated_data["email"],
        )
        user.set_password(password)
        user.save()
        return user
