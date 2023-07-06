
# todo:
# - `login/`: post-> get user tokens(Anonymous)

# - `register/`: post-> create user(Anonymous)

# - `users/`: get-> list of users(Admin only)

# - `users/<username>/`:
#       get-> detail user(Owner, Admin),
#       put-> edit details(Owner, Admin),
#       delete-> delete user(Owner, Admin)

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import create_user, user_detail, login, user_list

urlpatterns = [
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/login/', login, name='login'),
    path('auth/register/', create_user, name='register'),

    path('users/', user_list, name='user-list'),
    path('users/<str:username>/', user_detail, name='user-detail'),
    
]
