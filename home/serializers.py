from rest_framework import serializers
from .models import Color, Person
from django.contrib.auth.models import User


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField()


    def validate(self, data):
        if data['username']:
            if User.objects.filter(username=data['username']).exists():
                raise serializers.ValidationError('username is taken ')
            
        if data['email']:
            if User.objects.filter(email=data['email']).exists():
                raise serializers.ValidationError('email is taken')
        
        return data


    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'], email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return validated_data
        print(validated_data)




class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()




class ColorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Color
        fields = ['color_name', 'id']


class PeopleSerializer(serializers.ModelSerializer):
      color = ColorSerializer()
      color_info = serializers.SerializerMethodField()

      class Meta:
         model = Person
         fields = '__all__'
         # depth = 1 # глубина рассширяет get  и показывает боьше инфы

      def get_color_info(self, obj):
         if obj.color is not None:
            return {'color_name': obj.color.color_name, 'hex_code': '#000'}
         else:
            return None

      def validate(self, data):
         special_simbol = '!@#$%^&*()_+-=<>?/\|'
         if any(c in special_simbol for c in data['name']):
             raise serializers.ValidationError('имя не должно содиржать символов')

         if data.get('age') and data['age'] < 18 :
             raise serializers.ValidationError('Возраст должен быть больше 18')
         return data