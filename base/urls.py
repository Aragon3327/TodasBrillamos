from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Vistas
    path("", views.dashboard, name='index'),
    path("pedidos/",views.pedidosView, name='pedidos'),
    path("productos/",views.productosView,name='productos'),

    # Usuarios
    path("login/",views.loginView,name='login'),
    path("logout/",views.logoutView,name='logout'),
    
    # Items
    path("itemRegistro/",views.RegistroItem, name='itemRegistro'),
    path("itemDel/<int:pk>/",views.BorrarItem, name='borrarItem'),
    path("itemEdit/<int:pk>/",views.EditarItem, name='editarItem'),

    # Pedidos
    path("pedidoEdit/<int:pk>",views.pedidosCambio, name='editarPedido'),
    path("pedidoExtend/<int:pk>",views.pedidosExtendView,name='pedidosExtend'),

    # Categorias
    path("nuevaCategoria/",views.RegistroCategoria, name='nuevaCategoria'),
    path("categoriaDel/<int:pk>",views.BorrarCategoria,name='borrarCategoria')


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
