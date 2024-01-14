from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import CategoryViewSet, ProductViewSet, CustomUserRegistrationView, LogoutView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')


urlpatterns = [
    path('', include(router.urls)),
    path('signup/', CustomUserRegistrationView.as_view(), name='signup'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('customtoken/', CustomTokenObtainPairView.as_view(), name='custom_token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token-verify'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
