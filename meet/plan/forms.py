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
        fields = ["title", "category", "time", "address", "memo", "password"]

    def __init__(self, *args, **kwargs):
        super(PlanForm, self).__init__(*args, **kwargs)
        self.fields["title"].initial = ""
        self.fields["address"].initial = ""
        self.fields["memo"].initial = ""
        self.fields["password"].initial = ""


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["message"]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 2}),
        }


class PlanUpdateForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all())

    class Meta:
        model = Plan
        fields = ["title", "category", "memo", "password"]
