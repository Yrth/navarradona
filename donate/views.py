from django.shortcuts import render
from donate.models import *
from django.http import HttpResponse
def index(request):
    #context = {'latest_question_list': latest_question_list}
    return render(request, '../templates/landing_page.html')