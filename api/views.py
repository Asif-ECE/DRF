from rest_framework import viewsets, generics, permissions, status
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes  # , authentication_classes
# from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from api.models import Category, Product
from api.serializers import CategorySerializer, ProductSerializer, CustomUserSerializer, BlacklistedTokenSerializer


# @authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# @authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CustomUserRegistrationView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return Response({'user_id': user.id, 'tokens': tokens})


# this CustomTokenObtainPairView set's the refresh token as http-only
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh_token = response.data.get('refresh', None)

        if refresh_token:
            # HttpOnly cookie with the refresh token
            response.set_cookie('refresh_token', refresh_token,
                                httponly=True, samesite='None', secure=True)

        return response


class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh_token')

        if not refresh_token:
            return Response({'detail': 'refresh_token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh_token_instance = RefreshToken(refresh_token)
            refresh_token_instance.blacklist()

            blacklisted_token_data = {'token': refresh_token}
            blacklisted_token_serializer = BlacklistedTokenSerializer(
                data=blacklisted_token_data)
            if blacklisted_token_serializer.is_valid():
                blacklisted_token_serializer.save()
                return Response({'detail': 'Successfully logged out'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Unable to blacklist the token'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': f'Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
