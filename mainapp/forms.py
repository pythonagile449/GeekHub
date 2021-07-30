from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from martor.fields import MartorFormField

from mainapp.models import Hub, Article


class ArticleCkForm(forms.ModelForm):
    hub = forms.ModelChoiceField(label='Название хаба', widget=forms.Select(attrs={'class': 'select-3'}),
                                 empty_label='-- Выберите Хаб --', queryset=Hub.objects.all(), required=True)
    title = forms.CharField(label='Название статьи', widget=forms.TextInput(attrs={'class': 'editor-placeholder'}),
                            max_length=256, required=True)
    contents = forms.CharField(widget=CKEditorUploadingWidget(attrs={'style': 'width: auto'}))
    short_description = forms.CharField(label='Краткое описание',
                                        widget=forms.TextInput(attrs={'class': 'form-control'}),
                                        max_length=256, required=False)
    # article_sound = forms.ImageField(upload_to='media', label='Озвученная статья', widget=forms.FileInput(attrs={'class': '', 'required': False, }),
    #                                  required=False)

    class Meta:
        model = Article
        fields = [
            'hub',
            'title',
            'contents_ck',
            'contents_md',
            'short_description',
            'sound'
        ]


class ArticleMdForm(ArticleCkForm):
    contents = MartorFormField()
