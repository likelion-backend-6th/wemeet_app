from django import forms
from .models import Plan, Comment, Category


class PlanForm(forms.ModelForm):
    time = forms.DateTimeField(
        input_formats=["%Y-%m-%dT%H:%M"],  # ISO 8601 형식에 맞춰진 입력 포맷
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local"},
            format="%Y-%m-%dT%H:%M",  # ISO 8601 형식에 맞춰진 출력 포맷
        ),
    )
    category = forms.ModelChoiceField(queryset=Category.objects.all())

    class Meta:
        model = Plan
        fields = ["title", "category" ,"time", "address", "memo", "password"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["message"]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 2}),
        }
