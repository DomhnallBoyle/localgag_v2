from rest_framework import serializers
from localgag.models import Location as LocationModel, User as UserModel
from localgag.serializers import Location as LocationSerializer


class User(serializers.ModelSerializer):
    """
    Serializer to map the Model instance into JSON format.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    location = LocationSerializer(read_only=True)

    class Meta:
        """
        Meta class to map serializer's fields with the model fields.
        """
        model = UserModel
        fields = ('id', 'username', 'email', 'location', 'password')

    def create(self, validated_data):
        validated_data['location'] = LocationModel.objects.create()
        user = UserModel(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user

    def validate(self, data):
        """
        Check the password meets the following requirements:
            1: Must be > 8 characters long
            2: Contain both upper and lowercase alphabetic characters (e.g. A-Z, a-z)
            3: Have at least one numerical character (e.g. 0-9)
            4: Have at least one special character (e.g. ~!@#$%^&*()_-+=)
        """
        password = data.get('password')
        errors = []

        if len(password) < 8:
            errors.append('Password must be at least 8 characters long.')

        if not any(character.isupper() for character in password) or \
                not any(character.islower() for character in password):
            errors.append('Password must contain both uppercase and lowercase letters.')

        if not any(character.isdigit() for character in password):
            errors.append('Password must contain at least 1 numerical.')

        # if not any(special_char in password
        #            for special_char in ['~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-', '+', '=']):
        #     errors.append('Password must have at least 1 special character (e.g. ~!@#$%^&*()_-+=).')

        if len(errors) > 0:
            raise serializers.ValidationError({'password': errors})

        return data
