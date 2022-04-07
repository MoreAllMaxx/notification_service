from rest_framework import serializers

from .models import Dispatch, Message, Client, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', ]


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ['uid', 'phone', 'tags', 'timezone']


class DispatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dispatch
        fields = ['uid', 'text', 'notify_date_start', 'notify_date_end', 'tags', 'mobile_codes', 'should_send']

    def validate(self, data):
        if data['notify_date_start'] >= data['notify_date_end']:
            raise serializers.ValidationError("Дата начала рассылки не должна быть более даты окончания рассылки")
        return data


class MessageSerializer(serializers.ModelSerializer):
    status = serializers.ReadOnlyField()

    class Meta:
        model = Message
        fields = '__all__'
