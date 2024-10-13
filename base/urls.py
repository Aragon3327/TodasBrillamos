from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from . import tokens

urlpatterns = [
    # Vistas
    path('', views.dashboard, name='index'),
    path('pedidos/',views.pedidosView, name='pedidos'),
    path('productos/',views.productosView,name='productos'),

    # Usuarios
    path('login/',views.loginView,name='login'),
    path('registroAd/',views.registroAdmin,name='registroAdmin'),
    path('logout/',views.logoutView,name='logout'),
    
    # Items
    path('itemRegistro/',views.RegistroItem, name='itemRegistro'),
    path('itemDel/<int:pk>/',views.BorrarItem, name='borrarItem'),
    path('itemEdit/<int:pk>/',views.EditarItem, name='editarItem'),

    # Pedidos
    path('pedidoEdit/<int:pk>',views.pedidosCambio, name='editarPedido'),
    path('pedidoEditPago/<int:pk>',views.pedidosCambioPago,name='editarPedidoPago'),
    path('pedidoExtend/<int:pk>',views.pedidosExtendView,name='pedidosExtend'),

    # Categorias
    path('nuevaCategoria/',views.RegistroCategoria, name='nuevaCategoria'),
    path('categoriaDel/<int:pk>',views.BorrarCategoria,name='borrarCategoria'),

    # APP
    path('JSONlistadoItems/',views.ListadoItems),
    path('JSONItem/<int:id>',views.ItemJSON),
    path('JSONinfoUser/',views.InfoUser),
    path('registerApp/', views.register_user),
    path('JSONpedidosPasados/',views.pedidosPasados),
    path('editarP/',views.EditarPerfil),
    path('crearPedido/',views.crearPedido),

    # Autenticación
    path('api-token-auth/', tokens.CustomAuthToken.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
