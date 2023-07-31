from django import forms

from account_module.models import User
from django.core import validators
from django.core.exceptions import ValidationError


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'avatar', 'address', 'about_user']

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'avatar': forms.FileInput(attrs={

            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '3',

            }),
            'about_user': forms.Textarea(attrs={
                'class': 'form-control',
                'row': '3'
            })
        }

        labels = {
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'avatar': 'تصویر پروفایل',
            'address': 'ادرس'
        }


class ChangePasswordForm(forms.Form):
    password = forms.CharField(
        label='کلمه عبور فعلی ',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        }),
        validators=[
            validators.MaxLengthValidator(100),
        ]

    )
    new_password = forms.CharField(
        label='کلمه عبور جدید',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    confirm_new_password = forms.CharField(
        label='تکرار کلمه عبور جدید',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    def clean_confirm_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        confirm_new_password = self.cleaned_data.get('confirm_new_password')

        if new_password == confirm_new_password:
            return confirm_new_password
        else:
            raise ValidationError('کلمه عبور و تکرار کلمه عبور مغایرت دارند', )
