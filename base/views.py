
# Frontend
# Funciones de vista
# Docs: https://docs.djangoproject.com/en/5.1/topics/http/views/

from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm, ItemForm, CategoriasForm
from django.contrib.auth import logout,authenticate,login
from .models import Item,Pedido,Categoria
from django.http import HttpResponseRedirect

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

def logoutView(request):
    logout(request)
    return redirect('login')

def dashboard(request):

    return render(request,'index.html')

def productosView(request):
    items = Item.objects.all()
    context = {
        'items': Item.objects.all(),
        'categorias':Categoria.objects.all()
    }
    
    return render(request,'productos.html',context)

# Pedidos

def pedidosView(request):
    context = {
        'pedidos':Pedido.objects.all()
    }
    return render(request, 'pedidos.html', context)

def pedidosCambio(request,pk):
    pedido = Pedido.objects.get(id = pk)
    pedido.entregado = not pedido.entregado
    pedido.save()
    return redirect('pedidos')

def pedidosExtendView(request,pk):
    context = {
        'pedido': Pedido.objects.get(id = pk)
    }
    return render(request,'pedidosExtend.html', context)
# Categorias

def RegistroCategoria(request):
    if request.method == 'POST':
        form = CategoriasForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = CategoriasForm()
    return render(request,'registroItem.html',{'form':form})

def BorrarCategoria(request,pk):
    get_object_or_404(Categoria,id = pk).delete()
    return redirect('productos')

# ITEMS

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

def EditarItem(request,pk):
    itemEditado = Item.objects.get(id=pk)
    form = ItemForm(prefix='form',instance=itemEditado)
    form2 = CategoriasForm(prefix='form2')
    if request.method == 'POST':
        if 'submit_form1' in request.POST:
            form = ItemForm(request.POST,prefix='form',instance=itemEditado)
            form2 = CategoriasForm(prefix='form2')
            if form.is_valid():
                form.save()
                return redirect('productos')
        elif 'submit_form2' in request.POST:
            form = ItemForm(prefix='form',instance=itemEditado)
            form2 = CategoriasForm(request.POST, prefix='form2')
            if form2.is_valid():
                form2.save()
                return HttpResponseRedirect(request.get_full_path())
    return render(request,'registroItem.html',{
        'form':form,
        'form2':form2
        })

def BorrarItem(request,pk):
    get_object_or_404(Item,id = pk).delete()
    return redirect('productos')
