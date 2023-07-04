
# todo:
# - `login/`: post-> get user tokens(Anonymous)

# - `register/`: post-> create user(Anonymous)

# - `users/`: get-> list of users(Admin only)

# - `users/<username>/`:
#       get-> detail user(Owner, Admin),
#       put-> edit details(Owner, Admin),
#       delete-> delete user(Owner, Admin)

from django.urls import path
from .views import create_user, delete_detail

urlpatterns = [
    path('register/', create_user),
    # path('users/', ),
    path('users/<str:username>/', delete_detail),
]
