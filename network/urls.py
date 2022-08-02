from django.urls import path, include
from requests import post

#from rest_framework import routers

from . import views
from .apis import views as post_views

# Define Router
# router = routers.DefaultRouter()

# Define the Router Path and Viewset to be used
# router.register(r'posts', PostViewset)

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:profile_id>", views.profile, name="profile"),
    path("following/<int:user_id>", views.following, name="following"),

    # API Routes
    path('posts/', post_views.PostListCreateAPIView.as_view(), name="api-post-list"),
    path('posts/<int:pk>', post_views.PostRetrieveUpdateDestroyAPIView.as_view(), name="api-post-details"),
    # path('api/', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls'))
]
