from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from api.models import UserProfile

User = get_user_model()

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    # Don't let people select ADMIN
    ROLE_CHOICES = [
        (UserProfile.Role.MANAGER, "Property Manager"), 
        # no tenants role, property managers would make a seeker into a tenant
        (UserProfile.Role.SEEKER,  "Seeker"),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")  # password field comes from UserCreationForm

    def save(self, commit=True):
        user = super().save(commit=commit)
        # ensure email stored
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        # create/update the profile with chosen role
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.role = self.cleaned_data["role"]
        profile.save()
        return user
