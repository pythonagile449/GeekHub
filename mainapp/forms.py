from django import forms
from martor.fields import MartorFormField
from mainapp.models import Hub, Article


class ArticleForm(forms.ModelForm):
    hub = forms.ModelChoiceField(widget=forms.Select, empty_label='----', queryset=Hub.objects.all(), required=True)
    title = forms.CharField(label='Название статьи', widget=forms.TextInput(attrs={'class': 'form-control'}),
                            max_length=256, required=True)
    # contents = forms.CharField(label='Текст статьи', widget=forms.Textarea(), required=True)
    contents = MartorFormField()
    short_description = forms.CharField(label='Краткое описание',
                                        widget=forms.TextInput(attrs={'class': 'form-control'}),
                                        max_length=256, required=True)

    class Meta:
        model = Article
        fields = [
            'hub',
            'title',
            'contents',
            'short_description',
        ]
