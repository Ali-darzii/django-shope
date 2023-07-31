import requests_toolbelt
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from django.views import View
from account_module.models import User
from django.contrib.auth import login, logout
from django.template.loader import render_to_string
from order_module.models import Order, OrderDetail
from user_panel_module.forms import EditProfileForm, ChangePasswordForm
from django.urls import reverse
from django.utils.decorators import method_decorator


# for big project for struct of that project we need to study the micro-service architecture and onion architecture

@method_decorator(login_required, name='dispatch')  # first function that will run is dispatch that its invisible
class UserPanelDashboardPage(TemplateView):
    template_name = 'user_panel_module/user_panel_dashboard_page.html'


@method_decorator(login_required, name='dispatch')
class EditUserPage(View):
    def get(self, request: HttpRequest, ):
        current_user = User.objects.filter(id=request.user.id, ).first()
        edit_form = EditProfileForm(instance=current_user)
        return render(request, 'user_panel_module/edit_profile_page.html', {
            'edit_form': edit_form,
            'user': current_user
        })

    def post(self, request: HttpRequest):
        current_user = User.objects.filter(id=request.user.id).first()
        edit_form = EditProfileForm(request.POST, request.FILES, instance=current_user)
        if edit_form.is_valid():
            edit_form.save(commit=True)
            return redirect(reverse('edit_user_page'))  # becouse we need to refresh the wole page to show the image
        return render(request, 'user_panel_module/edit_profile_page.html', {'edit_form': edit_form})


@method_decorator(login_required, name='dispatch')
class ChangPasswordPage(View):
    def get(self, request: HttpRequest):
        pass_form = ChangePasswordForm()
        context = {'pass_form': pass_form}
        return render(request, 'user_panel_module/change_password_page.html', context)

    def post(self, request: HttpRequest):
        pass_form = ChangePasswordForm(request.POST)
        if pass_form.is_valid():
            current_user: User = User.objects.filter(id=request.user.id).first()
            current_password = pass_form.cleaned_data.get('password')
            check_password = current_user.check_password(current_password)

            if check_password is True:
                confirm_new_password = pass_form.cleaned_data.get('confirm_new_password')
                current_user.set_password(confirm_new_password)
                current_user.save()
                logout(request)
                return redirect(reverse('login_page'))
            else:
                pass_form.add_error('password', 'کلمه عبور فعلی اشتباه است')

        context = {'pass_form': pass_form}
        return render(request, 'user_panel_module/change_password_page.html', context)


@login_required
def user_panel_menu_component(request: HttpRequest):
    return render(request, 'user_panel_module/components/user_panel_menu_component.html')


@login_required
def user_basket(request: HttpRequest):
    # context
    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                             user_id=request.user.id)
    total_amount = current_order.calculate_total_price()
    tax = int((total_amount * 9) / 100)
    final_total_amount = int(total_amount - tax)
    context = {
        'order': current_order,
        'sum': total_amount,
        'tax': tax,
        'final_sum': final_total_amount,
    }

    return render(request, 'user_panel_module/user_basket.html', context)


@login_required
def remove_order_detail(request: HttpRequest):
    # remove_basket
    detail_id = request.GET.get('detail_id')
    if detail_id is None:
        return JsonResponse({
            'status': 'not_found_detail_id'
        })

    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                             user_id=request.user.id)
    detail = current_order.orderdetail_set.filter(pk=detail_id, order__is_paid=False,
                                                  order__user_id=request.user.id).first()

    if detail is None:
        return JsonResponse({
            'status': 'detail_not_found'
        })
    else:
        detail.delete()

    total_amount = current_order.calculate_total_price()
    tax = int((total_amount * 9) / 100)
    final_total_amount = int(total_amount - tax)

    context = {
        'order': current_order,
        'sum': total_amount,
        'tax': tax,
        'final_sum': final_total_amount,
    }

    return JsonResponse({
        'status': 'success',
        'body': render_to_string('user_panel_module/user_basket_content.html', context)
    })


@login_required
def change_order_detail_count(request: HttpRequest):
    detail_id = request.GET.get('detail_id')
    state = request.GET.get('state')

    if detail_id is None or state is None:
        return JsonResponse({
            'status': 'not_found_detail_or_status'
        })
    order_detail = OrderDetail.objects.filter(pk=detail_id, order__user_id=request.user.id,
                                              order__is_paid=False).first()

    if order_detail is None:
        return JsonResponse({
            'status': 'Detail_not_found'
        })

    if state == 'increase':
        order_detail.count += 1
        order_detail.save()

    elif state == 'decrease':
        if order_detail.count == 1:
            order_detail.delete()
        else:
            order_detail.count -= 1
            order_detail.save()
    else:
        return JsonResponse({
            'status': 'state_invalid'
        })
    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                             user_id=request.user.id)
    total_amount = current_order.calculate_total_price()
    tax = int((total_amount * 9) / 100)
    final_total_amount = int(total_amount - tax)

    context = {
        'order': current_order,
        'sum': total_amount,
        'tax': tax,
        'final_sum': final_total_amount,
    }

    return JsonResponse({
        'status': 'success',
        'body': render_to_string('user_panel_module/user_basket_content.html', context)
    })


@method_decorator(login_required, name='dispatch')
class MySHopping(ListView):
    model = Order
    template_name = 'user_panel_module/user_shopping.html'
    context_object_name = 'orders'

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(is_paid=True, user_id=self.request.user.id)
        return query
