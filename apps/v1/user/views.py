from django.contrib import messages
from django.shortcuts import render, redirect
from apps.commons.views import send_register_code
from apps.v1.user.models import RegisterCode, User
from django.http import HttpResponse, HttpResponseRedirect


def register(request, *args, **kwargs):
    data = request.POST
    phone_number = data.get('phone_number')
    code = data.get('code')
    method = request.get('method')
    context = {
        'method': 'enter_phone'
    }
    if request.method == 'POST':
        if method == 'verify_code':
            return HttpResponseRedirect('method=verify_code')

    return render(request, 'user/register.html')

    # if request.method == 'POST':
    #     if not method:
    #         user = User.objects.filter(phone_number=phone_number).first()
    #         if user:
    #             messages.error(request, "Ro'yhatdan o'tgansiz!!!")
    #         send_register_code(phone_number)
    #         session['method'] = 'enter_code'
    #         session['phone_number'] = phone_number
    #         return redirect('user_register')
    #
    #
    #     if session.get('method') == 'enter_code':
    #         codes = RegisterCode.objects.filter(
    #             phone_number=session['phone_number'], code=code
    #         ).first()
    #         if not codes:
    #             messages.error(request, "Kod topilmadi")
    #         session['method'] = 'register'
    #         return redirect('user_register')
    #
    #
    #     if session.get('method') == 'register':
    #         first_name = data.get('first_name')
    #         last_name = data.get('last_name')
    #         role = data.get('role')
    #         print(session['phone_number'])
    #         user = User.objects.create(
    #             phone_number=session['phone_number'],
    #             first_name=first_name,
    #             last_name=last_name,
    #             role=role,
    #         )
    #         del session['method']
    #         del session['phone_number']
    #         return redirect('user_login')
    # if request.method == "GET":
    #     return render(request, 'user/register.html')


def login(request):
    return HttpResponse("Registered True")
