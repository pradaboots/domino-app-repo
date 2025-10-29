from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model


# Create your models here.


"""Relaitonal Schema 
User(user_id, name, email, user_name, phone_number, password, role)
PropertyImg(property_id, img)
UnitImg(property_id, unit_id , img)
Property(property_id, manager_id (user_id), location, type)
Unit(property_id, unit_id, no_of_bedrooms, no_of_bathrooms, vacancy)
Listing(,property_id, description)
Lease(lease_id, unit_id, start_date, end_date, rent_amount)
Lease_Tenant(lease_id, user_id)
Account(acct_num, property_id, balance)
Invoice(invoice_id, lease_id, amount, due_date, issued_date)
Payment(paym_id, invoice_id, user_id, amount, payment_date)
Announcement(announce_no, property_id, content, date)
Viewing(viewing_id, property_id, user_id, time, rout_no, status, listing_id)
Maintenance(vendor, request_date, type, property_id, unit_id, user_id, status)
Package(barccode, user_id,)
Monthly_pnl(month_and_year, property_id, expenses, revenue, profit)
Message(message_id, sender_id (user_id1), receiver_id(user_id2), content, timestamp)
"""


"""django basic user model"""

User = get_user_model()

class UserProfile(models.Model):
    class Role(models.TextChoices):

        ADMIN = "ADMIN", "Admin"
        MANAGER = "MANAGER", "Property Manager"
        TENANT = "TENANT", "Tenant"
        SEEKER = "SEEKER", "Seeker"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.SEEKER)
    phone = models.CharField(max_length=20, blank=True, null=True)
    profile_image = models.ImageField(upload_to="profile_images/", blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} is a {self.role}"

"""relating to property, manager and other related """

class Property(models.Model):


    class PropertyType(models.TextChoices):
        HOUSE = "HOUSE", "House"
        APARTMENT = "APARTMENT", "Apartment"
        CONDO = "CONDO", "Condominium"
        TOWNHOUSE = "TOWNHOUSE", "Townhouse"
        DUPLEX = "DUPLEX", "Duplex"
        STUDIO = "STUDIO", "Studio"
        OFFICE = "OFFICE", "Office"
        OTHER = "OTHER", "Other"

    property_type = models.CharField(
        max_length = 20,
        choices=PropertyType.choices,
        default=PropertyType.APARTMENT,
        db_index=True
    )

    country = models.CharField(max_length=20, db_index=True)
    street_address = models.CharField(max_length=100, db_index=True)
    post_code = models.CharField(max_length=10, db_index=True)

    #basic marketing info
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=250)


    # NULL allows for change of management for a property 
    manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="properties",
        null=True,
        blank=True
    )

    #Many-To-Many USing through table 
    amenities = models.ManyToManyField(
        "Amenity",
        through="PropertyAmenity",
        related_name="properties",
        blank=True
    )

    def __str__(self):
        return f"{self.name} - {self.street_address} - managed by {self.manager}"

    
class PropertyImg(models.Model):

        property = models.ForeignKey(
            Property, 
            on_delete=models.CASCADE, 
            related_name="images"
        )

        img = models.ImageField(max_length=100,blank=False)




class Unit(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="units")

    unit_label = models.CharField(max_length=20, help_text="e.g., 3B or #12")  
    bedrooms   = models.PositiveSmallIntegerField()
    bathrooms  = models.PositiveSmallIntegerField()

    # marketing / inventory
    rent_amount       = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_available      = models.BooleanField(default=True)
    available_from    = models.DateField(null=True, blank=True)
    sqft              = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        constraints = [
            # one property can’t have two units with the same label
            models.UniqueConstraint(fields=["property", "unit_label"], name="uniq_unit_per_property")
        ]
        indexes = [
            models.Index(fields=["property", "is_available"]),
            models.Index(fields=["rent_amount"]),
        ]

    def __str__(self):
        return f"{self.property.name} – Unit {self.unit_label}"



class Amenity(models.Model):

    name = models.CharField(max_length=30,unique=True)
    icon = models.CharField(max_length=100,blank=True,null=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name



class PropertyAmenity(models.Model):

    property = models.ForeignKey(Property,on_delete=models.CASCADE)
    amenity = models.ForeignKey(Amenity,on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=["property", "amenity"], name="unique_property_amenity"
            )
        ]
        indexes = [
            models.Index(fields=["property", "amenity"]),
            models.Index(fields=["amenity"]),
        ]

    def __str__(self):
        return f"{self.property} - {self.amenity}"
    


class Listing(models.Model):

    class Status(models.TextChoices):
        DRAFT   = "DRAFT", "Draft"
        ACTIVE  = "ACTIVE", "Active"
        PAUSED  = "PAUSED", "Paused"
        CLOSED  = "CLOSED", "Closed"

    unit        = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="listings")
    title       = models.CharField(max_length=120, blank=True)
    description = models.TextField(blank=True)
    status      = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE, db_index=True)
    promo_rent  = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    available_from = models.DateField(null=True, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=["status", "created_at"])]

    def __str__(self):
        return f"Listing #{self.pk} – Unit {self.unit.unit_label} @ {self.unit.property.name}"


class UnitImage(models.Model):

    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(upload_to="unit_images/")
    caption = models.CharField(max_length=100, blank=True)
    is_feature = models.BooleanField(default=False)  # for main display image
    is_floor_plan = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=0)  

    class Meta:

        ordering = ["order"]  
        indexes = [
            models.Index(fields=["unit", "order"]),
        ]

    def __str__(self):
        return f"Image {self.order} for {self.unit}"
    

"""relating more to the tenants,leases and thier relationships """


class TenantUnit(models.Model):

    tenant = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    unit = models.ForeignKey(
        Unit,
        ron_delete=models.CASCADE,
    )

    
class Lease(models.Model):

    tenant = models.ForeignKey(
    User, 
    on_delete=models.SET_NULL,
    null=True,
    blank=True
    )

    start_date = models.DateField()
    end_date = models.DateField(null=True,blank=True)

