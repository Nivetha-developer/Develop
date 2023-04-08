from rest_framework import serializers
from .models import AccountMaster, Destination

class AccountMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountMaster
        fields = '__all__'
        

class AccountSerializer(serializers.ModelSerializer):
    destination = serializers.SerializerMethodField('getdestination')

    def getdestination(self,data):
        destinationObj = Destination.objects.filter(account_id=data.account_id)
        serializedData = DestinationSerializer(destinationObj,many=True).data
        return serializedData
    
    class Meta:
        model = AccountMaster
        fields = '__all__'

class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = '__all__'
        