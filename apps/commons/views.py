import requests
from django.shortcuts import render, redirect
from dotenv import load_dotenv
import os
load_dotenv()




def send_register_code(phone_number, cod):

    token = os.getenv('token')

    url = "https://notify.eskiz.uz/api/message/sms/send"

    payload = {'mobile_phone': phone_number.split('+')[1],
               'message': f"sizning maxfiy codingiz {cod},Bu codeni hech kimga bermang",
               'from': '4546',
               'callback_url': 'http://0000.uz/test.php'}

    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()





