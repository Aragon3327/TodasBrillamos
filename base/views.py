
# Frontend
# Funciones de vista
# Docs: https://docs.djangoproject.com/en/5.1/topics/http/views/

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout,authenticate,login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,JsonResponse,HttpResponse
from django.core import serializers
from .forms import LoginForm, ItemForm, CategoriasForm,RegistroForm,EditarPerfilForm
from .models import Item,Pedido,Categoria,Usuario,Pedido_Items,Donacion
from .decorators import admin_required

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework import status

from datetime import datetime
from calendar import monthrange
import json
import stripe

# VIEWS
def loginView(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect("/")
    else:
        form = LoginForm()
    return render(request,'login.html',{'form':form})

@login_required
def registroAdmin(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.es_admin = True
            user.super_user = True
            user.save()
            return redirect('/')
    else:
        form = RegistroForm()
    return render(request,'registroAdmin.html',{'form':form})

@login_required
def logoutView(request):
    logout(request)
    return redirect('login')

@login_required
@admin_required
def datosGraficas(request):
    actual = datetime.now()

    pedidos_totales = Pedido.objects.filter(fecha__year=actual.year, fecha__month=actual.month)

    dias_del_mes = actual.day
    pedidos_fecha_pagados = [0] * dias_del_mes
    pedidos_fecha_no_pagados = [0] * dias_del_mes
    pedidosEnviados = 0
    pedidoNoEnviados = 0

    for pedido in pedidos_totales:
        dia = pedido.fecha.day - 1

        if pedido.enviado: pedidosEnviados+=1 
        else: pedidoNoEnviados+=1

        if pedido.pagado:
            pedidos_fecha_pagados[dia] += 1
        else:
            pedidos_fecha_no_pagados[dia] += 1

    pedidos_pagados_no_pagados = [
        sum(pedidos_fecha_pagados),
        sum(pedidos_fecha_no_pagados),
    ]

    context = {
        "pedidosTotalesPagados": pedidos_fecha_pagados,
        "pedidosTotalesNoPagados": pedidos_fecha_no_pagados,
        "pedidosPagadosyNoPagados": pedidos_pagados_no_pagados,
        "pedidosEnviadosyNoEnviados":[pedidosEnviados,pedidoNoEnviados]
    }
    return JsonResponse(context)


@login_required
@admin_required
def dashboard(request):

    donadores = Donacion.objects.all()

    context = {
        'donadores':donadores
    }

    return render(request, 'index.html',context)


@login_required
@admin_required
def productosView(request):
    items = Item.objects.all()
    context = {
        'items': Item.objects.all(),
        'categorias':Categoria.objects.all()
    }
    
    return render(request,'productos.html',context)

# Pedidos
@login_required
@admin_required
def pedidosView(request):
    context = {
        'pedidos':Pedido.objects.all().order_by('-fecha')
    }
    return render(request, 'pedidos.html', context)

@login_required
@admin_required
def pedidosCambio(request,pk):
    pedido = Pedido.objects.get(id = pk)
    pedido.enviado = not pedido.enviado
    pedido.save()
    return redirect('pedidos')

@login_required
@admin_required
def pedidosCambioPago(request,pk):
    pedido = Pedido.objects.get(id = pk)
    pedido.pagado = not pedido.pagado
    pedido.save()
    return redirect('pedidos')

@login_required
@admin_required
def pedidosExtendView(request,pk):
    context = {
        'pedido': Pedido.objects.get(id = pk),
        'items': Pedido_Items.objects.filter(pedido = pk)
    }
    return render(request,'pedidosExtend.html', context)

# Categorias
@login_required
@admin_required
def RegistroCategoria(request):
    if request.method == 'POST':
        form = CategoriasForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = CategoriasForm()
    return render(request,'registroItem.html',{'form':form})

@login_required
@admin_required
def BorrarCategoria(request,pk):
    get_object_or_404(Categoria,id = pk).delete()
    return redirect('productos')

# ITEMS
@login_required
@admin_required
def RegistroItem(request):
    form = ItemForm(prefix='form')
    form2 = CategoriasForm(prefix='form2')
    if request.method == 'POST':
        if 'submit_form1' in request.POST:
            form = ItemForm(request.POST,prefix='form')
            form2 = CategoriasForm(prefix='form2')
            if form.is_valid():
                form.save()
                return redirect('productos')
        elif 'submit_form2' in request.POST:
            form = ItemForm(prefix='form')
            form2 = CategoriasForm(request.POST, prefix='form2')
            if form2.is_valid():
                form2.save()
                return HttpResponseRedirect(request.get_full_path())
    return render(request,'registroItem.html',{
        'form':form,
        'form2':form2
        })

@login_required
@admin_required
def EditarItem(request,pk):
    itemEditado = Item.objects.get(id=pk)
    form = ItemForm(prefix='form',instance=itemEditado)
    form2 = CategoriasForm(prefix='form2')
    descuentoPrePOST = itemEditado.descuento
    if request.method == 'POST':
        if 'submit_form1' in request.POST:
            form = ItemForm(request.POST,request.FILES,prefix='form',instance=itemEditado)
            form2 = CategoriasForm(prefix='form2')
            if form.is_valid():
                if form.cleaned_data['descuento']:
                    precio = form.cleaned_data['precio']
                    descuento = form.cleaned_data['descuento']
                    precio_Descuento = precio - (precio * (descuento/100))
                    itemEditado.precio = precio_Descuento
                elif(descuentoPrePOST):
                    precio = itemEditado.precio
                    print(f'Descuento: {type(descuentoPrePOST)}, precio = {precio}')
                    precio = precio / (1-(descuentoPrePOST/100))
                    print(precio)
                    itemEditado.precio = precio
                form.save()
                return redirect('productos')
        elif 'submit_form2' in request.POST:
            form = ItemForm(prefix='form',instance=itemEditado)
            form2 = CategoriasForm(request.POST, request.FILES,prefix='form2')
            if form2.is_valid():
                form2.save()
                return redirect('editar_item', pk=pk)
    return render(request,'registroItem.html',{
        'form':form,
        'form2':form2
        })

@login_required
@admin_required
def BorrarItem(request,pk):
    get_object_or_404(Item,id = pk).delete()
    return redirect('productos')

# APP POST's & GET's
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def EditarPerfil(request):
    user = request.user

    form = EditarPerfilForm(data=request.data, instance=user)

    if form.is_valid():
        password = request.data.get('contrasena')
        if password:
            user.set_password(password)
        form.save()
        return Response(status=status.HTTP_200_OK)
    else:
        print(form.errors)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ListadoItems(request):

    items = Item.objects.filter(stock__gt=0)

    data = []

    for item in items:
        json = {
            'id':item.id,
            'nombre':item.nombre,
            'stock':item.stock,
            'precio':item.precio,
            'descuento':item.descuento,
            'descripcion':item.descripcion,
            'categoria':item.categoria.nombre,
            'imagen':item.imagen.url if item.imagen else None
        }
        data.append(json)

    return JsonResponse(data,safe=False)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ItemJSON(request,id):
    item = Item.objects.get(id = id)
    json = {
        'id':item.id,
        'nombre':item.nombre,
        'stock':item.stock,
        'precio':item.precio,
        'descuento':item.descuento,
        'descripcion':item.descripcion,
        'categoria':item.categoria.nombre,
        'imagen':item.imagen.url if item.imagen else None
    }

    return JsonResponse(json,safe=False)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def InfoUser(request):

    user = request.user

    json = {
        'nombre': user.nombre,
        'email': user.email,
        'direccion': user.direccion,
        'numero': user.phone_number,
        'edad': user.edad,
    }

    return JsonResponse(json, safe=False)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def categoriasJSON(request):
    categorias = Categoria.objects.all()

    lista = []

    for categoria in categorias:
        json = {
            'nombre':categoria.nombre
        }
        lista.append(json)

    return JsonResponse(lista,safe=False)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def pedidosPasados(request):
    user = request.user
    pedidos = Pedido.objects.filter(cliente=user).order_by('-fecha')
    data = []
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
            'fecha':pedido.fecha,
            'estado': pedido.enviado,
            'items':dataitems,
            'total': pedido.total,
        }
        data.append(jsonpedido)
    return JsonResponse(data,safe=False)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    nombre = request.data.get('nombre')
    direccion = request.data.get('direccion')
    edad = request.data.get('edad')
    email = request.data.get('email')
    password = request.data.get('contrasena')
    genero = request.data.get('genero')

    if Usuario.objects.filter(email=email).exists():
        return Response('Ya existe una cuenta con el correo', status=status.HTTP_400_BAD_REQUEST)
    else:
        user = Usuario.objects.create_user(
            nombre=nombre,
            direccion = direccion,
            edad = edad,
            email=email,
            password=password,
            genero = genero)
        if user:
            Token.objects.get_or_create(user=user)
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def crearDonacion(request):
    datos = request.data
    usuario = request.user
    donacion = Donacion.objects.create(cliente = usuario,cantidad = datos['cantidad'],curp = datos['curp'])

    if donacion:
        donacion.save()
        return JsonResponse({"message":"Donación Creada"},status.HTTP_201_CREATED)
    else:
        return JsonResponse({"error":"Error en datos"},status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def crearPedido(request):
    datos = request.data
    user = request.user
    pedido = Pedido.objects.create(cliente=user, total=0.0)
    total_pedido = 0.0

    for item_data in datos:
        try:
            
            item = Item.objects.get(id=item_data['producto']['id'])
            cantidad = item_data.get('cantidad', 1)

            Pedido_Items.objects.create(pedido=pedido, item=item, cantidad=cantidad)

            total_item = item.precio * cantidad
            total_pedido += total_item

            item.stock -= cantidad
            item.save()
            
        except Item.DoesNotExist:
            return Response({"error": f"El item con id {item_data['id']} no existe."}, status=status.HTTP_404_NOT_FOUND)

    pedido.total = total_pedido
    pedido.save()

    return Response({"message": "Pedido creado con éxito", "pedido_id": pedido.id}, status=status.HTTP_201_CREATED)

stripe.api_key = 'sk_test_51QAhEw2K799XBlDvmeJDmugblwa16EaPE4SVLo6zWJGUNHNR0ekJ794wXHvhrEIjMgQtjZkHSA9TUPO7mxvb7Npy002OrMhkat'
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def paymentsheet(request):

    customer = stripe.Customer.create()
    ephemeralKey = stripe.EphemeralKey.create(
    customer=customer['id'],
    stripe_version='2024-09-30.acacia',
    )
    paymentIntent = stripe.PaymentIntent.create(
        amount=request.body,
        currency='mxn',
        customer=customer['id'],
        automatic_payment_methods={
          'enabled': True,
        },
    )
    return JsonResponse({
        'paymentIntent':paymentIntent.client_secret,
        'ephemeralKey':ephemeralKey.secret,
        'customer':customer.id,
        'publishableKey':'pk_test_51QAhEw2K799XBlDvFa90HJL1N9TF96Zc2Lxhap0t3xqORw2E4qwmADNVoIO9O9o4ED775BGs8DamhEnriVxpor5m00fd7MTDQk'
    })
