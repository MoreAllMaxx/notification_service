from rest_framework import viewsets

from .models import Dispatch, Message, Client, MobileOperatorCode, Tag
from .serializers import DispatchSerializer, MessageSerializer, ClientSerializer, TagSerializer


class TagAPIViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class DispatchAPIViewSet(viewsets.ModelViewSet):
    queryset = Dispatch.objects.all()
    serializer_class = DispatchSerializer


class MessageAPIViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class ClientAPIViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def perform_create(self, serializer):
        mobile_operator_code = str(serializer.validated_data.get('phone'))[1:4]
        mobile_operator_code = int(mobile_operator_code)
        if mobile_operator_code not in [obj.code for obj in MobileOperatorCode.objects.filter()]:
            new_obj = MobileOperatorCode.objects.create(code=mobile_operator_code)
            new_obj.save()
            serializer.save(mobile_operator_code=new_obj)
        else:
            serializer.save(mobile_operator_code=MobileOperatorCode.objects.get(code=mobile_operator_code))
