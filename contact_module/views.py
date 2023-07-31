from django.shortcuts import render, redirect
from django.urls import reverse

from site_module.models import SiteSetting
from .forms import ContactUsModelForm, ProfileForm
from django.views import View
from .models import ContactUs, UserProfile
from django.views.generic.edit import FormView, \
    CreateView  # from document u can see the others but important one is this
from django.views.generic import ListView


# class base view
class ContactUsView(FormView):  # instead of FormView we can use CreateView that don't need form class which
    # need model and directly get it from model and FormView is more completed and it must be formModel
    form_class = ContactUsModelForm
    template_name = 'contact_module/contact_us_page.html'
    success_url = '/contact-us/'

    # don't forget to use slash
    # the object_context default name is form

    def form_valid(self, form):
        form.save()  # it's gonna save the response of client
        return super().form_valid(form)  # it's gonna show it

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
        context['site_setting'] = setting
        return context


class CreateProfileView(FormView):
    template_name = 'contact_module/create_profile_page.html'
    form_class = ProfileForm
    success_url = '/contact-us/create-profile/'

    def form_valid(self, form):
        form.save()  # it's gonna save the response of client
        return super().form_valid(form)


class ProfileView(ListView):
    model = UserProfile
    template_name = 'contact_module/profiles_list_page.html'
    context_object_name = 'profiles'

    # def get(self, request):
    #     contact_form = ContactUsModelForm()
    #
    #     return render(request, 'contact_module/contact_us_page.html', {
    #         'contact_form': contact_form
    #     })
    #
    # def post(self, request):
    #     contact_form = ContactUsModelForm(request.POST)
    #     if contact_form.is_valid():
    #         contact_form.save()
    #         return redirect('home-page')
    #     else:
    #         return render(request, 'contact_module/contact_us_page.html', {
    #             'contact_form': contact_form
    #         })

#
# def store_file(file):
#     with open('temp/image.png', 'wb+') as dest:
#         for chunk in file.chunks():
#             dest.write(chunk)


# class CreateProfileView(View):
#     def get(self, request):
#         form_file = ProfileForm()
#
#         return render(request, 'contact_module/create_profile_page.html', {
#             'form_file': form_file
#         })
#
#     def post(self, request):
#         submited_form = ProfileForm(request.POST, request.FILES)
#         if submited_form.is_valid():
#             # store_file(request.FILES['profile'])
#             profile = UserProfile(image=request.FILES["image"])
#             profile.save()
#             return render(request, 'contact_module/create_profile_page.html')
#         return render(request, 'contact_module/create_profile_page.html', {
#             'form_file': submited_form
#         })


# def contact_us_page(request):
#     if request.method == 'POST':
#         # contact_form = ContactUsForm(request.POST)
#         contact_form = ContactUsModelForm(request.POST)
#         if contact_form.is_valid():  # it's going to check all the forms field are correct
#             contact = ContactUs(
#                 title=contact_form.cleaned_data.get('title'),
#                 full_name=contact_form.cleaned_data.get('full_name'),
#                 email=contact_form.cleaned_data.get('email'),
#                 message=contact_form.cleaned_data.get('message'),
#             )
#             contact.save()
#             contact_form.save()
#             return redirect('home-page')
#     else:
#         # contact_form = ContactUsForm()
#         contact_form = ContactUsModelForm()
#
#     return render(request, 'contact_module/contact_us_page.html', {
#         'contact_form': contact_form
#     })
