from django.http import JsonResponse
import requests
from django.views.decorators.csrf import csrf_exempt
from App.models import *
import json
from rest_framework.response import Response
from rest_framework import status

@csrf_exempt
def data_handler(request):
    """extract app secret token from request headers"""
    if 'CL-X-TOKEN' not in request.headers:
        return JsonResponse({"message":"Unauthorized","success":False})
    app_secret_token = request.headers['CL-X-TOKEN']

    """get account for the app secret token"""
    try:
        account = AccountMaster.objects.get(app_secret_token=app_secret_token)
    except AccountMaster.DoesNotExist:
        return JsonResponse({"message":"Invalid app secret token","success":False})

    """get destinations for the account"""
    destinations = Destination.objects.filter(account=account)
    """send data to destination"""
    body = request.body.decode('utf-8')
    data = json.loads(body)
    headers = {'Content-Type': 'application/json'}
    if request.method == 'GET':
        # send data as query parameters
        response = requests.get(f"http://127.0.0.1:8000/destination?account_id={data['account_id']}", headers=headers)
        return JsonResponse({"message":"Data sent to destinations successfully","success":True,'data':response.json()})
    elif request.method == 'POST':
        # send data as JSON in request body
        response = requests.post(f"http://127.0.0.1:8000/destination", headers=headers, data=json.dumps(data))
    elif request.method == 'PUT':
        # send data as JSON in request body
        response = requests.put("http://127.0.0.1:8000/destination", json=data, headers=headers)
    else:
        return JsonResponse({"message":"Invalid destination HTTP method","success":False})

    # check response status code
    if response.status_code >= 400:
        return JsonResponse({"message":"Failed to send data to destination","success":False})
    # return success response
    return JsonResponse({"message":"Data sent to destinations successfully","success":True})

