import time
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from order_module.models import Order, OrderDetail
from product_module.models import Product
from django.conf import settings
import requests
import json


def add_product_to_order(request: HttpRequest):
    # we get the product_id and count with Jquery and we put it in Get request
    product_id = request.GET.get('product_id')
    count = int(request.GET.get('count'))

    # print(request.GET)
    # print(f"product id is {product_id} and count is {count}")
    if count < 1:
        return JsonResponse({
            'status': 'invalid_count'
        })
    elif request.user.is_authenticated:
        product = Product.objects.filter(pk=product_id, is_active=True, is_delete=False).first()
        if product is not None:
            # get current user open order
            # get or create response is 2 : order and bool
            current_order, created = Order.objects.get_or_create(user_id=request.user.id, is_paid=False)
            current_order_detail = current_order.orderdetail_set.filter(product_id=product_id).first()

            if current_order_detail is not None:

                current_order_detail.count += count
                current_order_detail.save()
                return JsonResponse({
                    'status': 'success'
                })
            else:
                new_detail: OrderDetail = OrderDetail(product_id=product_id, order_id=current_order.id, count=count)
                new_detail.save()
                return JsonResponse({
                    'status': 'success'
                })
            # add product to order
        else:
            return JsonResponse({
                'status': 'product_not_fount'
            })
    else:
        return JsonResponse({
            'status': 'not_auth'

        })


# ? sandbox merchant
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

amount = 1000  # Rial / Required
description = "نهایی کردن خرید شما از سایت ما"  # Required
phone = ''  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://127.0.0.1:8080/order/verify-payment/'


@login_required
def request_payment(request: HttpRequest):
    current_order, create = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
    total_price = current_order.calculate_total_price()
    if total_price == 0:
        return redirect(reverse('user_basket_page'))

    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": total_price * 10,
        "Description": description,
        # "Phone": phone,
        "CallbackURL": CallbackURL,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                return {'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']),
                        'authority': response['Authority']}
            else:
                return {'status': False, 'code': str(response['Status'])}
        return response

    except requests.exceptions.Timeout:
        return {'status': False, 'code': 'timeout'}
    except requests.exceptions.ConnectionError:
        return {'status': False, 'code': 'connection error'}

@login_required
def verify_payment(request: HttpRequest, authority):
    current_order, create = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
    total_price = current_order.calculate_total_price()

    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": total_price * 10,
        "Authority": authority,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    response = requests.post(ZP_API_VERIFY, data=data, headers=headers)

    if response.status_code == 200:
        response = response.json()
        if response['Status'] == 100:
            current_order.is_paid = True
            current_order.payment_date = time.time()
            current_order.save()
            # return {'status': True, 'RefID': response['RefID']}
            ref_str = str(response['RefID'])
            return render(request,'order_module/payment_result.html',{
                'success': f'تراکنش شما با کد پیگیری {ref_str} موفقیت انجام شد'
            })
        else:
            # return {'status': False, 'code':  str(response['Status'])}
            return render(request, 'order_module/payment_result.html', {
                'error': str(response['Status'])
            })
    return response
