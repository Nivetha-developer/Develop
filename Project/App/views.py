# from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from App.models import * 
from App.serializers import *
from django.db import transaction
from rest_framework import status
import json
import requests
from django.views.decorators.csrf import csrf_exempt

"CRED operation for AccoutMaster and Destination"
class AccountDestinationAPI(APIView):

    def get(slef,request):
        try:
            """get all AccountMaster data"""
            AccountMasterObj = AccountMaster.objects.all()
            """If we want particular AccountMaster data send account id in params"""
            if "account_id" in request.query_params:
                account_id=request.query_params.get('account_id')
                if AccountMaster.objects.filter(account_id=account_id):
                    AccountMasterObj = AccountMaster.objects.filter(account_id=account_id)
                else:
                    return Response({"message":"Account details not found","success":False,"AccountMasters":[]},status=status.HTTP_400_BAD_REQUEST)
            """fetch serialized data"""
            result=AccountSerializer(AccountMasterObj,many=True).data
            return Response({"message":"Account details found","success":True,"AccountMasters":result},status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message":"There was a problem!","success":False,"AccountMasters":[]},status=status.HTTP_400_BAD_REQUEST)
    
    @transaction.atomic()
    def post(slef,request):
        try:
            data = request.data
           
            """check whether email is already exist"""
            if AccountMaster.objects.filter(email=data['email']):
                return Response({"message":"Email already exist","success":False},status=status.HTTP_409_CONFLICT)
            
            """creating AccountMaster entry on database"""
            newAccountMaster = AccountMaster.objects.create(email=data['email'],account_name = data['account_name'],website = data['website'])
            
            """Adding AccountMaster destination data in database"""
            for destination in data['destination_data']:
                url = destination['url']
                http_method = destination['http_method']
                headers = destination['headers']
                Destination.objects.create(account_id=newAccountMaster.account_id,url=url,http_method=http_method,headers=headers)

            return Response({"message":"Account created successfully","account_id":newAccountMaster.account_id,"success":True},status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            transaction.set_rollback(True)
            return Response({"message":"Account creation failed","success":False},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def put(slef,request):
        try:
            data = request.data
            account_id=data['account_id']
            if AccountMaster.objects.filter(email=data['email']).exclude(account_id=account_id):
                return Response({"message":"email already exist","success":False},status=status.HTTP_400_BAD_REQUEST)
            AccountMaster.objects.filter(account_id=account_id).update(email=data['email'],account_name = data['account_name'],website = data['website'])

            destinationArray = []
            for destination in data['destination_data']:
                if 'id' in destination:
                    id = destination['id']
                else:
                    id = None
                url = destination['url']
                http_method = destination['http_method']
                headers = destination['headers']
                destinationArray.append(id)
                if Destination.objects.filter(id=id,account_id=account_id):
                    """if id exist in table updating the data"""
                    Destination.objects.filter(id=id).update(url=url,http_method=http_method,headers=headers)
                else:
                    "if id none creating new data"
                    destination_obj = Destination.objects.create(account_id=account_id,url=url,http_method=http_method,headers=headers)
                    destinationArray.append(destination_obj.id)
            """If existing id not available in payload need to delete those data"""
            Destination.objects.filter(account_id=id).exclude(id__in=destinationArray).delete()
            return Response({"message":"Account updated successfully","success":True},status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message":"Account updation failed","success":True},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self,request):
        try:
            """checking require params in json"""
            json_vals=['account_id']
            for key in json_vals:
                for val in json_vals:
                    if (key not in dict.keys(request.data)) or (len(str(request.data[val])) == 0):
                        return Response({"message":"invalid body request","success":False}, status=status.HTTP_400_BAD_REQUEST)
            account_id = request.data['account_id']
            """check whether Account id exist or not if exist it goes to the if condition otherwise it goes to else part"""
            if AccountMaster.objects.filter(account_id=account_id):
                AccountMaster.objects.filter(account_id=account_id).delete()
                return Response({"message":"Account deleted successfully","success":True}, status=status.HTTP_200_OK)
            else:
                return Response({"message":"no Account found with this id","success":False}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message":"Account deletion failed","success":False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

"""CRED operation for AccoutMaster"""
class AccountAPI(APIView):

    def get(slef,request):
        try:
            """get all AccountMaster data"""
            AccountMasterObj = AccountMaster.objects.all()
            """If we want particular AccountMaster data send account id in params"""
            if "account_id" in request.query_params:
                account_id=request.query_params.get('account_id')
                if AccountMaster.objects.filter(account_id=account_id):
                    AccountMasterObj = AccountMaster.objects.filter(account_id=account_id)
                else:
                    return Response({"message":"Account details not found","success":False,"AccountMasters":[]},status=status.HTTP_400_BAD_REQUEST)
            """fetch serialized data"""
            result=AccountMasterSerializer(AccountMasterObj,many=True).data
            return Response({"message":"Account details found","success":True,"AccountMasters":result},status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message":"There was a problem!","success":False,"AccountMasters":[]},status=status.HTTP_400_BAD_REQUEST)
    
    @transaction.atomic()
    def post(slef,request):
        try:
            data = request.data
           
            """check whether email is already exist"""
            if AccountMaster.objects.filter(email=data['email']):
                return Response({"message":"Email already exist","success":False},status=status.HTTP_409_CONFLICT)
            
            """creating AccountMaster entry on database"""
            newAccountMaster = AccountMaster.objects.create(email=data['email'],account_name = data['account_name'],website = data['website'])
            return Response({"message":"Account created successfully","account_id":newAccountMaster.account_id,"success":True},status=status.HTTP_200_OK)
        except Exception as e:
            transaction.set_rollback(True)
            return Response({"message":"Account creation failed","success":False},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(slef,request):
        try:
            data = request.data
            account_id=data['account_id']
            if AccountMaster.objects.filter(email=data['email']).exclude(account_id=account_id):
                return Response({"message":"email already exist","success":False},status=status.HTTP_400_BAD_REQUEST)
            AccountMaster.objects.filter(account_id=account_id).update(email=data['email'],account_name = data['account_name'],website = data['website'])

            return Response({"message":"Account updated successfully","success":True},status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message":"Account updation failed","success":True},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
   
"""CRED operation for Destination"""
class DestinationAPI(APIView):

    def get(slef,request):
        try:
            if "account_id" in request.query_params:
                account_id=request.query_params.get('account_id')
                destinationObj = Destination.objects.filter(account_id=account_id)
            """If we want particular AccountMaster data send account id in params"""
            if "id" in request.query_params:
                id=request.query_params.get('id')
                if Destination.objects.filter(id=id):
                    destinationObj = Destination.objects.filter(id=id)
                else:
                    return Response({"message":"Account details not found","success":False,"AccountMasters":[]},status=status.HTTP_400_BAD_REQUEST)
            """fetch serialized data"""
            result=DestinationSerializer(destinationObj,many=True).data
            return Response({"message":"Account details found","success":True,"AccountMasters":result},status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message":"Please provide account id or destination id","success":False,"AccountMasters":[]},status=status.HTTP_400_BAD_REQUEST)
    
    @transaction.atomic()
    def post(slef,request):
        try:
            data = request.data
            account_id = data['account_id']
            """Adding AccountMaster destination data in database"""
            for destination in data['destination_data']:
                url = destination['url']
                http_method = destination['http_method']
                headers = destination['headers']
                s = Destination.objects.create(account_id=account_id,url=url,http_method=http_method,headers=headers)
            return Response({"message":"Destination created successfully","account_id":account_id,"success":True},status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            transaction.set_rollback(True)
            return Response({"message":"Destination creation failed","success":False},status=status.HTTP_500_INTERNAL_SERVER_ERROR)   

    def put(slef,request):
        try:
            data = request.data
            account_id = data['account_id']
            destinationArray = []
            for destination in data['destination_data']:
                if 'id' in destination:
                    id = destination['id']
                else:
                    id = None
                url = destination['url']
                http_method = destination['http_method']
                headers = destination['headers']
                destinationArray.append(id)
                if Destination.objects.filter(id=id,account_id=account_id):
                    """if id exist in table updating the data"""
                    Destination.objects.filter(id=id).update(url=url,http_method=http_method,headers=headers)
                else:
                    "if id none creating new data"
                    destination_obj = Destination.objects.create(account_id=account_id,url=url,http_method=http_method,headers=headers)
                    destinationArray.append(destination_obj.id)
            """If existing id not available in payload need to delete those data"""
            Destination.objects.filter(account_id=id).exclude(id__in=destinationArray).delete()
            return Response({"message":"Account updated successfully","success":True},status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message":"Account updation failed","success":True},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self,request):
        try:
            """checking require params in json"""
            json_vals=['id']
            for key in json_vals:
                for val in json_vals:
                    if (key not in dict.keys(request.data)) or (len(str(request.data[val])) == 0):
                        return Response({"message":"invalid body request","success":False}, status=status.HTTP_400_BAD_REQUEST)
            id = request.data['id']
            """check whether Account id exist or not if exist it goes to the if condition otherwise it goes to else part"""
            if Destination.objects.filter(id=id):
                Destination.objects.filter(id=id).delete()
                return Response({"message":"Account deleted successfully","success":True}, status=status.HTTP_200_OK)
            else:
                return Response({"message":"no Account found with this id","success":False}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message":"Account deletion failed","success":False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


