from rest_framework import serializers
from api.models import Pet, Photo

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('image',)  

class PetSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True, required=False) 

    class Meta:
        model = Pet
        fields = '__all__'
        read_only_fields = ('shelter',)

    def create(self, validated_data):
        photos_data = validated_data.pop('photos', [])
        pet = Pet.objects.create(**validated_data)
        for photo_data in photos_data:
            photo = Photo.objects.create(**photo_data) 
            pet.photos.add(photo)
        return pet

    def update(self, instance, validated_data):
        photos_data = validated_data.pop('photos', [])
        instance = super().update(instance, validated_data)
        if photos_data is not None:
            for photo_data in photos_data:
                instance.photos.clear()
                photo = Photo.objects.create(**photo_data)
                instance.photos.add(photo)
        return instance