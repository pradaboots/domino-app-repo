from django.contrib import admin
from .models import (
    UserProfile, Property, PropertyImg, Unit, Amenity, PropertyAmenity,
    Listing, UnitImage, Lease
)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "phone")
    list_filter = ("role",)
    search_fields = ("user__username", "user__email", "phone")
    list_select_related = ("user",)
    list_per_page = 50

class PropertyImgInline(admin.TabularInline):
    model = PropertyImg
    extra = 1

class UnitInline(admin.TabularInline):
    model = Unit
    extra = 0
    fields = ("unit_label", "bedrooms", "bathrooms", "is_available", "rent_amount")
    show_change_link = True

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ("name", "property_type", "street_address", "post_code", "manager")
    list_filter = ("property_type",)
    search_fields = ("name", "street_address", "post_code", "manager__username", "manager__email")
    autocomplete_fields = ("manager",)
    inlines = [UnitInline, PropertyImgInline]
    list_select_related = ("manager",)
    ordering = ("name",)
    list_per_page = 50

class UnitImageInline(admin.TabularInline):
    model = UnitImage
    extra = 1

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ("property", "unit_label", "bedrooms", "bathrooms", "is_available", "rent_amount", "available_from")
    list_filter = ("is_available", "bedrooms", "bathrooms")
    search_fields = ("property__name", "unit_label")
    autocomplete_fields = ("property",)
    inlines = [UnitImageInline]
    list_select_related = ("property",)
    ordering = ("property__name", "unit_label")
    list_per_page = 50

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ("name", "icon")
    search_fields = ("name",)
    ordering = ("name",)

@admin.register(PropertyAmenity)
class PropertyAmenityAdmin(admin.ModelAdmin):
    list_display = ("property", "amenity", "is_active")
    list_filter = ("is_active",)
    search_fields = ("property__name", "amenity__name")
    autocomplete_fields = ("property", "amenity")
    list_select_related = ("property", "amenity")

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ("unit", "status", "promo_rent", "available_from", "created_at")
    list_filter = ("status",)
    search_fields = ("unit__property__name", "unit__unit_label")
    autocomplete_fields = ("unit",)
    list_select_related = ("unit", "unit__property")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 50

@admin.register(Lease)
class LeaseAdmin(admin.ModelAdmin):
    list_display = ("unit", "tenant", "status", "start_date", "end_date", "monthly_rent")
    list_filter = ("status",)
    search_fields = ("tenant__username", "tenant__email", "unit__property__name", "unit__unit_label")
    autocomplete_fields = ("unit", "tenant")
    list_select_related = ("tenant", "unit", "unit__property")
    date_hierarchy = "start_date"
    ordering = ("-start_date",)
    list_per_page = 50
