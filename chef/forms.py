from django import forms
from chef.models import Application


class ApplicationForm(forms.Form):
    # Only form field we need to generate is the text field
    text = forms.CharField(max_length=1000, widget=forms.Textarea)

    # Saves a new Application object with the cleaned data
    def save(self):
        data = self.cleaned_data
        app = Application(user=self.request.user, text=data["text"])
        return app.save()

