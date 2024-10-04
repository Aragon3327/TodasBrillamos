from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .serializer import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.authtoken.views import obtain_auth_token
from . import tokens

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
    path("categoriaDel/<int:pk>",views.BorrarCategoria,name='borrarCategoria'),

    # APP
    path("JSONlistadoItems/",views.ListadoItems,name='listadoitems'),
    path("JSONItem/<int:id>",views.ItemJSON, name='itemDescripcion'),
    path('registerApp/', views.register_user, name='registerApp'),

    # Autenticación
    path('loginApp/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-token-auth/', tokens.CustomAuthToken.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
