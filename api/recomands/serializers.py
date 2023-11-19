# myapp/serializers.py

from rest_framework import serializers
from recomands.models import UserNode, ItemNode

class UserNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNode
        fields = ['username']

class ItemNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemNode
        fields = ['name']

class CreateUserItemWithRatingSerializer(serializers.Serializer):
    user = UserNodeSerializer()
    item = ItemNodeSerializer()
    rating = serializers.FloatField()
