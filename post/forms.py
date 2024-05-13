from django import forms
from django.core.exceptions import ValidationError

from post.models import Post


class NewPostform(forms.ModelForm):
    picture = forms.FileField(required=True)
    caption = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Caption'}), required=True)
    tags = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Tags | Seperate with comma'}), required=True)

    class Meta:
        model = Post
        fields = ['picture', 'caption', 'tags']


    def clean_picture(self):
        picture = self.cleaned_data.get('picture')
        if picture:
            # Perform file extension validation here
            valid_extensions = ['jpg', 'jpeg', 'png', 'mp4', 'mkv']
            file_extension = picture.name.lower().split('.')[-1]
            if not any(ext in file_extension for ext in valid_extensions):
                raise ValidationError("Unsupported file extension. Please upload a .jpg, .jpeg, .png, .mp4, .mkv file.")
        return picture
