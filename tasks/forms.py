from django import forms

from .models import Todo


class TodoForm(forms.ModelForm):
    """ModelForm for creating and editing tasks (Activities 4 and 5)."""

    class Meta:
        model = Todo
        # Explicitly list fields; created_at is NOT here, so users can't edit it.
        fields = ["title", "description", "completed"]
        labels = {
            "title": "Title",
            "description": "Description (optional)",
            "completed": "Completed",
        }
        widgets = {
            "title": forms.TextInput(attrs={"maxlength": 150, "placeholder": "e.g. Buy groceries"}),
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def clean_title(self):
        # Server-side validation: reject empty / whitespace-only titles.
        # Django's CharField strips whitespace, so "   " becomes "" here.
        title = (self.cleaned_data.get("title") or "").strip()
        if not title:
            raise forms.ValidationError("Title cannot be empty or only spaces.")
        if len(title) > 150:
            raise forms.ValidationError("Title must be 150 characters or fewer.")
        return title
