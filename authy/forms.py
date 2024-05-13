from django import forms
from authy.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class EditProfileForm(forms.ModelForm):
    image = forms.ImageField(required=True)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'First Name'}),
                                 required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Last Name'}),
                                required=True)
    bio = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Bio'}), required=True)

    class Meta:
        model = Profile
        fields = ['image', 'first_name', 'last_name', 'bio', 'url', 'location']


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'prompt srch_explore'}), max_length=50,
        required=True)
    # username = forms.EmailInput(widget=forms.TextInput(attrs={'placeholder': 'Username'}), max_length=50, required=True)

    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'prompt srch_explore'}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password', 'class': 'prompt srch_explore'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'prompt srch_explore'}))

    # email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


from django import forms
from authy.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm


class EditProfileForm(forms.ModelForm):
    image = forms.ImageField(required=True)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'First Name'}),
                                 required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Last Name'}),
                                required=True)
    bio = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Bio'}), required=True)

    class Meta:
        model = Profile
        fields = ['image', 'first_name', 'last_name', 'bio', 'url', 'location']


class OTPForm(forms.Form):
    otp_code = forms.CharField(label='OTP Code', max_length=6, widget=forms.TextInput(attrs={'class': 'form-control'}))


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'prompt srch_explore'}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password', 'class': 'prompt srch_explore'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'prompt srch_explore'}))



    class Meta:
        model = User
        # fields = ['username', 'email', 'password1', 'password2', 'otp_code']
        fields = ['username', 'email', 'password1', 'password2']


class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password1 = forms.CharField(max_length=100,
                                    widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password2 = forms.CharField(max_length=100,
                                    widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')
