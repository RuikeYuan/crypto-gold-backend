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
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.views.crypto_view import (
    UpdateDeleteGetCryptoViewSet, CryptoHistoryView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from app.views.medal_view import MetalViewSet
from app.views.transaction_view import TransactionView
from app.views.user_change_password_view import UserChangePasswordView
from app.views.user_view import UserRegistrationView, UserView, UserLoginView, UserTransactionView

router = DefaultRouter()
router.register(r'metals', MetalViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include('forum.urls')),  # Add this line to include the app's URL configuration
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    #http://127.0.0.1:8000/api/token/refresh/

    # {
    #     "refresh":
    #         "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczNTU3MDA4MSwiaWF0IjoxNzM1NDgzNjgxLCJqdGkiOiI1ODk3OWVkMzFjNTc0OTg2YjM5NTk3NzIxMTUzMTc5NyIsInVzZXJfaWQiOjF9.HKkJKREf07XLK_jIktpZOB1FBc8hs3AQF1yfwGZJ6wk"
    #
    # }
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    #http://127.0.0.1:8000/api/user/transactions/processing
    #http://127.0.0.1:8000/api/user/transactions/completed
    path('api/user/transactions/<str:status>/', UserTransactionView.as_view(), name='user_transactions'),
    #http://127.0.0.1:8000/api/user/login/
    # {
    #     "username": "testuser",
    #     "password": "testpassword123"
    # }
    path('api/user/login/', UserLoginView.as_view(), name='user-login'),
    #http://localhost:8000/change-password/
    # {
    #   "old_password": "testpassword123",
    #   "new_password": "new2Password123"
    # }
    path('change-password/', UserChangePasswordView.as_view(), name='change-password'),
    path('api/user/', UserView.as_view(), name='user-check'),
    # http://127.0.0.1:8000/api/user/
    # {
    #     "username": "testuser1",
    #     "email": "testuser1@example.com"
    # }
    path('api/register/', UserRegistrationView.as_view(), name='user-registration'),
    path('cryptos/', UpdateDeleteGetCryptoViewSet.as_view(), name='cryptos_list'),
    path('api/crypto-history/', CryptoHistoryView.as_view(), name='crypto-history'),
    # Endpoint to fetch and save historical data from the external API
    path('api/crypto-history/fetch/', CryptoHistoryView.fetch_from_api, name='fetch_crypto_data'),
    path('transaction/', TransactionView.as_view(), name='transaction'),
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
