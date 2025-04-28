from datetime import datetime
from django.shortcuts import render

def Home(request):
    current_time = datetime.now().strftime('%H:%M')
    return render(request, 'Home.html', {'current_time': current_time})
