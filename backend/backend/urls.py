"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# filepath: /Users/ruikeyuan/Desktop/endpoints/backend/backend/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app import views
from app.views import (
    UserViewSet, MetalViewSet,
    TransactionViewSet, PostViewSet, 
    UserRegistrationView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
# router.register(r'crypto', CryptoViewSet)
router.register(r'metals', MetalViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'posts', PostViewSet)
# router.register(r'price-history', CryptoHistoryViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', UserRegistrationView.as_view(), name='user-registration'),
    path('crypto/<str:symbol>/', views.crypto_view, name='crypto_view')
]

# Available endpoints:
# GET /api/users/ - List all users
# POST /api/users/ - Create a user
# GET /api/users/{id}/ - Get user details
# GET /api/users/{id}/portfolio/ - Get user portfolio

# GET /api/crypto/ - List all cryptocurrencies
# GET /api/crypto/fetch_all/ - Fetch latest crypto data
# GET /api/crypto/{id}/ - Get specific crypto details

# GET /api/metals/ - List all metals
# GET /api/metals/fetch_all/ - Fetch latest metal prices
# GET /api/metals/{id}/ - Get specific metal details

# GET /api/transactions/ - List all transactions
# POST /api/transactions/ - Create a transaction
# GET /api/transactions/{id}/ - Get transaction details

# GET /api/posts/ - List all posts
# POST /api/posts/ - Create a post
# POST /api/posts/{id}/add_reply/ - Add reply to a post

# GET /api/price-history/ - List price history
# GET /api/price-history/{id}/fetch_history/ - Fetch price history for an asset
