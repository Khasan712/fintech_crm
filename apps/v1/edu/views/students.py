from django.shortcuts import render

from apps.commons.decorators import isAuthenticated


# @isAuthenticated
def student_dashboard(request):
    return render(request, 'edu/dashboard.html')