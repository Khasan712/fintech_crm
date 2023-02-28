import datetime
import random
import uuid
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from apps.commons.helper import code_decoder, generate_key
from apps.commons.views import send_register_code
from apps.v1.user.models import RegisterCode, User
from django.http import HttpResponse


def register(request, *args, **kwargs):
    data = request.POST
    phone_number = data.get('phone_number')
    code = data.get('code')
    session = request.session
    method = session.get('method')
    # if request.user.is_anonymous:
    #     return redirect("student_dashboard")
    if request.method == 'POST':
        if not method:
            user = User.objects.filter(phone_number=phone_number).first()
            if user:
                ctx = {'message': "Ro'yhatdan o'tgansiz!!!", 'class': 'danger'}
                return render(request, 'user/regis.html', ctx)
# """qo'wildi"""


            cod = random.randint(100000, 999999)

            # sms = send_register_code(phone_number, cod)
            # if sms.get('status') != "waiting":
            #     ctx = {'message': "sms xizmatida muammo!!!", 'class': 'danger'}
            #     return render(request, 'user/regis.html', ctx)
            root = RegisterCode()
            root.phone_number = phone_number
            root.code = code_decoder(str(generate_key(50)) + "$" + str(cod) + "$" + uuid.uuid4().__str__())
            root.save()

            session['method'] = 'enter_code'
            session['phone_number'] = phone_number
            session['token'] = root.code
            session['code'] = cod
            return redirect('user_register')

        if session.get('method') == 'enter_code':
            codes = RegisterCode.objects.filter(code=session['token']).first()
            if not codes:
                ctx = {'message': "OTP xato", 'class': 'danger'}
                return render(request, 'user/regis.html', ctx)

            codes.state = "step_two"
            codes.save()
            now = datetime.datetime.now(datetime.timezone.utc)
            cr = codes.created_at

            if codes.is_expired:
                del session['method']
                del session['phone_number']
                del session['token']
                return redirect('user_register')

            if (now - cr).total_seconds() > 180:
                codes.is_expired = True
                codes.save()
                ctx = {'message': "Kod eskirgan", 'class': 'danger'}
                return render(request, 'user/regis.html', ctx)

            otp_key = code_decoder(codes.code, decode=True)
            key = otp_key.split("$")[1]
            if str(key) != str(code):
                codes.tries += 1
                if codes.tries >= 3:
                    codes.is_expired = True

                codes.save()
                ctx = {'message': "Kod XATO", 'class': 'danger'}
                return render(request, 'user/regis.html', ctx)

            codes.state = "confirmed"
            codes.save()

            session['method'] = 'register'
            return redirect('user_register')

        if session.get('method') == 'register':
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            role = data.get('role')

            if data.get('password1') != data.get('password2'):
                ctx = {'message': "Parollar bir biriga mos emas", 'class': 'danger'}
                return render(request, 'user/regis.html', ctx)

            user = User.objects.create_user(
                phone_number=session['phone_number'],
                first_name=first_name,
                last_name=last_name,
                father_full_name=data.get('father_name'),
                father_phone=data.get('father_phone'),
                mother_full_name=data.get('mother_name'),
                mother_phone=data.get('mother_phone'),
                role=role,
                password=data.get('password1')
            )
            del session['method']
            del session['phone_number']
            del session['token']

            return redirect('user_login')
    else:
        return render(request, 'user/regis.html')


def user_login(request):
    if not request.user.is_anonymous:
        return redirect("student_dashboard")

    ctx = {}
    if request.POST:
        phone = request.POST.get('phone_number')
        password = request.POST.get('password')

        user = User.objects.filter(phone_number=phone).first()
        print(user)
        if not user:
            ctx = {'message': 'User not found', 'class': 'danger'}
            return render(request, 'user/login.html', ctx)
        if not user.check_password(password):
            ctx = {'message': 'Wrong password', 'class': 'danger'}
            return render(request, 'user/login.html', ctx)

        authenticate(request, user=user)
        login(request, user)
        return redirect('student_dashboard')

    return render(request, 'user/login.html', ctx)


def reset(request):
    session = request.session
    del session['method']
    del session['phone_number']
    del session['token']
    return redirect('user_register')


def user_logout(request):
    logout(request)
    return redirect("user_login")
