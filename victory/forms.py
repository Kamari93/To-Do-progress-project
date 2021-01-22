from django.forms import ModelForm
from .models import Victory

class VictoryForm(ModelForm):
    class Meta:
        model = Victory
        fields = ['title', 'memo', 'important']