from django.shortcuts import render

def get_administrator_render(request, context):
    return render(request, 'edu/administrator/dashboard.html', context)