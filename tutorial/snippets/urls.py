from django.urls import path, include
from rest_framework.routers import DefaultRouter

from snippets import views


# Create a router and register our viewsets with it.
# The DefaultRouter class we're using also automatically creates the API root view.
router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet, basename="snippet")
router.register(r'users', views.UserViewSet, basename="user")

urlpatterns = [
    # Registering the viewsets with the router is similar to providing a urlpattern.
    path('', include(router.urls))
]
