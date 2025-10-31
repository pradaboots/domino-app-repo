from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PropertyViewSet, UnitViewSet, ListingViewSet

router = DefaultRouter()
router.register(r"properties", PropertyViewSet, basename="properties")
router.register(r"units", UnitViewSet, basename="units")
router.register(r"listings", ListingViewSet, basename="listings")

urlpatterns = [path("", include(router.urls))]
