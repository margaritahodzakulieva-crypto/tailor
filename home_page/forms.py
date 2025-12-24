from django import forms
from django.contrib.auth.models import User
from .models import Profile, Post

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image','about']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['about'].widget = forms.Textarea(attrs={'rows': 6, 'placeholder': 'Tell us about yourself...'})
        self.fields['image'].label = "Avatar"
        self.fields['about'].label = "About"


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_image','post_title','post_description','post_file',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['post_image'].label = "Post Image"
        self.fields['post_title'].label = forms.Textarea(attrs={'rows': 2, 'placeholder': 'Post Title...'})
        self.fields['post_description'].label = forms.Textarea(attrs={'rows': 5, 'placeholder': 'Post Description...'})
        self.fields['post_file'].label = "Post File"




class UserProfileForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        label="Username",
        help_text="Necessarily. Up to 150 characters. Only letters, numbers and @.+-_"
    )
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(max_length=30, required=False, label="Name")
    last_name = forms.CharField(max_length=30, required=False, label="Surname")

    class Meta:
        model = Profile
        fields = ['image', 'about']
        widgets = {
            'about': forms.Textarea(attrs={
                'rows': 6,
                'placeholder': 'Tell us about yourself'
            }),
        }
        labels = {
            'image': '',
            'about': 'About',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['image'].widget = forms.FileInput(attrs={'accept': 'image/*'})

        if self.instance.pk and self.instance.user:
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and username != self.instance.user.username:
            if User.objects.filter(username=username).exclude(pk=self.instance.user.pk).exists():
                raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if email != self.instance.user.email:
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("This email is already in use")
        return email

    def save(self, commit=True):
        profile = super().save(commit=False)

        user = profile.user
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
            profile.save()
        return profile