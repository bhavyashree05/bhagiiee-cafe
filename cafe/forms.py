from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=False)

    class Meta:
        model = User
        fields = ["username", "email", "phone_number", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            Profile.objects.create(
                user=user, phone_number=self.cleaned_data.get("phone_number", "")
            )
        return user


class OrderQuantityForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1)


class PaymentForm(forms.Form):
    amount_paid = forms.DecimalField(max_digits=8, decimal_places=2, min_value=0)
