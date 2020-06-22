#-*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.template.context_processors import csrf
import os,docker,uuid
from pythontest.settings import DOCKER_TMP
# Create your views here.
def index(request):
#    print(uuid.uuid1())
    request.session['session_id']=str(uuid.uuid1())
    return render(request,'index.html',csrf(request)) 
#    return HttpResponse("Hello, world. You're at the polls index.")
@ensure_csrf_cookie
def run_code(request):
    if 'session_id' in request.session:
        uuid_val=request.session['session_id']
        if not os.path.abspath(os.path.join(DOCKER_TMP,uuid_val))==DOCKER_TMP+'/'+uuid_val:
            return HttpResponse("uuid error")
        language=request.POST.get('language',None)
        code_content=request.POST.get('code_content',None)
        with open(DOCKER_TMP+'/'+uuid_val,'w') as wr_options:
            wr_options.write(code_content)
        client = docker.from_env()
        if language=='py2':
            try:
                container = client.containers.run(image='python:2.7.5',command='timeout 20 python '+'/tmp/'+uuid_val,remove=True,volumes={DOCKER_TMP+'/'+uuid_val:{'bind':'/tmp/'+uuid_val,'mode':'rw'}})
                return HttpResponse(str(container,encoding = "utf-8"))
            except Exception as except_result:
                return HttpResponse(except_result)
        elif language=='py3':
            try:
                container = client.containers.run(image='python:3.7.7',command='timeout 20 python '+'/tmp/'+uuid_val,remove=True,volumes={DOCKER_TMP+'/'+uuid_val:{'bind':'/tmp/'+uuid_val,'mode':'rw'}})
                return HttpResponse(str(container,encoding = "utf-8"))
            except Exception as except_result:
                return HttpResponse(except_result)
        elif language=='shell':
            try:
                container = client.containers.run(image='centos:7',command='timeout 20 /bin/sh '+'/tmp/'+uuid_val,remove=True,volumes={DOCKER_TMP+'/'+uuid_val:{'bind':'/tmp/'+uuid_val,'mode':'rw'}})
                return HttpResponse(str(container,encoding = "utf-8"))
            except Exception as except_result:
                return HttpResponse(except_result)
    return HttpResponse("success")
