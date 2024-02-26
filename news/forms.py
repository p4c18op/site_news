from django import forms
from django.core.exceptions import ValidationError

from .models import New


class NewForm(forms.ModelForm):
    description = forms.CharField(min_length=20)

    class Meta:
        model = New
        fields = [
            'name',
            'description',
            'news',
        ]

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        description = cleaned_data.get("description")

        if name == description:
            raise ValidationError(
                "Текст не должен совпадать с заголовком!"
            )

        return cleaned_data