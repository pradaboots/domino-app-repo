from rest_framework import serializers
from .models import Property, Unit, Listing

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = [
            "id", "name", "description", "property_type",
            "country", "city", "state", "street_address", "post_code", "manager"
        ]

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = [
            "id", "property", "unit_label", "bedrooms", "bathrooms",
            "rent_amount", "is_available", "available_from", "sqft"
        ]

class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = [
            "id", "unit", "title", "description", "status",
            "promo_rent", "available_from", "created_at"
        ]
