from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomLoginSerializer(TokenObtainPairSerializer):

    username_field = 'email'

    def validate(self, attrs):
        data = super().validate(attrs)

        user = self.user
        data['message'] = "Login Succesfull"
        
        data['user'] = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "role": user.role
        }

        return data