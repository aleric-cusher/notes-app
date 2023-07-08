
# todo:
# - `login/`: post-> get user tokens(Anonymous)

# - `register/`: post-> create user(Anonymous)

# - `users/`: get-> list of users(Admin only)

# - `users/<username>/`:
#       get-> detail user(Owner, Admin),
#       put-> edit details(Owner, Admin),
#       delete-> delete user(Owner, Admin)

from django.urls import path
from rest_framework_simplejwt.views import TokenBlacklistView, TokenRefreshView
from .views import RegisterUser, CheckUsernameAvailiblity, LoginUser, UserDetailView

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register-user'),
    path('username-available/', CheckUsernameAvailiblity.as_view(), name='username-available'),

    path('login/', LoginUser.as_view(), name='login-user'),
    path('logout/', TokenBlacklistView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    path('profile/', UserDetailView.as_view(), name='user-profile'),

    # path('change-password/', , name='change-password')
    
]
