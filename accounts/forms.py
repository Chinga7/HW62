from django.contrib.auth.forms import UserCreationForm
from django import forms


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label=("Email"),
        widget=forms.EmailInput(attrs={"autocomplete": "new-password"})
    )

    class Meta(UserCreationForm.Meta):
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email']

    def clean(self):
        cleaned_data = super().clean()
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')

        if not first_name and not last_name:
            raise forms.ValidationError(
                "Please Fill Out Either First Name Or Last Name")
        return cleaned_data
