
# Frontend
# Funciones de vista
# Docs: https://docs.djangoproject.com/en/5.1/topics/http/views/

from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm, ItemForm, CategoriasForm
from django.contrib.auth import logout,authenticate,login
from django.contrib.auth.decorators import login_required
from .models import Item,Pedido,Categoria,Usuario,Pedido_Items
from django.http import HttpResponseRedirect,JsonResponse

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework import status

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
def logoutView(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):

    return render(request,'index.html')

@login_required
def productosView(request):
    items = Item.objects.all()
    context = {
        'items': Item.objects.all(),
        'categorias':Categoria.objects.all()
    }
    
    return render(request,'productos.html',context)

# Pedidos
@login_required
def pedidosView(request):
    context = {
        'pedidos':Pedido.objects.all()
    }
    return render(request, 'pedidos.html', context)

@login_required
def pedidosCambio(request,pk):
    pedido = Pedido.objects.get(id = pk)
    pedido.entregado = not pedido.entregado
    pedido.save()
    return redirect('pedidos')

@login_required
def pedidosExtendView(request,pk):
    context = {
        'pedido': Pedido.objects.get(id = pk)
    }
    return render(request,'pedidosExtend.html', context)
# Categorias
@login_required
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
def BorrarCategoria(request,pk):
    get_object_or_404(Categoria,id = pk).delete()
    return redirect('productos')

# ITEMS
@login_required
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

# APPJSON
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ListadoItems(request):

    print(request.headers)

    items = Item.objects.all()

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
        'edad': user.edad
    }
    print(json)

    return JsonResponse(json, safe=False)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def pedidosPasados(request):
    user = request.user
    pedidos = Pedido.objects.filter(cliente=user)
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
            'estado': pedido.entregado,
            'items':dataitems,
            'total': pedido.total,
        }
        data.append(jsonpedido)
    return JsonResponse(data,safe=False)

@api_view(['POST'])
def register_user(request):
    nombre = request.data.get('nombre')
    direccion = request.data.get('direccion')
    edad = request.data.get('edad')
    email = request.data.get('email')
    password = request.data.get('contrasena')
    genero = request.data.get('genero')

    if Usuario.objects.filter(email=email).exists():
        return Response('Ya existe una cuenta con el correo', status=status.HTTP_400_BAD_REQUEST)
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

@login_required
def BorrarItem(request,pk):
    get_object_or_404(Item,id = pk).delete()
    return redirect('productos')
