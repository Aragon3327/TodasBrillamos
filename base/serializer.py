from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import serializers

from .models import Pedido,Pedido_Items

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['nombre'] = user.nombre
        token['email'] = user.email
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        pedidos = Pedido.objects.filter(cliente = self.user)

        datapedido = []

        for pedido in pedidos:
            items = Pedido_Items.objects.filter(pedido = pedido.id)
            dataitems = []
            for item in items:
                jsonItem = {
                    'producto':{
                        'id':item.item.id,
                        'nombre':item.item.nombre,
                        'imagen': item.item.imagen.url,
                        'precio': item.item.precio,
                    },
                    'cantidad': item.cantidad
                }
                dataitems.append(jsonItem)

            jsonpedido = {
                'estado': pedido.entregado,
                'items':dataitems,
                'total': pedido.total,
            }
            datapedido.append(jsonpedido)

        data.update({
            'user': {
                'nombre': self.user.nombre,
                'email': self.user.email,
                'direccion': self.user.direccion,
                'numero': self.user.phone_number,
                'edad':self.user.edad
            },
            'pedidos': datapedido
        })
        
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
