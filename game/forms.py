from django import forms
from django.core.exceptions import ValidationError
from .models import Post
from django.contrib.auth.models import Group
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from ckeditor_uploader.fields import RichTextUploadingFormField
'''class PostForm(forms.ModelForm):
    name = forms.CharField(label='Название')
    text = forms.CharField(label='содержание',min_length=20, widget = forms.Textarea)
    class Meta:
        model = Post
        fields = ['name', 'text','post_category', 'image']
    def clean(self):
        cleaned_data = super().clean()
        description = cleaned_data.get("text")
        name = cleaned_data.get("name")
        if name == description:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )

        return cleaned_data'''

class PostForm(forms.ModelForm):
    text = RichTextUploadingFormField(
    )
    class Meta:
        model = Post
        fields = ['name', 'text','post_category']
