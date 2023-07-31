from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.views import View
from django.utils.crypto import get_random_string
from account_module.forms import RegisterForm, LoginForm, ResetPasswordFrom
from .models import User
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpRequest
from django.contrib.auth import login, logout
from .forms import ForgotPasswordForm
from utils.email_service import send_email


class RegisterView(View):

    def get(self, request):
        register_form = RegisterForm()
        context = {
            'register_form': register_form
        }
        return render(request, 'account_module/register.html', context)

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_email = register_form.cleaned_data.get('email')
            user_password = register_form.cleaned_data.get('password')
            user: bool = User.objects.filter(email__iexact=user_email).exists()
            if user:
                register_form.add_error('email', 'ایمیل وارد شده تکراری میباشد')
            else:
                new_user = User(email=user_email, email_active_code=get_random_string(72), is_active=False,
                                username=user_email)
                new_user.set_password(user_password)  # we use set_password because the password is encrypted
                new_user.save()
                send_email('فعال سازی حساب کاربری ', new_user.email, {'user': new_user}, 'emails/activate_account.html')
                return redirect(reverse('login_page'))  # instead of login page we can show him that u should activate
                # / ur account with ur email

        context = {
            'register_form': register_form
        }
        return render(request, 'account_module/register.html', context)


class ActivateAccountView(View):
    def get(self, request, email_active_code):  # because active_code will receive on url we write it in get method
        user: User = User.objects.filter(email_active_code__iexact=email_active_code).first()
        if user is not None:
            if not user.is_active:
                user.is_active = True
                user.email_active_code = (get_random_string(72))  # we do that so user can't active again when we
                # bane or
                # delete his account
                user.save()
                # todo: show success massage to user
                return redirect(reverse('login_page'))
            else:
                # todo: show your account was activated
                pass
        raise Http404

        #  with this package (django-ipware) we can get the client ip so force that to just he can try only 5-10 time
        #  activate his account after that it's like attack on a server


class LoginView(View):

    def get(self, request):
        login_form = LoginForm()
        context = {
            'login_form': login_form
        }
        return render(request, 'account_module/login.html', context)

    def post(self, request: HttpRequest):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_email = (login_form.cleaned_data.get('email'))
            user: User = User.objects.filter(email__iexact=user_email).first()
            user_pass = (login_form.cleaned_data.get('password'))
            if user is not None:
                if not user.is_active:
                    login_form.add_error('email', 'حساب کاربری شما فعال نشده است')
                else:
                    is_password_correct = user.check_password(user_pass)
                    if is_password_correct:
                        login(request, user)
                        return redirect(reverse('user_panel_dashboard'))
                    else:
                        login_form.add_error('email', 'نام کاربری یا کلمه عبور اشتباه است ')
            else:
                login_form.add_error('email', 'کاربری با مشخصات وارد شده یافت نشد')

        context = {
            'login_form': login_form
        }
        return render(request, 'account_module/login.html', context)


class ForgetPasswordView(View):
    def get(self, request: HttpRequest):
        forget_pass_form = ForgotPasswordForm()
        return render(request, 'account_module/forgot_passsword.html', {
            'forget_pass_form': forget_pass_form
        })

    def post(self, request: HttpRequest):
        forgot_password_form = ForgotPasswordForm(request.POST)
        if forgot_password_form.is_valid():
            user_email = forgot_password_form.cleaned_data.get('email')
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                send_email('فراموشی رمز عبور', user.email, {'user': user}, 'emails/forgotten_password.html')
                return redirect(reverse('home-page'))
            else:
                forgot_password_form.add_error('email', 'حساب کاربر ای با این ایمیل پیدا نشد')


class RessetPasswordView(View):  # because we send the active code with url so method is get
    def get(self, request: HttpRequest, active_code):
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()
        # when ever u send active_code to a client u should change it
        if user is None:
            return redirect(reverse('login_page'))

        reset_pass_form = ResetPasswordFrom()
        context = {
            'reset_pass_form': reset_pass_form,
            'user': user
        }
        return render(request, 'account_module/reset_password.html', context)

    def post(self, request: HttpRequest, active_code):
        reset_pass_form = ResetPasswordFrom(request.POST)
        if reset_pass_form.is_valid():
            user_new_pass = reset_pass_form.cleaned_data.get('password')
            user: User = User.objects.filter(email_active_code__iexact=active_code).first()
            if user is None:
                return redirect(reverse('login_page'))
            else:
                user.set_password(user_new_pass)
                user.email_active_code = get_random_string(72)
                user.is_active = True
                user.save()
                return redirect(reverse('login_page'))


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('login_page'))
