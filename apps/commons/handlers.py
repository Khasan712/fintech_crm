from django.shortcuts import render

# Create your views here.


def error_500(request):
    return render(request, 'handlers/error-500.html')


def error_404(request, exception):
    return render(request, 'handlers/error-404.html')
