from django import forms
from.models import Customer,Comment
from django.contrib.auth.forms import UserChangeForm,UserCreationForm,PasswordChangeForm
from django.utils.translation import ugettext_lazy as _
from django.core.files.images import get_image_dimensions

class CustomerCreationForm(UserCreationForm):
    class Meta:
        model=Customer
        fields="__all__"
    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']

        try:
            w, h = get_image_dimensions(avatar)

            # validate dimensions
            max_width = max_height = 100
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    u'Please use an image that is '
                    '%s x %s pixels or smaller.' % (max_width, max_height))

            # validate content type
            main, sub = avatar.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                raise forms.ValidationError(u'Please use a JPEG, '
                                            'GIF or PNG image.')

            # validate file size
            if len(avatar) > (20 * 1024):
                raise forms.ValidationError(
                    u'Avatar file size may not exceed 20k.')

        except AttributeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new avatar
            """
            pass

        return avatar



class EditProfileform(UserChangeForm):
    password = None
    class Meta:
        model=Customer
        fields=(
            'email',
            'first_name',
            'last_name',
            'phone_number',
        )


class ResetPassword(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','type':'password'}))
    new_password1 =forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','type':'password'}))
    new_password2 =forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','type':'password'}))
    class Meta:
        model=Customer
        fields=('old_password')

from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')