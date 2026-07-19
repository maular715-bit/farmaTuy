from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from core import views

router = routers.DefaultRouter()
router.register(r'farmacias', views.FarmaciaViewSet)
router.register(r'medicamentos', views.MedicamentoViewSet)
router.register(r'inventario', views.InventarioViewSet)
router.register(r'tipos', views.TipoViewSet)
router.register(r'usuarios', views.UsuarioViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', include('core.urls')),
    path('api/medicamentos/search/', views.MedicamentosAPI.as_view()),
    path('api/auth/register/', views.RegisterView.as_view(), name='register'),
    path('api/auth/login/', views.LoginView.as_view(), name='login'),
    path('api/auth/me/', views.MeView.as_view(), name='me'),
    path('api/auth/logout/', views.LogoutView.as_view(), name='logout'),
    path('api/auth/social/', views.SocialAuthView.as_view(), name='social_auth'),
]
