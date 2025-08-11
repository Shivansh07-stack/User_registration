from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'msg': 'User registered successfully'})
        return Response(serializer.errors, status=400)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
            })
        return Response(serializer.errors, status=400)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        request.user.auth_token.delete()
        return Response({'msg': 'Logged out successfully'})

class EditUserView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Profile updated'})
        return Response(serializer.errors, status=400)
