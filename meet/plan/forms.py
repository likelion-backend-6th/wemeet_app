from django import forms
from .models import Plan


class PlanForm(forms.ModelForm):
    time = forms.DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M'],  # ISO 8601 형식에 맞춰진 입력 포맷
        widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local"
            },
            format='%Y-%m-%dT%H:%M'  # ISO 8601 형식에 맞춰진 출력 포맷
        )
    )
    class Meta:
        model = Plan
        fields = ["title", "time", "address", "memo"]
