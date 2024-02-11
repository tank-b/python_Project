from django import forms
from .models import Sessions
from django.db import models

from django.forms import ModelForm


class SessionForm(ModelForm):

    class Meta :
        model = Sessions
        fields = ["date", "opening_hour", "closing_hour"]
        widgets = {
            "date": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            "opening_hour": forms.TimeInput(format="%H:%M", attrs={"type": "time"}),
            "closing_hour": forms.TimeInput(format="%H:%M", attrs={"type": "time"})

        }
        """
        opening_date = forms.DateField(
            label="Jour d'ouverture de sesssion",
            required=True,
            widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            input_formats=["%Y-%m-%d"]
        )

        opening_hour = forms.DateField(
            label="Heure d'ouverture de sesssion",
            required=True,
            widget=forms.TimeInput(format="%H:%M", attrs={"type": "time"}),
            input_formats=["%H:%M"]
        )

        closing_hour = forms.DateField(
            label="Heure de fermeture de session",
            required=True,
            widget=forms.TimeInput(format="%H:%M", attrs={"type": "time"}),
            input_formats=["%H:%M"]
        )
        exclude = ['id']
    """




