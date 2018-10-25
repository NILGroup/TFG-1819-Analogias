from django.http import HttpResponse

import datetime
from django.shortcuts import render_to_response



def current_datetime(request):

    return render_to_response(request, '/templates/index.html', {})
