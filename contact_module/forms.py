from django import forms
from django.core import validators
from django.core.exceptions import ValidationError

from .models import ContactUs, UserProfile


# class ContactUsForm(forms.Form):  # we could set required on False
#     full_name = forms.CharField(label='نام و نام خانوادگی',
#                                 max_length=50,
#                                 widget=forms.TextInput(attrs={
#                                     'class': 'form-control',
#                                     'placeholder': 'نام و نام خانوادگی'
#                                 }),
#                                 error_messages={'required': 'لطفا نام و نام خانوادگی را وارد کنید',
#                                                 'max_length': 'نام و نام خانوادگی نمی تواند بیشتر از 50 کارکتر باشد'})
#     email = forms.EmailField(label='ایمیل',
#                              max_length=50,
#                              widget=forms.EmailInput(attrs={
#                                  'class': 'form-control',
#                                  'placeholder': 'ایمیل'
#                              }),
#                              error_messages={'required': 'لطفاایمیل خود را وارد کنید'})
#     title = forms.CharField(label='موضوع',
#                             max_length=50,
#                             widget=forms.TextInput(attrs={
#                                 'class': 'form-control',
#                                 'placeholder': 'موضوع'
#                             }),
#                             error_messages={'required': 'لطفا موضوع خود را وارد کنید'})
#     message = forms.CharField(label='متن پیام',
#                               max_length=50,
#                               widget=forms.Textarea({
#                                   'class': 'form-control',
#                                   'placeholder': 'پیغام  شما',
#                                   'id': "message"
#                               }),
#                               error_messages={'required': 'لطفا متن پیام خود را وارد کنید'})


# upper class is not connected to model so it's hard to use instead we use this class in bottom

class ContactUsModelForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['email', 'full_name', 'title', 'message']

        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'email': forms.TextInput(
                attrs={
                'class': 'form-control'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'message': forms.TextInput(attrs={
                'class': 'form-control',
                'rows': '5',
                'id': 'message'
            }),
        }

        error_messages = {
            'full_name': {
                'required': 'لطفا نام و نام خانوادگی را وارد کنید'

            },
            'email': {
                'required': 'لطفاایمیل خود را وارد کنید'

            },
            'title': {
                'required': 'لطفا موضوع خود را وارد کنید'

            },
            'message': {
                'required': 'لطفا متن پیام خود را وارد کنید'

            }
        }
        # because this class connected to the Model, labels that given are the names from verbose_name in model
    #
    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     if '@' not in email or '.com' not in email:
    #         raise ValidationError('ایمیل معتبر وارد کنید')
    #     return email


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']

        error_messages = {
            'image': {
                'required': 'صثقثقصثقثصثصقصثق',
                'accept': 'بیسم یسسیب'
            }
        }
