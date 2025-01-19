from .models import Data
from django import forms

class DataForm(forms.ModelForm):
    class Meta:
        model = Data
        fields = ("job_desc","resume_file")