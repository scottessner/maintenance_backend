from rest_framework import serializers
from maintenance.models import Car, FillUp


class FillupSerializer(serializers.ModelSerializer):

    class Meta:
        model = FillUp
        fields = ('url', 'id', 'car', 'odometer', 'distance', 'price', 'quantity', 'datetime', 'economy')

    def create(self, validated_data):
        return FillUp.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.odometer = validated_data.get('odometer', instance.odometer)
        instance.distance = validated_data.get('distance', instance.distance)
        instance.price = validated_data.get('price', instance.price)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.datetime = validated_data.get('datetime', instance.datetime)
        instance.save()
        return instance


class CarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Car
        fields = ('url', 'id', 'make', 'model', 'nickname', 'year', 'average_economy', 'last_economy', 'last_updated')

    def create(self, validated_data):
        car = Car.objects.create(**validated_data)
        return car

    def update(self, instance, validated_data):
        instance.make = validated_data.get('make', instance.make)
        instance.model = validated_data.get('model', instance.model)
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.year = validated_data.get('year', instance.year)
        instance.save()
        return instance



