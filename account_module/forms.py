from django import forms
from django.core import validators
from django.core.exceptions import ValidationError

from .models import User


# class RegisterForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['email', 'password']
#
#         widgets = {
#             'email': forms.EmailField(
#
#
#             ),
#
#             'password': forms.PasswordInput(
#
#             )
#         }

# confirm_password = forms.CharField(
#     label='تکرار کلمه عبور',
#     # widget=forms.PasswordInput()
# )


class RegisterForm(forms.Form):
    email = forms.CharField(
        label='ایمیل',
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator(message='ایمیل معتبر نیست'),
        ],
        required=True,
        error_messages={'required': 'لطفا ایمیل معتبر وارد کنید'}

    )
    password = forms.CharField(
        label='کلمه رمز',
        widget=forms.PasswordInput(),
        validators=[
            validators.MaxLengthValidator(100),

        ]

    )
    confirm_password = forms.CharField(
        label='تکرار کلمه رمز',
        widget=forms.PasswordInput(),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     if '@' not in email or '.com' not in email:
    #         raise ValidationError('ایمیل معتبر وارد کنید')
    #     return email

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password == confirm_password:
            return confirm_password
        raise ValidationError('کلمه عبور و تکرار کلمه عبور مغایرت دارند')


class LoginForm(forms.Form):
    email = forms.CharField(
        label='ایمیل',
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator,
        ],
        required=True,
        error_messages={'required': 'لطفا ایمیل معتبر وارد کنید'}

    )
    password = forms.CharField(
        label='کلمه رمز',
        widget=forms.PasswordInput(),
        validators=[
            validators.MaxLengthValidator(100),
        ]

    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if '@' not in email or '.com' not in email:
            raise ValidationError('ایمیل معتبر وارد کنید')
        return email


class ForgotPasswordForm(forms.Form):
    email = forms.CharField(
        label='ایمیل',
        widget=forms.CharField(),
        validators=[
            validators.MaxLengthValidator(100),

        ],
        required=True,
        error_messages={'required': 'لطفا ایمیل معتبر وارد کنید'}

    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if '@' not in email or '.com' not in email:
            raise ValidationError('ایمیل معتبر وارد کنید')
        return email


class ResetPasswordFrom(forms.Form):
    password = forms.CharField(
        max_length=20,

        label='کلمه رمز',
        widget=forms.PasswordInput(),
        validators=[
            validators.MaxLengthValidator(100),
        ]

    )
    confirm_password = forms.CharField(
        label='تکرار کلمه رمز',
        widget=forms.PasswordInput(),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    def clean_confirm_reset_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password == confirm_password:
            return password
        raise ValidationError('رمز شما مطابقت ندارد')
