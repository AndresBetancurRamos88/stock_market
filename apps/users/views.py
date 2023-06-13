import secrets

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import UserSerializer


class Singup(APIView):
    serializer_class = UserSerializer

    def get_key(self):
        return secrets.token_hex(15)

    @extend_schema(
        responses={
            200: {
                "type": "object",
                "properties": {
                    "key": {
                        "type": "string",
                        "description": "Created"
                    }
                },
            },
            400: {
                "type": "object",
                "properties": {
                    "error": {"type": "string", "description": "Bad Request"}
                },
            },
        },
        summary="Signup user",
        description="Signup user and a key is generated that must \
            then be sent in the headers in market API request.",
    )
    def post(self, request):
        name = request.data.get("name")
        last_name = request.data.get("last_name")
        email = request.data.get("email")
        user_serializer = self.serializer_class(data=request.data)
        if user_serializer.is_valid():
            user = User.objects.create(
                name=name,
                last_name=last_name,
                email=email,
                key=self.get_key(),
            )
            return Response(user.key, status=status.HTTP_201_CREATED)
        return Response(
            user_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )
