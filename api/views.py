from rest_framework import permissions
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Property, Unit, Listing
from .serializers import PropertySerializer, UnitSerializer, ListingSerializer

class PropertyViewSet(ReadOnlyModelViewSet):
    queryset = Property.objects.select_related("manager").all()
    serializer_class = PropertySerializer
    permission_classes = [permissions.AllowAny]

class UnitViewSet(ReadOnlyModelViewSet):
    queryset = Unit.objects.select_related("property").all()
    serializer_class = UnitSerializer
    permission_classes = [permissions.AllowAny]

class ListingViewSet(ReadOnlyModelViewSet):
    queryset = Listing.objects.select_related("unit", "unit__property").all()
    serializer_class = ListingSerializer
    permission_classes = [permissions.AllowAny]
