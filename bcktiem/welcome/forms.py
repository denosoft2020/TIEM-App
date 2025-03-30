from django import forms
from .models import Profile, Post

#form for profile page
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']

    def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')
        if picture:
            if picture.size > 2*1024*1024:  # 2MB limit
                raise forms.ValidationError("Image file too large (max 2MB)")
            return picture
        return None   

# Forms.py (Create an upload form)
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["caption", "video", "image"]

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']
        
    def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')
        if picture and picture.size > 2*1024*1024:  # 2MB limit
            raise forms.ValidationError("Image file too large ( > 2MB )")
        return picture